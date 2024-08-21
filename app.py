from flask import Flask, request, jsonify, send_file, render_template
from transformers import AutoTokenizer, AutoModelForCausalLM
import io
import torch
import os
from animal_crossing import korean_animalize, print_sound_files_for_characters, split_korean_char, get_sound_files_for_char, CHOSUNG_LIST, JUNGSUNG_LIST, JONGSUNG_LIST
import random
from pydub import AudioSegment
import re

app = Flask(__name__)

# 모델과 토크나이저 로드
model_id = 'gogamza/kobart-base-v2'
tokenizer = AutoTokenizer.from_pretrained(model_id)

# 모델 아키텍처 정의
model = AutoModelForCausalLM.from_pretrained(model_id)

# 학습된 모델 가중치 로드 (전체 모델 객체를 로드)
model = torch.load('k.pth', map_location=torch.device('cpu'))

# GPU 또는 CPU 설정
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# 모델을 평가 모드로 설정
model.eval()

# 전역 변수 정의
shortened_sounds = None

# 텍스트 전처리 함수
def preprocess_text(text):
    return text.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')





def summarize_text(text):
    try:
        text = preprocess_text(text)
        text_parts = [text[i:i+1024] for i in range(0, len(text), 1024)]
        summaries = []

        for part in text_parts:
            inputs = tokenizer(part, return_tensors="pt", truncation=True, max_length=1024).to(device)
            summary_ids = model.generate(
                inputs["input_ids"],
                max_length=380,
                min_length=1,
                num_beams=5,
                length_penalty=1.0,
                no_repeat_ngram_size=2,
                early_stopping=True
            )
            summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
            summaries.append(summary)

        final_summary = " ".join(summaries)
        final_summary = re.sub(r'\s+', ' ', final_summary).strip()

        # 문장 단위로 분리
        sentences = re.split(r'(?<=[.!?])\s+', final_summary.strip())

        # 문장 추출 및 조합
        if len(sentences) > 3:
            selected_sentences = [sentences[1], sentences[2], sentences[-2]]
        else:
            selected_sentences = sentences

        final_summary = ' '.join(selected_sentences).strip()

        # 필요할 경우 추가 문장 삽입
        # additional_sentence = (
        #     "이 특별한 영상은 캠페인으로 진행되었으며 이 캠페인을 통해 “모두가 사랑과 친절을 나눔으로써 지구촌 폭력이 하루 빨리 사라지기를 소망한다”고 말했다."
        # )
        # final_summary = f"{final_summary} {additional_sentence}".strip()


        final_summary = f"{final_summary}".strip()
        # 문장 사이에 적절한 공백 추가
        final_summary = re.sub(r'(?<! )(?=[.,!?])', ' ', final_summary)

        # 특정 패턴 제거 (예: 날짜 및 숫자가 섞인 불필요한 부분)
        final_summary = re.sub(r'(\d{2,})\s*([^\s]*\d+)+', '', final_summary).strip()

        # 필요 시 길이 조정
        if len(final_summary) > 512:
            final_summary = final_summary[:512] + '...'

        return final_summary

    except Exception as e:
        print(f"Error during summarization: {type(e).__name__} - {e}")
        return "Error generating summary"









@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_summary_and_audio', methods=['POST'])
def generate_summary_and_audio():
    global shortened_sounds
    try:
        text = request.form['text']
        print(f"Received text for summarization and audio generation: {text}")
        
        summarized_text = summarize_text(text)
        print(f"Generated summary for audio: {summarized_text}")

        base_dir = os.path.abspath(os.path.dirname(__file__))
        pitch = 'korean'
        sounds = {}
        keys = CHOSUNG_LIST + JUNGSUNG_LIST + JONGSUNG_LIST + [',', '?', ' ', '.']
        for index, ltr in enumerate(keys):
            num = str(index + 1).zfill(2)
            file_path = os.path.join(base_dir, 'sounds', pitch, f'sound{num}.wav')
            sounds[ltr] = file_path if os.path.isfile(file_path) else os.path.join(base_dir, 'sounds', pitch, 'sound01.wav')

        infiles = []
        for char in summarized_text:
            sound_files = get_sound_files_for_char(char, sounds)
            for sound_file in sound_files:
                if os.path.exists(sound_file):
                    infiles.append(sound_file)
                else:
                    print(f"File not found or None: {sound_file}")

        combined_sounds = AudioSegment.silent(duration=0)
        for sound in infiles:
            try:
                tempsound = AudioSegment.from_wav(sound)
                octaves = random.random() * 0.25 + 1.2
                new_sample_rate = int(tempsound.frame_rate * (2.0 ** octaves))
                new_sound = tempsound._spawn(tempsound.raw_data, overrides={'frame_rate': new_sample_rate})
                new_sound = new_sound.set_frame_rate(44100)
                combined_sounds += new_sound
            except Exception as e:
                print(f"Error processing sound {sound}: {e}")

        speedup_factor = 1.3
        combined_sounds = combined_sounds._spawn(
            combined_sounds.raw_data,
            overrides={'frame_rate': int(combined_sounds.frame_rate * speedup_factor)}
        )
        combined_sounds = combined_sounds.set_frame_rate(44100)

        duration = len(combined_sounds)
        shortened_duration = int(duration * 0.6)
        shortened_sounds = combined_sounds[:shortened_duration]

        output_stream = io.BytesIO()
        shortened_sounds.export(output_stream, format="wav")
        output_stream.seek(0)

        return jsonify({
            "original_text": text,
            "summary_k": summarized_text,
            "audio_url": '/audio_stream'
        })

    except Exception as e:
        print(f"Error during summary and audio generation: {type(e).__name__} - {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/audio_stream')
def audio_stream():
    global shortened_sounds
    try:
        if shortened_sounds is None:
            return jsonify({"error": "No audio available"}), 404
        
        output_stream = io.BytesIO()
        shortened_sounds.export(output_stream, format="wav")
        output_stream.seek(0)

        return send_file(
            output_stream,
            mimetype='audio/wav',
            as_attachment=False,
            download_name='output.wav'
        )
    except Exception as e:
        print(f"Error during audio streaming: {type(e).__name__} - {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
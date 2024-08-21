# import random
# from pydub import AudioSegment
# import os

# # 초성, 중성, 종성 리스트
# CHOSUNG_LIST = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
# JUNGSUNG_LIST = ['ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅣ']
# JONGSUNG_LIST = [' ', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']

# def korean_animalize(stringy, pitch, output_stream):
#     base_dir = os.path.dirname(os.path.abspath(__file__))
#     sounds = {}
#     keys = CHOSUNG_LIST + JUNGSUNG_LIST + JONGSUNG_LIST + [',', '?', ' ', '.']

#     # 사운드 파일 경로 설정
#     for index, ltr in enumerate(keys):
#         num = str(index + 1).zfill(2)
#         file_path = os.path.join(base_dir, 'sounds', pitch, f'sound{num}.wav')
        
#         if os.path.isfile(file_path):
#             sounds[ltr] = file_path
#         else:
#             print(f"Warning: Sound file not found: {file_path}")
#             sounds[ltr] = os.path.join(base_dir, 'sounds', pitch, 'sound01.wav')

#     rnd_factor = 0.45 if pitch == 'med' else 0.25
#     infiles = []

#     # 입력 문자열을 기반으로 사운드 파일 수집
#     for i, char in enumerate(stringy):
#         try:
#             if char in CHOSUNG_LIST and (i + 1 < len(stringy) and stringy[i + 1] in CHOSUNG_LIST + [' ']):
#                 sound_file = sounds.get('*' + char, sounds.get(' '))
#             elif char in [',', '?']:
#                 sound_file = sounds.get('.', sounds.get(' '))
#             else:
#                 sound_file = sounds.get(char, sounds.get(' '))

#             if sound_file and os.path.exists(sound_file):
#                 infiles.append(sound_file)
#                 print(f"Added sound file: {sound_file}")
#             else:
#                 print(f"No valid sound file found for character: {char}")
#         except IndexError:
#             print(f"IndexError encountered for character: {char}")
#             pass

#     combined_sounds = AudioSegment.silent(duration=0)

#     # 각 사운드 파일 처리 및 결합
#     for index, sound in enumerate(infiles):
#         try:
#             if os.path.exists(sound):
#                 print(f"Processing sound file: {sound}")
#                 tempsound = AudioSegment.from_wav(sound)
                
#                 if stringy[-1] == '?':
#                     if index >= len(infiles) * 0.8:
#                         octaves = random.random() * rnd_factor + (index - index * 0.8) * 0.1 + 0.3
#                     else:
#                         octaves = random.random() * rnd_factor + 1.5
#                 else:
#                     octaves = random.random() * rnd_factor + 1.0
                
#                 new_sample_rate = int(tempsound.frame_rate * (2.0 ** octaves))
#                 new_sound = tempsound._spawn(tempsound.raw_data, overrides={'frame_rate': new_sample_rate})
#                 new_sound = new_sound.set_frame_rate(44100)
#                 combined_sounds += new_sound
#             else:
#                 print(f"File not found or None: {sound}")
#                 continue
#         except Exception as e:
#             print(f"Error processing sound {sound}: {e}")

#     combined_sounds.export(output_stream, format="wav")
#     print(f"Exported to {output_stream}")



# def korean_decode(korean_word):
#     r_lst = []
#     for w in list(korean_word.strip()):
#         if '가' <= w <= '힣':
#             ch1 = (ord(w) - ord('가')) // 588
#             ch2 = ((ord(w) - ord('가')) - (588 * ch1)) // 28
#             ch3 = (ord(w) - ord('가')) - (588 * ch1) - 28 * ch2
#             r_lst.append([CHOSUNG_LIST[ch1], JUNGSUNG_LIST[ch2], JONGSUNG_LIST[ch3]])
#         else:
#             r_lst.append([w])

#     r_lst = sum(r_lst, [])
#     sentence = "".join([str(_) for _ in r_lst])

#     return sentence

# def print_sound_files_for_characters(stringy, pitch):
#     base_dir = os.path.dirname(os.path.abspath(__file__))
#     sounds = {}
#     keys = CHOSUNG_LIST + JUNGSUNG_LIST + JONGSUNG_LIST + [',', '?', ' ', '.']

#     # 사운드 파일 경로 설정
#     for index, ltr in enumerate(keys):
#         num = str(index + 1).zfill(2)
#         file_path = os.path.join(base_dir, 'sounds', pitch, f'sound{num}.wav')
        
#         if os.path.isfile(file_path):
#             sounds[ltr] = file_path
#         else:
#             sounds[ltr] = os.path.join(base_dir, 'sounds', pitch, 'sound01.wav')

#     # 입력 문자열을 기반으로 사운드 파일 확인
#     for i, char in enumerate(stringy):
#         if char in CHOSUNG_LIST or char in JUNGSUNG_LIST or char in JONGSUNG_LIST or char in [',', '?', ' ', '.']:
#             sound_file = sounds.get(char, sounds.get(' '))
#             if sound_file and os.path.exists(sound_file):
#                 print(f"Character '{char}' maps to sound file: {sound_file}")
#             else:
#                 print(f"Character '{char}' does not have a valid sound file.")
#         else:
#             print(f"Character '{char}' is not mapped to any sound file.")

# # 예제 사용법
# if __name__ == '__main__':
#     pitch = 'korean'
#     stringy = korean_decode("어서와구리 나는 너굴상점의 사장 너굴이라고해구리")
    
#     # 사운드 파일 매핑 출력
#     print_sound_files_for_characters(stringy, pitch)
    
#     # 사운드 파일 생성
#     with open("output.wav", "wb") as f:
#         korean_animalize(stringy, pitch, f)




import random
from pydub import AudioSegment
import os

# 초성, 중성, 종성 리스트
CHOSUNG_LIST = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
JUNGSUNG_LIST = ['ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅣ']
JONGSUNG_LIST = [' ', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']

def split_korean_char(char):
    if '가' <= char <= '힣':
        base = ord(char) - ord('가')
        ch1 = base // 588
        ch2 = (base % 588) // 28
        ch3 = base % 28
        return (CHOSUNG_LIST[ch1], JUNGSUNG_LIST[ch2], JONGSUNG_LIST[ch3])
    else:
        return (char, '', '')

def get_sound_files_for_char(char, sounds):
    cho, jung, jong = split_korean_char(char)
    sound_files = []
    
    if cho and cho in sounds:
        sound_files.append(sounds[cho])
    if jung and jung in sounds:
        sound_files.append(sounds[jung])
    if jong and jong in sounds:
        sound_files.append(sounds[jong])
    
    return sound_files




def korean_animalize(stringy, pitch, output_stream):
    base_dir = os.path.abspath(os.path.dirname(__file__))
    sounds = {}
    keys = CHOSUNG_LIST + JUNGSUNG_LIST + JONGSUNG_LIST + [',', '?', ' ', '.']

    for index, ltr in enumerate(keys):
        num = str(index + 1).zfill(2)
        file_path = os.path.join(base_dir, 'sounds', pitch, f'sound{num}.wav')

        if os.path.isfile(file_path):
            sounds[ltr] = file_path
        else:
            print(f"Warning: Sound file not found: {file_path}")
            sounds[ltr] = os.path.join(base_dir, 'sounds', pitch, 'sound01.wav')

    infiles = []

    for char in stringy:
        sound_files = get_sound_files_for_char(char, sounds)
        for sound_file in sound_files:
            if sound_file and os.path.exists(sound_file):
                infiles.append(sound_file)
            else:
                print(f"No valid sound file found for character: {char}")

    combined_sounds = AudioSegment.silent(duration=0)

    for sound in infiles:
        try:
            if os.path.exists(sound):
                tempsound = AudioSegment.from_wav(sound)
                octaves = random.random() * 0.25 + 1.0
                new_sample_rate = int(tempsound.frame_rate * (2.0 ** octaves))
                new_sound = tempsound._spawn(tempsound.raw_data, overrides={'frame_rate': new_sample_rate})
                new_sound = new_sound.set_frame_rate(44100)
                combined_sounds += new_sound
            else:
                print(f"File not found or None: {sound}")
        except Exception as e:
            print(f"Error processing sound {sound}: {e}")

    combined_sounds.export(output_stream, format="wav")
    print(f"Exported to {output_stream}")

def korean_decode(korean_word):
    r_lst = []
    for w in list(korean_word.strip()):
        if '가' <= w <= '힣':
            ch1 = (ord(w) - ord('가')) // 588
            ch2 = ((ord(w) - ord('가')) - (588 * ch1)) // 28
            ch3 = (ord(w) - ord('가')) - (588 * ch1) - 28 * ch2
            r_lst.append([CHOSUNG_LIST[ch1], JUNGSUNG_LIST[ch2], JONGSUNG_LIST[ch3]])
        else:
            r_lst.append([w])

    r_lst = sum(r_lst, [])
    sentence = "".join([str(_) for _ in r_lst])

    return sentence

def print_sound_files_for_characters(stringy, pitch):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    sounds = {}
    keys = CHOSUNG_LIST + JUNGSUNG_LIST + JONGSUNG_LIST + [',', '?', ' ', '.']

    for index, ltr in enumerate(keys):
        num = str(index + 1).zfill(2)
        file_path = os.path.join(base_dir, 'sounds', pitch, f'sound{num}.wav')
        
        if os.path.isfile(file_path):
            sounds[ltr] = file_path
        else:
            print(f"Warning: Sound file not found: {file_path}")
            sounds[ltr] = os.path.join(base_dir, 'sounds', pitch, 'sound01.wav')

    for char in stringy:
        sound_files = get_sound_files_for_char(char, sounds)
        for sound_file in sound_files:
            if sound_file and os.path.exists(sound_file):
                print(f"Character '{char}' maps to sound file: {sound_file}")
            else:
                print(f"Character '{char}' does not have a valid sound file.")




# 예제 사용법
if __name__ == '__main__':
    pitch = 'korean'
    stringy = korean_decode("어서와구리 나는 너굴상점의 사장 너굴이라고해구리")
    
    # 사운드 파일 매핑 출력
    print_sound_files_for_characters(stringy, pitch)
    
    # 사운드 파일 생성
    with open("output.wav", "wb") as f:
        korean_animalize(stringy, pitch, f)
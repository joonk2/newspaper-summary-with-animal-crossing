import sys
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import pyttsx3
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton, QMessageBox

# 디바이스 설정: GPU가 사용 가능하면 GPU로, 그렇지 않으면 CPU로 설정
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# 모델과 토크나이저 불러오기
model_id = 'gogamza/kobart-base-v2'
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id)

# 저장된 모델 가중치 로드 (map_location 사용)
model.load_state_dict(torch.load('model_adamw_12_8.pth', map_location=device))
model.to(device)
model.eval()

def get_answer2(prefix):
    print(f"input length: {len(prefix)}")
    prefix = tokenizer([prefix], return_tensors="pt").to(device)
    outputs = model.generate(prefix['input_ids'], max_new_tokens=512,  num_beams=10, early_stopping=True)
    decoded_output = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    # 출력 디버깅
    print(f"Decoded output: {decoded_output}")
    print(f"Output length: {len(decoded_output)}")
    
    return decoded_output

class SummarizerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.engine = pyttsx3.init()  # pyttsx3 엔진 초기화
    
    def initUI(self):
        self.setWindowTitle('텍스트 요약 및 음성 변환')
        self.setGeometry(100, 100, 800, 600)

        # 레이아웃 설정
        layout = QVBoxLayout()

        # 원본 텍스트 입력 필드
        self.input_label = QLabel('원본 텍스트:')
        layout.addWidget(self.input_label)
        self.input_text = QTextEdit(self)
        self.input_text.setLineWrapMode(QTextEdit.WidgetWidth)  # 자동 줄바꿈 설정
        layout.addWidget(self.input_text)

        # 요약 텍스트 출력 필드
        self.output_label = QLabel('요약 텍스트:')
        layout.addWidget(self.output_label)
        self.output_text = QTextEdit(self)
        self.output_text.setLineWrapMode(QTextEdit.WidgetWidth)  # 자동 줄바꿈 설정
        self.output_text.setReadOnly(True)
        layout.addWidget(self.output_text)

        # 요약 버튼
        self.summarize_button = QPushButton('요약하기', self)
        self.summarize_button.clicked.connect(self.summarize_text)
        layout.addWidget(self.summarize_button)

        # 음성 실행 버튼
        self.speech_button = QPushButton('음성 실행', self)
        self.speech_button.clicked.connect(self.play_speech)
        layout.addWidget(self.speech_button)

        # 레이아웃 설정
        self.setLayout(layout)
    
    def summarize_text(self):
        # 사용자가 입력한 텍스트 가져오기
        input_text = self.input_text.toPlainText()

        # 요약 생성
        output_text = get_answer2(input_text)
        generated_text = output_text[len(input_text):]

        # 요약된 텍스트를 출력 필드에 표시
        self.output_text.setPlainText(generated_text)

        # 요약된 텍스트 저장 (음성 변환에 사용)
        self.generated_text = generated_text

        # 요약 완료 팝업 메시지
        QMessageBox.information(self, '완료', '요약 완료')

    def play_speech(self):
        # pyttsx3를 사용하여 음성을 생성 및 재생
        self.engine.setProperty('rate', 120)  # 음성 속도 조절
        self.engine.setProperty('volume', 0.8)  # 음량 설정 (0.0 to 1.0)

        # 생성된 텍스트를 직접 재생
        self.engine.say(self.generated_text)
        self.engine.runAndWait()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SummarizerApp()
    ex.show()
    sys.exit(app.exec_())
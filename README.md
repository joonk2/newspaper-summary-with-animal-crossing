## 신문을 요약해주는 언어모델 + 동물의 숲 npc 음성 
<br><br>

![image](https://github.com/user-attachments/assets/8dde5764-820c-4fe3-a13e-4430fca8a7c5)
<br><br>

# 사용법(최소 colab pro 결제 필수)
(아래 사용법을 봐도 잘 안되면 ppt도 참고)

### 1. git clone
```bash
git init
git clone https://github.com/joonk2/newspaper-summary-with-animal-crossing.git

```

### 2. aihub에서 아래링크의 파일을 우선 다운로드 받자
https://www.aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=100&aihubDataSe=realm&dataSetSn=97

### 3. colab을 켜서 kobert_test.ipynb를 불러온다
아까 다운로드 받은 파일 googledrive에 코드 참고해서 정리하고 모델 학습 후 .pth 저장하자<br>
필자는 신문기사 데이터 27만개 다 사용했으나 3만개 or 5만개 등등 사용하는건 본인 마음

### 4. app.py 들어간다
※ 음역대 및 속도 조절은 주석을 달아놓았다 원하는대로 변경하면 될 것 같다. <br>
그리고 app.py가 있는 경로에 들어와 python app.py를 실행하면 뜬다 <br><br>

# 시연영상

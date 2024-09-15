## 신문을 요약해주는 언어모델 + 동물의 숲 npc 음성 
<br><br>

![image](https://github.com/user-attachments/assets/8dde5764-820c-4fe3-a13e-4430fca8a7c5)
<br><br>

# 환경 & 도구
- Colab, VScode, GoogleDrive
- Python
- SLLM모델 (kobart)
- HTML5
- Javascript


# 사용법
(아래 사용법 1 ~ 4 를 봐도 잘 안되면 ppt도 참고)

우선 시작 전에 본인의 노트북이 완전 좋은 gpu의 게임용이라면? --> 코렙결제 필요X, <br>
그게 아니라면 --> **`최소 colab pro`** 결제 권장, 정신건강에 좋으려면 colab pro+도 괜찮을 수도.. 근데 50불이라 한국돈 7만원 상당ㅇㄴ, <br>
"그래도 내는 돈쓰기 싫어서 로컬로 쓸거다" --> 다운로드 엄청 오래걸림ㅋ <br>


### 1. git clone
```bash
git init
git clone https://github.com/joonk2/newspaper-summary-with-animal-crossing.git

```

### 2. aihub에서 아래링크의 파일을 우선 다운로드 받자
https://www.aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=100&aihubDataSe=realm&dataSetSn=97

### 3. colab을 켜서 kobert_test.ipynb를 불러온다
아까 다운로드 받은 파일 googledrive에 코드 참고해서 정리하고 모델 학습 후 .pth 저장하자<br>
필자는 신문기사 데이터 27만개 다 사용했으나 데이터 갯수는 2만개 이상이면 딱히 큰 차이는 없는듯

### 4. app.py 들어간다
※ 음역대 및 속도 조절은 주석을 달아놓았다 원하는대로 변경하면 될 것 같다. <br>
그리고 app.py가 있는 경로에 들어와 python app.py를 실행하면 뜬다 <br><br>

# 시연영상
소리가 안들린다? --> 음소거 되어있음 <br>

https://github.com/user-attachments/assets/f15bce9a-633d-4efb-984f-df6a65619f06

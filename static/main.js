document.addEventListener('DOMContentLoaded', function() {
    var form = document.getElementById('textForm');
    var audioPlayer = document.getElementById('audioPlayer');
    var summaryContainer = document.getElementById('summaryContainer');
    var summaryText = document.getElementById('summaryText');
    var timerElement = document.getElementById('timer');
    var timerBox = document.getElementById('timer-box');
    var birdGif = document.getElementById('bird-gif');

    form.onsubmit = async function(event) {
        event.preventDefault(); // 폼 제출 기본 동작 방지

        // 요약본과 오디오 플레이어 숨기기
        summaryContainer.style.display = 'none';
        audioPlayer.style.display = 'none';
        audioPlayer.src = ''; // 오디오 소스 초기화
        summaryText.innerHTML = ''; // 요약본 초기화

        // 타이머와 GIF를 초기화하고 보여주기
        timerBox.style.display = 'block';
        birdGif.style.display = 'block';

        var formData = new FormData(form);
        var textArea = formData.get('text');  // 입력된 텍스트 가져오기

        // 문장 길이에 따라 예상 시간을 설정합니다 (예: 1초당 20자)
        const charsPerSecond = 20; // 초당 처리 가능한 문자 수
        const estimatedTime = Math.ceil(textArea.length / charsPerSecond); // 예상 처리 시간
        const totalTime = Math.max(5, estimatedTime); // 최소 5초 설정

        let remainingTime = totalTime;
        timerElement.textContent = remainingTime;

        const timer = setInterval(function() {
            remainingTime--;
            timerElement.textContent = remainingTime;

            if (remainingTime <= 0) {
                clearInterval(timer);  // 타이머 정지
                timerBox.style.display = 'none';  // 타이머 숨기기
                birdGif.style.display = 'none';   // GIF 숨기기
            }
        }, 1000);

        try {
            const startTime = Date.now();
            const response = await fetch('/generate_summary_and_audio', {
                method: 'POST',
                body: formData
            });

            // 응답 상태 확인
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            // JSON 응답 파싱
            const data = await response.json();

            // 서버 응답 완료 시간 측정
            const endTime = Date.now();
            const elapsedTime = (endTime - startTime) / 1000; // 초 단위

            // 타이머 조정
            remainingTime = Math.max(0, totalTime - Math.round(elapsedTime));
            timerElement.textContent = remainingTime;

            // 요약본과 오디오 플레이어를 보여주기
            summaryText.innerHTML = `<p>${data.summary_k}</p>`; // 요약된 텍스트를 summaryText에 추가
            summaryContainer.style.display = 'block'; // 요약본 표시

            audioPlayer.src = data.audio_url;
            audioPlayer.style.display = 'block'; // 오디오 플레이어 표시

            // 오디오가 재생되기 시작하면 타이머와 GIF 숨기기
            audioPlayer.addEventListener('play', function() {
                timerBox.style.display = 'none';  // 타이머 숨기기
                birdGif.style.display = 'none';   // GIF 숨기기
            });

            audioPlayer.play(); // 자동 재생

        } catch (error) {
            console.error('Error:', error);
            summaryText.innerHTML = '요약본 생성에 실패했습니다. 다시 시도해주세요.'; // 에러 메시지 표시
            summaryContainer.style.display = 'block'; // 에러 메시지 표시
        } finally {
            // 타이머가 이미 정지했으므로 추가적인 작업 없음
        }
    };
});
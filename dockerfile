# 1. 베이스 이미지 설정 (가벼운 파이썬 이미지)
FROM python:3.10-slim

# 2. 작업 디렉토리 설정
WORKDIR /app

# 3. 필요한 라이브러리 설치
# (requirements.txt가 없다면 직접 설치 명령어를 써도 됩니다)
RUN pip install --no-cache-dir kuksa-client

# 4. 소스 코드 복사
COPY seat_service.py .

# 5. 실행 명령
# 도커 내부에서 실행되므로 호스트 IP 대신 환경변수 등을 쓸 수 있지만, 
# 여기서는 간단히 실행하도록 설정합니다.
CMD ["python", "seat_service.py"]
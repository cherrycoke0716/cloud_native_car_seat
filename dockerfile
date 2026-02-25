FROM python:3.10-slim

WORKDIR /app

RUN pip install --no-cache-dir kuksa-client

# 경로 수정: src 폴더 안의 파일을 현재 작업 디렉토리(/app)로 복사
COPY src/seat_service.py .

CMD ["python", "seat_service.py"]
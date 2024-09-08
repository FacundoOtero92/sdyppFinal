FROM python:3.12.3-slim
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY . .
COPY credentials.json /app/credentials.json
RUN pip install -r requirements.txt
ENV GOOGLE_APPLICATION_CREDENTIALS=/app/credentials.json
CMD ["python", "coordinator.py"]
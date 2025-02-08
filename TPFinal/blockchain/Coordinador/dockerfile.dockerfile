FROM python:3.10.14-alpine3.20
WORKDIR /app
COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
ENV PYTHONUNBUFFERED=1
CMD ["python", "coordinator.py"]
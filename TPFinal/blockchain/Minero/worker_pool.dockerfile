FROM python:3.12

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY worker_pool.py ./

CMD ["python", "worker_pool.py"]

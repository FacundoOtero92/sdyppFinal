import pika
import json
import hashlib
import random
import requests
import time
import threading
import os

# Configuración desde variables de entorno
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT", "5672"))
COORDINATOR_URL = os.getenv("COORDINATOR_URL", "http://coordinador-integrador:5000/solved_task")
QUEUE_NAME = os.getenv("QUEUE_NAME", "QueueTransactions")
EXCHANGE_BLOCK = os.getenv("EXCHANGE_BLOCK", "ExchangeBlock")
NUM_WORKERS = int(os.getenv("NUM_WORKERS", "2"))

def calculate_hash(data):
    hash_md5 = hashlib.md5()
    hash_md5.update(data.encode('utf-8'))
    return hash_md5.hexdigest()

def send_result(data):
    try:
        response = requests.post(COORDINATOR_URL, json=data)
        print("Post response:", response.text)
    except requests.exceptions.RequestException as e:
        print("Failed to send POST request:", e)

def process_message(ch, method, properties, body):
    data = json.loads(body)
    print(f"Message {data} received")
    
    encontrado = False
    intentos = 0
    start_time = time.time()

    print("## Iniciando Minero ##")

    while not encontrado:
        intentos += 1
        random_number = str(random.randint(0, data['numMaxRandom']))
        hash_calculado = calculate_hash(random_number + data['baseStringChain'] + data['blockchainContent'])
        
        if hash_calculado.startswith(data['prefijo']):
            encontrado = True
            processing_time = time.time() - start_time
            
            data_result = {
                'blockId': data['blockId'],
                'processingTime': processing_time,
                'hash': hash_calculado,
                'result': random_number   
            }
            
            print(f"[x] Hash con el prefijo {data['prefijo']} encontrado")
            print(f"[x] HASH: {hash_calculado}")
            send_result(data_result)
    
    ch.basic_ack(delivery_tag=method.delivery_tag)
    print(f"Result found and posted for block ID {data['blockId']} in {processing_time:.2f} seconds in {intentos} attempts")

def worker():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT, credentials=pika.PlainCredentials("guest", "guest")))
    channel = connection.channel()
    channel.exchange_declare(exchange=EXCHANGE_BLOCK, exchange_type='topic', durable=True)
    result = channel.queue_declare('', exclusive=True)
    queue_name = result.method.queue
    channel.queue_bind(exchange=EXCHANGE_BLOCK, queue=queue_name, routing_key='blocks')
    channel.basic_consume(queue=queue_name, on_message_callback=process_message, auto_ack=False)
    print('Worker started, waiting for messages...')
    channel.start_consuming()

def main():
    workers = []
    for _ in range(NUM_WORKERS):
        thread = threading.Thread(target=worker)
        thread.start()
        workers.append(thread)
    for thread in workers:
        thread.join()

if __name__ == '__main__':
    main()

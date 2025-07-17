import pika
import json
import hashlib
import random
import requests
import time
import os
import threading

hostRabbit = os.getenv("RABBITMQ_HOST", "rabbitmq")
exchangeBlock = os.getenv("EXCHANGE_BLOCK", "ExchangeBlock")
NUM_WORKERS = int(os.getenv("NUM_WORKERS", "2"))


def calculateHash(data):
    hash_md5 = hashlib.md5()
    hash_md5.update(data.encode('utf-8'))
    return hash_md5.hexdigest()


def sendResult(data):
    coordinator_url = os.getenv("COORDINATOR_URL", "http://coordinador-integrador:5000/solved_task")

    try:
        response = requests.post(coordinator_url, json=data)
        print("Post response:", response.text)
    except requests.exceptions.RequestException as e:
        print("Failed to send POST request:", e)


def on_message_received(ch, method, properties, body):
    data = json.loads(body)
    print(f"Message {data} received")

    encontrado = False
    intentos = 0
    startTime = time.time()

    print("## Iniciando Minero ##")

    while not encontrado:
        print("+++++++++++++++++++++++++++POOL++++++++++++++++++++++++++++++++++")
        intentos += 1
        randomNumber = str(random.randint(0, data['numMaxRandom']))

        hashCalculado = calculateHash(randomNumber + data['baseStringChain'] + data['blockchainContent'])
        if hashCalculado.startswith(data['prefijo']):
            encontrado = True
            processingTime = time.time() - startTime

            dataResult = {
                'blockId': data['blockId'],
                'processingTime': processingTime,
                'hash': hashCalculado,
                'result': randomNumber
            }

            print(f"[x] Hash con el prefijo {data['prefijo']} encontrado")
            print(f"[x] HASH: {hashCalculado}")
            sendResult(dataResult)

    ch.basic_ack(delivery_tag=method.delivery_tag)
    print(f"Result found and posted for block ID {data['blockId']} in {processingTime:.2f} seconds after {intentos} attempts")


def worker():
    while True:
        try:
            print("+++++++++++++++++++++++++++POOL2++++++++++++++++++++++++++++++++++")
            connection = pika.BlockingConnection(pika.ConnectionParameters(
                host=hostRabbit, port=5672,
                credentials=pika.PlainCredentials("guest", "guest")))

            channel = connection.channel()
            channel.exchange_declare(exchange=exchangeBlock, exchange_type='topic', durable=True)
            result = channel.queue_declare('', exclusive=True)
            queue_name = result.method.queue
            channel.queue_bind(exchange=exchangeBlock, queue=queue_name, routing_key='blocks')

            channel.basic_consume(queue=queue_name, on_message_callback=on_message_received, auto_ack=False)

            print('Worker started, waiting for messages...')
            channel.start_consuming()
        except pika.exceptions.AMQPConnectionError as e:
            print(f"Connection error: {e}. Reconnecting in 5 seconds...")
            time.sleep(5)
        except Exception as e:
            print(f"Unexpected error: {e}. Restarting worker in 5 seconds...")
            time.sleep(5)


def main():
    threads = []
    for _ in range(NUM_WORKERS):
        thread = threading.Thread(target=worker)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

if __name__ == '__main__':
    main()

import hashlib
import json
import random
import threading
from flask import Flask, jsonify, request
import pika
import redis
import time
from google.cloud import storage

app = Flask(__name__)

# VARIABLES

hostRedis = 'redis-integrador'
portRedis = 6379
hostRabbit = 'rabbitmq'
queueNameTx = 'QueueTransactions'
exchangeBlock = 'ExchangeBlock'
timer = 15
datosBucket = []
bucketName = 'bucket_integrador'
credentialPath = 'credentials.json'


# Conexion a Redis

def redisConnect():
    client = redis.Redis(host = hostRedis, port = portRedis, db = 0)
    print('[x] Conectado a Redis')
    return client

# Conexion a Rabbit-MQ para encolar Transacciones

def queueConnect():
    # connection = pika.BlockingConnection(pika.ConnectionParameters(host=hostRabbit))
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=hostRabbit,
        port=5672,
        credentials=pika.PlainCredentials("guest", "guest"),
    )
)


    channel = connection.channel()
    channel.queue_declare(queue=queueNameTx)
    channel.exchange_declare(exchange=exchangeBlock, exchange_type='topic', durable=True)
    print(f'[x] Conectado a Rabbit-MQ')
    return connection, channel

def bucketConnect(bucketName, credentialPath):
    bucketClient = storage.Client.from_service_account_json(credentialPath)
    bucket = bucketClient.bucket(bucketName)
    return bucket

def encolar(transaction):

    jsonTransaction = json.dumps(transaction)
    channel.basic_publish(exchange='',
                            routing_key=queueNameTx,
                            body=jsonTransaction)
    print(f'[x] Se enconlo en {queueNameTx}: {transaction}')   



# Validar que lo que me haya llegado es una transaccion
# {'origen': 'idOrigen'
#  'destino': 'idDestino'
#  'monto': 'monto'}

def validarTransaction(transaction): 
    if transaction['origen'] and transaction['destino'] and transaction['monto']:
        return True
    else: 
        return False
    
def calculateHash(data):
    hash_md5 = hashlib.md5()
    hash_md5.update(data.encode('utf-8'))
    return hash_md5.hexdigest()

# --- Metodos Redis --- #

def getUltimoBlock():

    ultimoBlock = client.lindex('blockchain', 0)
    if ultimoBlock:
        return json.loads(ultimoBlock)
    return None 

def existBlock(id):
    allBlocks = client.lrange('blockchain',0,-1)

    for block in allBlocks:
            msg = json.loads(block)
            if 'blockId' in msg and msg['blockId'] == id:
                return True
            return False
    
def postBlock(block):
    blockJson = json.dumps(block)
    client.lpush('blockchain', blockJson)

# --- TERMINAN METODOS REDIS --- #


def subirBlock(bucket,block): #bucket, block

    blockId = block['blockId']
    jsonBlock = json.dumps(block)

    fileName = (f'block_{blockId}.json')

    # Crear un blob (objeto en el bucket) con el nombre deseado
    blob = bucket.blob(fileName)
    
    # Subir la imagen al blob
    blob.upload_from_string(jsonBlock, content_type='application/json')

    print(f"[x] El bloque {blockId} fue subido al bucket con el nombre de {fileName}")

def descargarBlock(bucket, blockId):
    
    # Nombre del archivo en bucket
    fileName =  (f'block_{blockId}.json')

    # Obtener el blob (archivo) del bucket
    blob = bucket.blob(fileName)

    # Descargamos del bucket
    jsonBlock = blob.download_as_text()

    # Serializamos

    block = json.loads(jsonBlock)

  
    print(f"[x] {blockId} Descaargo del Bucket")
    return block



@app.route('/transaction', methods=['POST'])
def addTransaction():

    transaction = request.json

    try:
        if validarTransaction(transaction):
            print('OK')
            encolar(transaction)    # Encolar
            

    except Exception as e:
        print("[x] La transaccion no es valida")
        print(e)
        return 'Transaccion no recibida', 400

    return 'Transaccion Recibida', 200

@app.route('/status', methods=['GET'])
def status():
    mensaje = jsonify({'status': 'OK'})
    return mensaje

@app.route('/solved_task', methods=['POST'])
def receive_solved_task():
    
    newBlock = {
        'blockId': None,
        'hash': None,
        'hashPrevio': None,
        'nonce': None,
        'prefijo': None,
        'transactions': None,
        'timestamp': None,
        'blockchainContent': None,
        'baseStringChain' : None
    }

    data = request.get_json()

    global datosBucket
    
    # Procesa los datos recibidos
    if data:
        print(f"Received data: {data}")
        
        bucket=bucketConnect(bucketName, credentialPath)
        block = descargarBlock(bucket, data['blockId'])
        dataHash = data['result'] + block['baseStringChain'] + block['blockchainContent']
        hashResult = calculateHash(dataHash)
        timestamp = time.time()
        print(f"[x] Hash recibido: {data['hash']}")
        print(f"[x] Hash calculado: {hashResult}")
        print('')

        if hashResult == data['hash']:
            print('[x] Los Hash son iguales » Data valida.')

            # Validar si existe el bloque
            if existBlock(block['blockId']):
                print('[x] Existe Bloque » Descartar')
                return jsonify({'message': 'El bloque ya fue resuelto » DESCARTADO'}), 200
            else:
                print('[x] No existe bloque » Proceder')
                print('')

                # Calcular blockchainContent
                blockchainData = block['baseStringChain'] + data['hash'] # H('A2F8' + Hash del worker)  
                blockchainContent = calculateHash(blockchainData)
                newBlock['blockchainContent'] = blockchainContent
                print(f"[x] Blockchain Content: {blockchainContent}")

                # Obtener ultimo bloque

                try:
                    ultimoBloque = getUltimoBlock()
                except:
                    ultimoBloque = None
                
                if ultimoBloque != None:
                    print('[x] Hay bloque anterior » Conectar bloques')

                    # Conectar los bloques
                    newBlock['hashPrevio'] = ultimoBloque['hash']
                    print(f"[x] Hash del ultimo bloque: {ultimoBloque['hash']}")

                else:
                    print('[x] No hay bloque anterior » Bloque genesis')
                    newBlock['hashPrevio'] = None

            # Armamos bloque

            newBlock['blockId'] = data['blockId']
            newBlock['hash'] = data['hash']
            newBlock['transactions'] = block['transactions']
            newBlock['prefijo'] = block['prefijo']
            newBlock['baseStringChain'] = block['baseStringChain']
            newBlock['timestamp'] = timestamp
            newBlock['nonce'] = data['result']

            postBlock(newBlock)
            print('[x] Bloque validado » Agregado a la blockchain')

            return jsonify({'message': 'Bloque validado » Agregado a la blockchain'}), 201

        else:
            print('[x] Los Hash son distintos » Dato invalido')
            return jsonify({'message': 'El Hash recibido es invalido » DESCARTADO'}), 200
        # Aquí puedes agregar la lógica de procesamiento de datos

    else:
        # Si no se reciben datos, responde con un error
        return jsonify({'status': 'error', 'message': 'No data received'}), 400
    
def processPackages():
    while True:
        contadorTransaction = 0
        print('[x] Buscando Transacciones')
        print('---------------------------')
        print('')
        listaTransactions = []
        for _ in range(20):
            method_frame, header_frame, body = channel.basic_get(queue=queueNameTx)
            if method_frame:
                contadorTransaction = contadorTransaction + 1
                listaTransactions.append(json.loads(body))
                print(f"[x] Desencole una transaccion")
                print(f'[x] Transaccion: {body}')
                print('')
                channel.basic_ack(method_frame.delivery_tag)
            else:
                print('[x] No hay transacciones')
                print(f'[x] Cantidad de trasacciones desencoladas: {contadorTransaction}')
                print('')
                break

        if listaTransactions: # Armar bloque
            print('')

            maxRandom = 99999999
            blockId = str(random.randint(0, maxRandom))

            block = {
                "blockId": blockId,
                "transactions": listaTransactions,
                "prefijo": '000',
                "baseStringChain": "A3F8",
                "blockchainContent": getUltimoBlock()['blockchainContent'] if getUltimoBlock() else "0",
                "numMaxRandom": maxRandom 
            }

            print(f"blockchainContent: {block['blockchainContent']}")

            # Guardar en bucket
            global datosBucket 
            datosBucket.append(block)

            # Me conecto al bucket
            bucket = bucketConnect(bucketName, credentialPath)
            subirBlock(bucket, block)

            # Publicar el bloque en el Topic
            channel.basic_publish(exchange= exchangeBlock, routing_key='blocks', body=json.dumps(block))
            print(f'[x] Bloque {blockId} enviado')
            print('')


        time.sleep(timer)



# Conectamos a la cola
     
connection, channel = queueConnect()
client = redisConnect()

status_thread = threading.Thread(target=processPackages)
status_thread.start()

if __name__ == '__main__':
    app.run(host='0.0.0.0')


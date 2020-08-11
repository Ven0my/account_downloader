import pika

scan = input("Enter message to pass on ACCOUNT_DOWNLOADER Queue:")
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='ACCOUNT_DOWNLOADER')
channel.basic_publish(exchange='',
                    routing_key='ACCOUNT_DOWNLOADER',
                    body=scan)
print(scan + "sent to ACCOUNT_Downloader Queue")
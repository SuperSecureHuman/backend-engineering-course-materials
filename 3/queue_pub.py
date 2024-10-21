import pika
import sys


def publish_message(message):
    # Update the connection parameters with your RabbitMQ server's details
    connection_params = pika.ConnectionParameters('localhost')
    connection = pika.BlockingConnection(connection_params)
    channel = connection.channel()

    channel.queue_declare(queue='task_queue', durable=True)

    channel.basic_publish(
        exchange='',
        routing_key='task_queue',
        body=message,
        properties=pika.BasicProperties(
            delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE))

    print(f" [x] Sent '{message}'")
    connection.close()


if __name__ == '__main__':
    message = ' '.join(sys.argv[1:]) or "Hello World!"
    publish_message(message)

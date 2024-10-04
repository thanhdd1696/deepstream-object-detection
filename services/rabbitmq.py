import pika
import urllib
import json
from time import time
from configs.settings import settings


class MqPublisher(object):
    EXCHANGE = settings.EXCHANGE
    EXCHANGE_TYPE = settings.EXCHANGE_TYPE
    EXCHANGE_ROUTING_KEY = settings.EXCHANGE_ROUTING_KEY
    EXCHANGE_USER = settings.EXCHANGE_USER
    EXCHANGE_PASSWORD = settings.EXCHANGE_PASSWORD
    EXCHANGE_IP = settings.EXCHANGE_IP
    EXCHANGE_VIRTUALHOST = settings.EXCHANGE_VIRTUALHOST

    def __init__(self):
        self._retry = 0
        self._channel = None
        self._connection = None
        self._queue = None
        credentials = pika.PlainCredentials(self.EXCHANGE_USER,
                                            self.EXCHANGE_PASSWORD)
        mqparameters = pika.ConnectionParameters(self.EXCHANGE_IP,
                                                 credentials=credentials,
                                                 virtual_host=self.EXCHANGE_VIRTUALHOST)
        self._connection = pika.BlockingConnection(mqparameters)
        self._channel = self._connection.channel()
        self._channel.exchange_declare(exchange=self.EXCHANGE,
                                       exchange_type=self.EXCHANGE_TYPE)
        self._channel.queue_declare("AEQ-1", durable=True)

    def publish_message(self, ai_count):
        try:
            routing_key = "AEQ-1"
            msg = json.dumps({
                "ai_count": ai_count
            })
            # print(ai_count, topic)
            self._channel.basic_publish(
                exchange=self.EXCHANGE,
                routing_key=routing_key,
                body=msg
            )

            self._retry = 0
        except Exception as ex:
            print(ex)

    def stop(self):
        self.close_channel()
        self.close_connection()

    def close_channel(self):
        if self._channel is not None:
            self._channel.close()

    def close_connection(self):
        if self._connection is not None:
            self._connection.close()


publisher = MqPublisher()

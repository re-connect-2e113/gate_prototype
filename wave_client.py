import json
import os
from urllib import request
import time
import random

# 彼女たち用のWAVEクライアント(仮)
class WaveClient():

  def __init__(self, wave_server_url, message_queue_channel):
    # WAVEサーバーのURL
    self.wave_server_url = wave_server_url
    self.channel = message_queue_channel
    # 受け取ったメッセージを取り出すキュー
    self.channel.queue_declare(queue = 'wave-messages-to-her', durable = True)

  # WAVEクライアント起動メソッド
  def lauch(self, callback) :
    # メッセージを受け取る都度実行される
    def event_handler(ch, method, properties, body):
      message_data = json.loads(body)
      # TODO: 正しいJSONだったら受け取り成功ackにする
      self.channel.basic_ack(delivery_tag = method.delivery_tag)
      callback(message_data)

    self.channel.basic_consume(
        event_handler,
        queue ='wave-messages-to-her',
        no_ack = False
    )
    self.channel.start_consuming()

  # WAVE送信メソッド
  def send_message(self, message) :
    payload = json.dumps({
      'text': message,
      'recipient': 'YOU'
    }).encode('utf-8')
    time.sleep(random.randrange(1, 5))
    req = request.Request(self.wave_server_url + '/messages', data = payload, method = 'POST', headers = { 'Content-Type': 'application/json' })
    with request.urlopen(req) as res:
      body = res.read().decode('utf-8')
      print(body)

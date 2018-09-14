import json

# 彼女たち用のWAVEクライアント(仮)
class WaveClient():

  def __init__(self, message_queue_channel) :
    self.channel = message_queue_channel
    # 受け取ったメッセージを取り出すキュー
    self.channel.queue_declare(queue='wave-messages', durable=True)

  # WAVEクライアント起動メソッド
  def lauch(self, callback) :
    # メッセージを受け取る都度実行される
    def event_handler(ch, method, properties, body):
      message_data = json.loads(body)
      callback(message_data)
      self.channel.basic_ack(delivery_tag = method.delivery_tag)

    self.channel.basic_consume(
        event_handler,
        queue='wave-messages',
        no_ack=False
    )
    self.channel.start_consuming()

  # WAVE送信メソッド
  def send_message(self, message) :
    pass

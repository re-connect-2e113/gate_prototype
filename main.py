import os
import pika
from urllib import parse as url_parse
from wave_client import WaveClient
import gensim

# 受け答えのBotさん側発言のW2Vを作るのに使われたのと同じgensimモデル
W2V_MODEL_PATH = os.getenv('W2V_MODEL_PATH')
W2V_MODEL_DIMS = os.getenv('W2V_MODEL_DIMS')
model = gensim.models.KeyedVectors.load_word2vec_format(W2V_MODEL_PATH, binary=False)

RABBITMQ_URL = os.getenv('RABBITMQ_URL', 'localhost')
rabbitmq_url = url_parse.urlparse(RABBITMQ_URL)
# 接続する
connection = pika.BlockingConnection(
  pika.ConnectionParameters(host=rabbitmq_url.hostname),
)
# チャンネルを作る
channel = connection.channel()

# WAVEクライアントを作成
wave = WaveClient(channel)

# メッセージ紡ぐ関数
def weave_message(message_data):
  # 届いたメッセージを確認
  # print(message_data['text'])
  wave.send_message('どーん！')

# WAVEクライアントを起動し、メッセージ受信したときにメッセージを紡ぐ
wave.lauch(weave_message)

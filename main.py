import os
import pika
from urllib import parse as url_parse
from wave_client import WaveClient
import gensim
from morphologic_analyzer import MorphogicAnalizer
import conversation_loader

# 受け答えのBotさん側発言のW2Vを作るのに使われたのと同じgensimモデル
W2V_MODEL_PATH = os.getenv('W2V_MODEL_PATH')
W2V_MODEL_DIMS = os.getenv('W2V_MODEL_DIMS')
model = gensim.models.KeyedVectors.load_word2vec_format(W2V_MODEL_PATH, binary=False)

# WAVEのメッセージを受け取るのに必要なジョブキューへの接続を用意
RABBITMQ_URL = os.getenv('RABBITMQ_URL', 'localhost')
rabbitmq_url = url_parse.urlparse(RABBITMQ_URL)
# 接続する
connection = pika.BlockingConnection(
  pika.ConnectionParameters(host=rabbitmq_url.hostname),
)
# チャンネルを作る
channel = connection.channel()

# 分かち書きを得るために使う
analyzer = MorphogicAnalizer('MeCab')

# WAVEクライアントを作成
wave = WaveClient(channel)


# TODO: 本当はDBに入れておきたい
CONVERSATION_CSV_PATH = os.getenv('CONVERSATION_CSV_PATH')
# TODO: 本当は宛先情報から読み出したい
PRECIOUS_NAME = os.getenv('PRECIOUS_NAME')
conversations = conversation_loader.load(PRECIOUS_NAME, CONVERSATION_CSV_PATH)

def weave_message(message_data):
  # 届いたメッセージからっ表層系だけ取り出し
  nodes = analyzer.analyze(message_data['text'])
  surfaces = map(lambda node: node.surface, nodes)
  surfaces = list(surfaces)

  # 謎の単語を取り除く
  known_words = filter(lambda surface: surface in model.vocab, surfaces)
  known_words = list(known_words)

# WAVEクライアントを起動し、メッセージ受信したときにメッセージを紡ぐ
wave.lauch(weave_message)

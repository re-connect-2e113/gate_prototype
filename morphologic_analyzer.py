import MeCab
from collections import namedtuple

MorphogicNodeSurface = namedtuple('MorphogicNodeSurface', (
    'part_type',
    'part_detail_type1',
    'part_detail_type2',
    'part_detail_type3',
    'conjugated',
    'conjugation',
    'original',
    'reading',
    'pronunciation'
))

MorphogicNode = namedtuple('MorphogicNode', ('surface', 'feature', 'cost'))

class MorphogicAnalizer:
  def __init__(self, engne_name):
    self.engine = MeCab.Tagger(
        "-Ochasen -d/usr/local/lib/mecab/dic/mecab-ipadic-neologd")
        # "-Ochasen -d/usr/local/lib/mecab/dic/ipadic")
    # バグ対策 無いと UnicodeDecodeError: 'utf-8' codec can't decode byte 0x9c in position 1: invalid start byte とか言われる
    self.engine.parse('')

  def analyze(self, text):
    nodes = []
    currentNode = self.engine.parseToNode(text)
    currentNode = currentNode.next
    while currentNode.next:
      # 空文字も結果として解釈する
      featureString = currentNode.feature.split(',')
      feature = self.build_morphogic_node_surface(featureString)
      node = MorphogicNode(surface=currentNode.surface, feature=feature, cost=currentNode.cost)
      nodes.append(node)
      currentNode = currentNode.next
    return nodes

  def build_morphogic_node_surface(self, featureString):
    try:
      length = len(featureString)
      part_type = featureString[0] if(0 < length) else None
      part_detail_type1 = featureString[1] if(1 < length) else None
      part_detail_type2 = featureString[2] if(2 < length) else None
      part_detail_type3 = featureString[3] if(3 < length) else None
      conjugated = featureString[4] if(4 < length) else None
      conjugation = featureString[5] if(5 < length) else None
      original = featureString[6] if(6 < length) else None
      reading = featureString[7] if(7 < length) else None
      pronunciation = featureString[8] if(8 < length) else None
    except IndexError as err:
      print(err)
    finally:
      return MorphogicNodeSurface(part_type, part_detail_type1, part_detail_type2, part_detail_type3, conjugated, conjugation, original, reading, pronunciation)

import csv

def load(precious_name, csv_path):
  messages = []
  with open(csv_path) as csvFile:
    reader = csv.reader(csvFile)
    # ヘッダーとばす
    next(reader, None)
    for row in reader:
      messages.append({'sender': row[0], 'text': row[1]})

  conversations = []
  for index, message in enumerate(messages):
    if message['sender'] == '':
      # Botのメッセージの時
      conversations.append(
        {
          'sender_name': precious_name,
          'bot_message': message['text'],
          'her_message': messages[index + 1]['text']
        }
      )
  return conversations

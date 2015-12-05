import requests
from requests_oauthlib import OAuth1
import json
import re

CK = 'GKfSyzp8iW1rEIg0D21bBXQ8O'                             # Consumer Key
CS = 'Gb7AdIVbMnR9jpGcVQRq6KgXdyhQHYliigWYOmHete9cheLF6Z'         # Consumer Secret
AT = '2838969204-M9jti6tiMFHIBTrHHaVIe8sG1X9DhAwzVuhLqQS' # Access Token
AS = '7SxqI7rO5jo6wkx5VoXw1YCuvCc8FvC9Ub42pk9xe5C6i'         # Accesss Token Secert



auth = OAuth1(CK, CS, AT, AS)
url = "https://stream.twitter.com/1.1/statuses/sample.json"
r = requests.get(url, auth=auth, stream=True, data={})
#url = "https://stream.twitter.com/1.1/statuses/filter.json"
#r = requests.post(url, auth=auth, stream=True, data={"track":"コミケ"})

for line in r.iter_lines():
  if line:
    try:
      data = json.loads(line.decode('utf-8'))
      if 'text' in data:
        t = data['text']
        if re.match("[ぁ-ゞ]", t) and t.count('#') == 0 and t.count('http') == 0 and len(t)>10:
          print("-"*20)
          print(data['text'])
    except UnicodeEncodeError:
      pass
      #print('ERROR')
  else:
    #print('NOP')
    pass
      

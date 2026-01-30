import os
import argparse
from datetime import datetime
import requests

topics = ['Kenyan politics','AFCON Kenya','Nairobi gossip','Kenyan business']

parser = argparse.ArgumentParser()
parser.add_argument('--out-dir', default='./content')
args = parser.parse_args()

os.makedirs(args.out_dir, exist_ok=True)
topic = topics[datetime.now().weekday() % 4]

def puter_chat(prompt):
    url = "https://api.puter.com/v2/ai/chat"
    payload = {
        "messages": [{"role": "user", "content": prompt}],
        "model": "gpt-4o-mini",
        "stream": False
    }
    response = requests.post(url, json=payload)
    data = response.json()
    return data['choices'][0]['message']['content']

prompt_text = "Write 1000 word UK English blog on '" + topic + "'. Varied sentences. Human style."
body = puter_chat(prompt_text)

filename = datetime.now().strftime('%Y%m%d') + '.md'
path = os.path.join(args.out_dir, filename)

header = "# " + topic + "

"
content = header + body

with open(path, 'w') as f:
    f.write(content)
print("✅ Puter.js created " + path)
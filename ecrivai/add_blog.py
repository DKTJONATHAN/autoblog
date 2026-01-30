import os
import argparse
from datetime import datetime
import requests
import json

topics = ['Kenyan politics','AFCON Kenya','Nairobi gossip','Kenyan business']

parser = argparse.ArgumentParser()
parser.add_argument('--out-dir', default='./content')
args = parser.parse_args()

os.makedirs(args.out_dir, exist_ok=True)
topic = topics[datetime.now().weekday() % 4]

# ✅ Puter.js AI API (FREE GPT-4o/Claude)
def puter_chat(prompt, model='gpt-4o-mini'):
    url = "https://api.puter.com/v2/ai/chat"
    payload = {
        "messages": [{"role": "user", "content": prompt}],
        "model": model,
        "stream": False
    }
    response = requests.post(url, json=payload)
    return response.json()['choices'][0]['message']['content']

prompt = f"Write 1000 word UK English blog on '{topic}'. Varied sentences. Human style."
body = puter_chat(prompt)

path = os.path.join(args.out_dir, datetime.now().strftime('%Y%m%d') + '.md')
with open(path, 'w') as f:
    f.write(f"# {topic}

{body}")
print(f'✅ Puter.js created {path}')
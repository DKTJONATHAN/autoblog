import os
import argparse
from datetime import datetime
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import re

os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

topics = ['Kenyan politics 2026','AFCON Kenya','Nairobi gossip','Kenyan business']
llm = ChatOpenAI(model='gpt-4o-mini', temperature=0.7)

parser = argparse.ArgumentParser()
parser.add_argument('--out-dir', default='./content')
args = parser.parse_args()

topic = topics[datetime.now().weekday() % 4]
title_prompt = PromptTemplate.from_template('Title for Kenyan blog: {t}')
title = (title_prompt | llm | StrOutputParser()).invoke({'t': topic})
body_prompt = PromptTemplate.from_template('Write 1200 word UK English blog titled {t}. Varied sentences, conversational.')
body = (body_prompt | llm | StrOutputParser()).invoke({'t': title})

slug = re.sub(r'[^a-z0-9]', '-', title.lower())
date = datetime.now().strftime('%Y-%m-%d')
fm = '---
title: ' + title + '
date: ' + date + '
slug: ' + slug + '
---

'
path = os.path.join(args.out_dir, date + '-' + slug + '.md')
os.makedirs(args.out_dir, exist_ok=True)
with open(path, 'w') as f:
 f.write(fm + body)
print('Created ' + path)
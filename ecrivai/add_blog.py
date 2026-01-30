import os
import argparse
from datetime import datetime
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

topics = ['Kenyan politics','AFCON Kenya','Nairobi gossip','Kenyan business']
llm = ChatOpenAI(model='gpt-4o-mini', temperature=0.7)

parser = argparse.ArgumentParser()
parser.add_argument('--out-dir', default='./content')
args = parser.parse_args()

os.makedirs(args.out_dir, exist_ok=True)
topic = topics[datetime.now().weekday() % 4]
prompt = PromptTemplate.from_template('Write 1000 word UK English blog on {topic}. Varied sentences.')
body = (prompt | llm | StrOutputParser()).invoke({'topic': topic})
path = os.path.join(args.out_dir, datetime.now().strftime('%Y%m%d') + '.md')
with open(path, 'w') as f:
    f.write(body)
print('Created ' + path)
import os
import argparse
from datetime import datetime
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

# ✅ AUTO-FIND working model
models = []
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        models.append(m.name)
model_name = models[0] if models else 'gemini-1.5-flash'  # fallback
print(f'✅ Using model: {model_name}')

llm = ChatGoogleGenerativeAI(model=model_name, temperature=0.7)

topics = ['Kenyan politics','AFCON Kenya','Nairobi gossip','Kenyan business']
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
print('✅ Created ' + path)
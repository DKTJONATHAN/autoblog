import os
import argparse
import logging
from datetime import datetime
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import re

load_dotenv()
logging.basicConfig(level=logging.INFO)

topics = ["Kenyan politics 2026", "AFCON Kenya news", "Nairobi celebrity gossip", "Kenyan business tips"]

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-dir", default="./content")
    args = parser.parse_args()
    os.makedirs(args.out_dir, exist_ok=True)
    
    topic = topics[datetime.now().weekday() % len(topics)]
    title_prompt = PromptTemplate.from_template("Blog title for: {topic}")
    title = (title_prompt | llm | StrOutputParser()).invoke({"topic": topic}).strip('"')
    
    body_prompt = PromptTemplate.from_template("Write 1500 word blog: {title}. UK English, varied sentences, conversational, SEO, no lists.")
    body = (body_prompt | llm | StrOutputParser()).invoke({"title": title})
    
    slug = re.sub(r'[^a-z0-9]+', '-', title.lower())
    date = datetime.now().strftime('%Y-%m-%d')
    
    fm = '---
title: "{}"
date: {}
slug: {}
---

'.format(title, date, slug)
    
    path = os.path.join(args.out_dir, '{}-{}.md'.format(date, slug))
    with open(path, 'w') as f:
        f.write(fm + body)
    
    logging.info('Wrote ' + path)
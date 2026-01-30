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
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

topics_pool = [
    "latest Kenyan politics governance updates 2026",
    "AFCON African Cup Nations Kenya team news",
    "Nairobi celebrity gossip entertainment trends",
    "Kenyan business entrepreneurship startup tips"
]

topic_prompt = PromptTemplate.from_template("Suggest engaging blog title for Kenyan audience on: {topic_pool}. Output only title.")

content_prompt = PromptTemplate.from_template("Write 1200-1600 word blog post titled '{title}'. UK English. Varied sentence lengths (mix short/long). Conversational professional tone. Structure: Engaging intro, 4-5 sections with subheads, conclusion CTA. Human-like: Contractions, rhetorical questions, anecdotes. Research-backed facts. No lists if possible. SEO keywords natural. Output pure Markdown body (no frontmatter).")

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

topic_chain = topic_prompt | llm | StrOutputParser()
content_chain = content_prompt | llm | StrOutputParser()

def get_blog_chain():
    topic_pool = topics_pool[datetime.now().weekday() % len(topics_pool)]
    title = topic_chain.invoke({"topic_pool": topic_pool})
    body = content_chain.invoke({"title": title})
    return title.strip('"'), body

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-dir", default="./content", type=str)
    args = parser.parse_args()
    
    os.makedirs(args.out_dir, exist_ok=True)
    title, body = get_blog_chain()
    slug = re.sub(r'[^a-z0-9]+', '-', title.lower().strip())
    date_str = datetime.now().strftime('%Y-%m-%d')
    
    frontmatter = "---
title: "{}"
date: {}
slug: {}
description: "Kenyan {} insights."
---".format(title, date_str, slug, slug)
    
    md_content = frontmatter + "

" + body
    out_path = os.path.join(args.out_dir, "{}-{}.md".format(date_str, slug))
    
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(md_content)
    
    logging.info("Wrote {}".format(out_path))
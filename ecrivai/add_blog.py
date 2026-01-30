import os
import argparse
import logging
from datetime import datetime
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import git

load_dotenv()
logging.basicConfig(level=logging.INFO)

topics_pool = [
    "latest Kenyan politics governance updates 2026",
    "AFCON African Cup Nations Kenya team news",
    "Nairobi celebrity gossip entertainment trends",
    "Kenyan business entrepreneurship startup tips"
]

topic_prompt = PromptTemplate.from_template(
    "Suggest engaging blog title for Kenyan audience on: {topic_pool}. Output only title."
)

content_prompt = PromptTemplate.from_template(
    """Write 1200-1600 word blog post titled '{title}'.
    UK English. Varied sentence lengths (mix short/long). Conversational professional tone.
    Structure: Engaging intro, 4-5 sections with subheads, conclusion CTA.
    Human-like: Contractions, rhetorical questions, anecdotes. Research-backed facts.
    No lists if possible. SEO keywords natural.
    Output pure Markdown body (no frontmatter)."""
)

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

    title, body = get_blog_chain()
    slug = title.lower().replace(' ', '-').replace('[^a-z0-9-]', '')
    date_str = datetime.now().strftime('%Y-%m-%d')
    
    frontmatter = f"""---
title: "{title}"
date: {date_str}
slug: {slug}
description: "Kenyan {slug} insights."
---
"""
    
    md_content = frontmatter + "

" + body
    out_path = os.path.join(args.out_dir, f"{date_str}-{slug}.md")
    with open(out_path, 'w') as f:
        f.write(md_content)
    
    logging.info(f"Wrote {out_path}")
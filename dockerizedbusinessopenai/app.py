from flask import Flask, jsonify, request
from uuid import uuid4
from dotenv import load_dotenv
import openai
import os
import pandas as pd
import tiktoken
from urllib.parse import urlparse
import asyncio
import aiohttp

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from utils.webcrawl import crawl, remove_newlines, split_into_many
from flask_cors import CORS

load_dotenv()
openai.api_key = os.environ.get("OPEN_AI_APIKEY")
PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")
PINECONE_API_ENV = os.environ.get("PINECONE_API_ENV")

app = Flask(__name__)
app.config["DEBUG"] = True
CORS(app, origins=["*"])


async def embed_text(text):
    async with aiohttp.ClientSession() as session:
        async with session.post(
            url="https://api.openai.com/v1/embeddings",
            headers={"Authorization": f"Bearer {os.environ.get('OPEN_AI_APIKEY')}"},
            json={"model": "text-embedding-ada-002", "input": text},
        ) as response:
            response = await response.json()
            return response["data"][0]["embedding"]


@app.route("/", methods=["GET", "POST"])
async def hello_from_root():
    business_name = request.json["business_name"]
    business_idea = request.json["business_idea"]
    websites = request.json["domains"]
    domains = websites.split(",")
    texts = []

    for domain in domains:
        root_domain = urlparse(domain).netloc
        print("Crawling " + root_domain + "...")
        await crawl(domain)
        print("reading files...")
        for file in os.listdir("text/" + root_domain + "/"):
            with open("text/" + root_domain + "/" + file, "r") as f:
                text = f.read()

                # Omit the first 11 lines and the last 4 lines, then replace -, _, and #update with spaces.
                texts.append(
                    (
                        urlparse(file)
                        .netloc.replace("-", " ")
                        .replace("_", " ")
                        .replace("#update", ""),
                        text,
                    )
                )

    print("Creating Dataframe...")
    # Create a dataframe from the list of texts
    df = pd.DataFrame(texts, columns=["fname", "text"])

    # Set the text column to be the raw text with the newlines removed
    df["text"] = df.fname + ". " + remove_newlines(df.text)
    df.to_csv("processed/scraped.csv")
    print("Created CSV file.")
    tokenizer = tiktoken.get_encoding("cl100k_base")

    df = pd.read_csv("processed/scraped.csv", index_col=0)
    df.columns = ["title", "text"]
    print("Encoding text...")
    # Tokenize the text and save the number of tokens to a new column
    df["n_tokens"] = df.text.apply(lambda x: len(tokenizer.encode(x)))

    shortened = []

    # Loop through the dataframe
    for row in df.iterrows():
        # If the text is None, go to the next row
        if row[1]["text"] is None:
            continue

        # If the number of tokens is greater than the max number of tokens, split the text into chunks
        if row[1]["n_tokens"] > 500:
            text_chunks = split_into_many(row[1]["text"], 500, tokenizer)
            shortened.extend(
                [{"title": row[1]["title"], "text": chunk} for chunk in text_chunks]
            )

        # Otherwise, add the text, title, and url to the list of shortened texts
        else:
            shortened.append({"title": row[1]["title"], "text": row[1]["text"]})

    df = pd.DataFrame(shortened, columns=["title", "text"])
    df["n_tokens"] = df.text.apply(lambda x: len(tokenizer.encode(x)))
    print("Embedding text... from OpenAI")
    df["embeddings"] = await asyncio.gather(*(embed_text(text) for text in df.text))
    df["embeddings"] = df["embeddings"].apply(np.array)
    df.to_csv("processed/embeddings.csv")

    # Add an 'id' column to the DataFrame
    df["id"] = [str(uuid4()) for _ in range(len(df))]

    # Fill null values in 'title' column with 'No Title'
    df["title"] = df["title"].fillna("No Title")

    embed_model = "text-embedding-ada-002"
    user_input = f"""My business name is: {business_name} My business idea is: {business_idea}. 
    From the information that I have provided, please provide a financial plan month to month and roadmap to help.
    Also list the disadvantages of the business idea."""
    print("Embedding user query...")
    embedding = openai.Embedding.create(input=user_input, engine=embed_model)["data"][
        0
    ]["embedding"]
    # Convert the embedding to a NumPy array
    embedding = np.array(embedding)

    df["similarities"] = df.embeddings.apply(
        lambda x: cosine_similarity(x.reshape(1, -1), embedding.reshape(1, -1))[0][0]
    )
    res = df.sort_values("similarities", ascending=False).head(15)
    contexts = res.text.tolist()

    augmented_query = "\n\n---\n\n".join(contexts) + "\n\n-----\n\n" + user_input

    # system message to assign role the model
    system_msg = f"""You are a business analyst looking to create a business based off 
    of the weaknesses of the context provided. Provide a financial plan month to month and roadmap to help
     create this business. Give 3 business name ideas with it.

     Format this all in Markdown format.
    """
    chat = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": augmented_query},
        ],
    )

    print(chat)

    return jsonify(chat)


if __name__ == "__main__":
    app.run(host="0.0.0.0")

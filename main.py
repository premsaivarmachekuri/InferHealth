import pandas as pd
import numpy as np
import json 
import re
from typing import List, Dict, Any, Optional, Tuple
import faiss
from openai import OpenAI
import time
from sentence_transformers import SentenceTransformer
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import seaborn as sns 
from dotenv import load_dotenv
import openai 
import os
import chromadb
import sqlite3
from langchain_community.utilities import GoogleSerperAPIWrapper
from math import radians, cos, sin, sqrt, atan2
from geocode import get_coordinates
from llm import get_llm_response
load_dotenv()

openai_api_key = os.getenv("OPEN_AI_KEY")
SERPER_API_KEY = os.getenv("SERPER_API_KEY")
GEOCODE_API_KEY = os.getenv("GEOCODE_API_KEY")

df_qa = pd.read_csv("data/train.csv")
df_qa = df_qa.sample(500, random_state=0).reset_index(drop=True)

df_qa["combined_text"] = (
    "Question: " + df_qa["Question"].astype(str) + ". " +
    "Answer: " + df_qa["Answer"].astype(str) + ". "  +
    ": " + df_qa["qtype"].astype(str) + ". "  
)

print(df_qa.head())


df_hospital = pd.read_csv("data/hospitals.csv")
print(df_hospital.shape)
print(df_hospital[["LATITUDE", "LONGITUDE", "CITY", "STATE", "TYPE", "NAME", "ADDRESS", "BEDS", "WEBSITE", "COUNTRY"]].head())


client = chromadb.PersistentClient(path="./chroma_db")

# Collection 1 for medical Q&A Dataset
collection1 = client.get_or_create_collection(name="medical_q_n_a")


collection1.add(
    documents=df_qa['combined_text'].tolist(),
    metadatas=df_qa.to_dict(orient="records"),
    ids=df_qa.index.astype(str).tolist(),
)

query = "What are the treatments for Kawasaki disease ?"

results = collection1.query(query_texts=[query],
    n_results=3
)
# print(results)

search = GoogleSerperAPIWrapper()

print(search.run(query="What are the various vaccines of COVID-19"))


address = "New York City"
coords = get_coordinates(address)
if coords:
    lat, lon = coords
    print(f"Latitude: {lat}, Longitude: {lon}")
else:
    print("Could not retrieve coordinates.")




def main():
    print("Hello from inferhealth!")


if __name__ == "__main__":
    main()

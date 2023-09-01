import openai
import streamlit as st
from embeddings import db
import api
import langchain
openai.api_key = api.OPENAI_API_KEY

def find_match(input):
    result = db.similarity_search(input)
    return result[0].page_content+"\n"+result[1].page_content+"\n"+result[2].page_content

def get_conversation_string(responses,requests):
    conversation_string = ""
    for i in range(len(responses)-1):
        conversation_string += "Human: "+requests[i] + "\n"
        conversation_string += "Bot: "+ responses[i+1] + "\n"
    return conversation_string
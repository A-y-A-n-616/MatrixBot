import regex as re
from OPENSOURCE_MODEL import yt_embeddings_langchain
import langchain
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
    MessagesPlaceholder
)
from langchain.callbacks import get_openai_callback
import requests
from flask import Flask,request
import loops
import streamlit as st
from streamlit_chat import message
from utils import *
import os 
import api
import time
from flask_cors import CORS,cross_origin
from threading import Timer
from langchain.cache import InMemoryCache,SQLiteCache
from flask_caching import Cache
app = Flask(__name__)
CORS(app)
cache=Cache()
app.config["CACHE_TYPE"] = 'simple'
OPENAI_API_KEY = api.OPENAI_API_KEY
cache.init_app(app)
escape=['idon\'tknow','idonotknow','no','matrixnmedia']
greetings=['hi','hello','helo','goodmorning','goodnight','thankyou','thanks','goodafternoon','what\'sup','ok','bye','welcome','yo','hey','hye']

llm = ChatOpenAI(model_name="gpt-3.5-turbo",temperature=0.3, openai_api_key=OPENAI_API_KEY)
buffer_memory=ConversationBufferWindowMemory(k=1,return_messages=True)

system_msg_template = SystemMessagePromptTemplate.from_template(template="""You are virtual assistant of a reputed organization. Answer the question as truthfully as possible using the provided context, 
and if the answer is not contained within the text below, say 'I don't know'""")


human_msg_template = HumanMessagePromptTemplate.from_template(template="{input}")

prompt_template = ChatPromptTemplate.from_messages([system_msg_template, MessagesPlaceholder(variable_name="history"), human_msg_template])

conversation = ConversationChain(memory=buffer_memory, prompt=prompt_template, llm=llm, verbose=True)
responses=[]
requests=[]

@app.route('/query')
def getanswer():
    
    print('starting')
    query = request.args.get('query')
    
    if query:
        try:
            support = loops.refine(yt_embeddings_langchain.get_answer(query))
            if loops.escape_check(escape,support) or loops.contain_check(greetings,loops.refine(query)):
                print(query)
                try:      
                    conversation_string = get_conversation_string(responses,requests)
                    with get_openai_callback() as cb:
                        start = time.time()
                        context = find_match(query) 
                        @cache.memoize(timeout=1800) 
                        def get_response(query):
                            return conversation.predict(input=f"Context:\n {context} \n\n Query:\n{query}")
                        
                        response = get_response(query)
                        end = time.time()
                        print(str(cb),"--",end-start)
                        result={'status':200,'response':response}
                        requests.append(query)
                        responses.append(response)
                        return result
                except Exception as e:
                    print(e)
                    result={'status':408,'result':"An unexpected Error Occured!"}
                    return result
            else:
                response="I don't really't have any specific information about your query"
                result={'status':200,'response':response}
                requests.append(query)
                responses.append(response)
                return result
        except Exception as e:
            result={'status':408,'result':"I am really tired right now! Please give me a little break of 1 minute."}
            return result
    else:
        return  {'status':204,'result':"An unexpected Error Occured!"}    

if __name__=="__main__":
    # langchain.llmcache = SQLiteCache(database_path=".cachedatabase.db")
    app.run()
          
import os
import sys
from tkinter import *
import openai
from langchain.chains import ConversationalRetrievalChain, RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.indexes import VectorstoreIndexCreator
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain.llms import OpenAI
from langchain.vectorstores import Chroma

import constants
chat_history = []
constants.APIKEY = os.environ.get('OPENAI_API_KEY') 

# Enable to save to disk & reuse the model (for repeated queries on the same data)
PERSIST = FALSE
def send_message():
     message = e.get()
     txt.insert(END, "You: " + message + "\n", "sender")
     e.delete(0, END)
     
     

     if PERSIST and os.path.exists("persist"):
          vectorstore = Chroma(persist_directory="persist", embedding_function=OpenAIEmbeddings())
          index = VectorStoreIndexWrapper(vectorstore=vectorstore)
     else:
     #loader = TextLoader("data/data.txt") # Use this line if you only need data.txt
          loader = DirectoryLoader("source_documents/")
          if PERSIST:
               index = VectorstoreIndexCreator(vectorstore_kwargs={"persist_directory":"persist"}).from_loaders([loader])
          else:
               index = VectorstoreIndexCreator().from_loaders([loader])

     chain = ConversationalRetrievalChain.from_llm(
     llm=ChatOpenAI(model="gpt-3.5-turbo"),
     retriever=index.vectorstore.as_retriever(search_kwargs={"k": 1}),
     )
     result = chain({"question": message, "chat_history": chat_history})
     #print(result['answer'])
     txt.insert(END, "Bot: " + result['answer'] + "\n", "receiver")
     chat_history.append((message, result['answer']))

def clear_chat():
    txt.delete(1.0, END)




# GUI
root = Tk()
root.title("Chatbot")

BG_GRAY = "#ABB2B9"
BG_COLOR = "#17202A"
TEXT_COLOR = "#EAECEE"

FONT = "Helvetica 14"
FONT_BOLD = "Helvetica 13 bold"

# Send function

lable1 = Label(root, bg=BG_COLOR, fg=TEXT_COLOR, text="Welcome", font=FONT_BOLD, pady=10, width=20, height=1).grid(
     row=0)

txt = Text(root, bg=BG_COLOR,  fg=TEXT_COLOR,font=FONT, width=100)
txt.grid(row=1, column=0, columnspan=2,padx=5,pady=2)
#txt.tag_configure("sender", foreground="blue")
#txt.tag_configure("receiver", foreground="red")

scrollbar = Scrollbar(txt)
scrollbar.place(relheight=1, relx=0.974)

e = Entry(root, bg="#2C3E50", fg=TEXT_COLOR, font=FONT, width=80)
e.grid(row=2, column=0)

send = Button(root, text="Send", font=FONT_BOLD, bg=BG_GRAY,
               command=send_message).grid(row=2, column=1)

clear_button = Button(root, text="Clear", font=FONT_BOLD, bg=BG_GRAY,
               command=clear_chat).grid(row=2, column=2)

root.mainloop()

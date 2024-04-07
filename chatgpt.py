# importing  the required libraries
import os

from dotenv import load_dotenv
from langchain import OpenAI
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.document_loaders import PDFPlumberLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.prompts.chat import (ChatPromptTemplate,
                                    HumanMessagePromptTemplate,
                                    SystemMessagePromptTemplate)
from langchain.vectorstores import Chroma

# loading the OpenAI key


def load_key():
    load_dotenv()
    os.environ["OPENAI_API_KEY"] = os.getenv('OpenAI_key')


# function to load the PDF DOC
def load_doc(doc):
    loader = PDFPlumberLoader(doc)
    data = loader.load_and_split()
    return data


# adding data to the vector store


def create_chromadb(data, persist_directory):
    embeddings = OpenAIEmbeddings()
    vectordb = Chroma.from_documents(
        documents=data,
        embedding=embeddings,
        persist_directory=persist_directory)
    return vectordb

# add new doc need to test 
def add_doc(data, vectordb):
    vectorstore = Chroma.add_documents(
        documents=data,
        self=vectordb
    )
    return vectorstore

# retriving the info


def retrive_db(pre_dirctory):
    vectorstore = Chroma(persist_directory= pre_dirctory,
                         embedding_function=OpenAIEmbeddings())
    return vectorstore
# creating the vector chain


def creating_chain(vectordb, chain_type_kwargs):
    chain = RetrievalQAWithSourcesChain.from_chain_type(
        OpenAI(model_name="gpt-3.5-turbo", temperature=0),
        chain_type="stuff",
        retriever=vectordb.as_retriever(),
        return_source_documents=True,
        chain_type_kwargs=chain_type_kwargs)
    return chain


# System template
def chain_msg():
    system_template = """Use the following pieces of context to answer the users question.
                       Take note of the sources and include them in the answer in the format: "SOURCES: source1 source2", use "SOURCES" in capital letters regardless of the number of sources.
                       Add an indication when moving to next line : "1. this is a demo line.\\n".
                       If you don't know the answer, just say that "I don't know", don't try to make up an answer.
                       ----------------
                       {summaries}"""
    messages = [
        SystemMessagePromptTemplate.from_template(system_template),
        HumanMessagePromptTemplate.from_template("{question}")
    ]
    prompt = ChatPromptTemplate.from_messages(messages)
    chain_type_kwargs = {"prompt": prompt}
    return chain_type_kwargs


def answer(query):
    load_key()
    # doc = load_doc('cucm_b_troubleshooting-guide-1251-extracted (1).pdf')
    presist_dict = './db'
    # vectorstore = create_chromadb(doc, presist_dict)
    vectorstore = retrive_db(presist_dict)
    chain = creating_chain(vectorstore, chain_msg())
    # query = "procedure to configure the Real-Time Monitoring Tool to email the administrator whenever a core dump occurs"
    result = chain(query)
    print(result['answer'])
    return result['answer']

# # demo message
# def demo(msg):
#     print(type(msg))
#     return "hello world \nmy name is janakiRAM"
# r = answer("procedure to Configuring Packet Capturing in the Phone Configuration Window")
# print("hello world \n my name is janakiRAM")
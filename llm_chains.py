from prompt_templates import memory_prompt_template
from langchain.chains import StuffDocumentsChain, LLMChain, ConversationalRetrievalChain
from langchain_community.embeddings import HuggingFaceInstructEmbeddings
from langchain.memory import ConversationBufferWindowMemory
from langchain.prompts import PromptTemplate
from langchain.llms import CTransformers
from langchain_community.vectorstores import Chroma
import chromadb
import yaml

with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

def create_llm(model_path = config["ctransformers"]["model_path"]["small"], model_type = config["ctransformers"]["model_type"], model_config = config["ctransformers"]["model_config"]):
    llm = CTransformers(model=model_path, model_type=model_type, config=model_config)
    return llm

def create_embeddings(embeddings_path = config["embeddings_path"]):
    model_kwargs = {'device': 'cpu'}
    encode_kwargs = {'normalize_embeddings': True}
    return HuggingFaceInstructEmbeddings(model_name=embeddings_path, model_kwargs=model_kwargs, encode_kwargs=encode_kwargs)

def create_llm_chain(llm, chat_prompt, memory):
    return LLMChain(llm=llm, prompt=chat_prompt, memory=memory)

def create_chat_memory(chat_history):
    return ConversationBufferWindowMemory(memory_key="history", chat_memory=chat_history, k=3)

def create_prompt_from_template(template):
    return PromptTemplate.from_template(template)

def load_normal_chain(chat_history):
    return chatChain(chat_history)

def load_vectordb(embeddings):
    persistent_client = chromadb.PersistentClient("chroma_db")
    #collection = persistent_client.get_or_create_collection("collection_name")
    #collection.add(ids=["1", "2", "3"], documents=["a", "b", "c"])

    langchain_chroma = Chroma(
        client=persistent_client,
        collection_name="col_pdfs",
        embedding_function=embeddings,
    )
    #print("There are", langchain_chroma._collection.count(), "in the collection")
    return langchain_chroma

class chatChain:

    def __init__(self, chat_history, model_path=config["ctransformers"]["model_path"]["small"], model_type=config["ctransformers"]["model_type"]):
        self.memory = create_chat_memory(chat_history)
        llm = create_llm()
        #llm = load_ollama_model()
        chat_prompt = create_prompt_from_template(memory_prompt_template)
        self.llm_chain = create_llm_chain(llm, chat_prompt, self.memory)

    def run(self, user_input):
        return self.llm_chain.run(human_input= user_input, history=self.memory.chat_memory.messages ,stop=["Human:"])
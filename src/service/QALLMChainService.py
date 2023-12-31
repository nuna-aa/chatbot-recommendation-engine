from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from service.ConfigurationParser import ConfigurationParser as cp

"""
Service to handle LLM chain processing using RetrivalQAChain
"""
class ChatModelService:

    def __init__(self, retrival_qa_prompt):
        configurations = cp().get_configuration_properties()
        self.__open_ai_api_key = configurations["openai"]["apiKey"]
        self.__open_ai_timeout = float(configurations["openai"]["timeout"])
        self.__open_ai_temperature = float(configurations["openai"]["temperature"])
        self.__open_ai_max_retry = int(configurations["openai"]["maxRetry"])
        self.__open_ai_model = configurations["openai"]["model"]
        self.__chain_type = configurations["chain"]["type"]
        self.__chat = ChatOpenAI(model_name=self.__open_ai_model, streaming=True,
                                 temperature=self.__open_ai_temperature,
                                 openai_api_key=self.__open_ai_api_key, request_timeout=self.__open_ai_timeout,
                                 max_retries=self.__open_ai_max_retry)
        self.__memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        self.__retrival_qa_prompt = retrival_qa_prompt

    """
    LLM generates response based on the question and vector store parameters
    """
    def retrieval_qa_chain(self, question, vector_store):
        chain = RetrievalQA.from_chain_type(
            llm=self.__chat, chain_type=self.__chain_type, retriever=vector_store.as_retriever(search_type="mmr"),
            chain_type_kwargs={"prompt": self.__retrival_qa_prompt}, verbose=True)

        result = chain.run(question)

        return result

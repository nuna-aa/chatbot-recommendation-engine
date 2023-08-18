from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from service.ConfigurationParser import ConfigurationParser as cp


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
        self.__response_exclude_word = "Here is a revised response:\n\nModel:"

    def get_chat_history(self):
        return self.__memory.buffer

    def clear_chat_history(self):
        return self.__memory.clear()

    def retrieval_qa_chain(self, vector_store, question):
        chain = RetrievalQA.from_chain_type(
            llm=self.__chat, chain_type=self.__chain_type, retriever=vector_store.as_retriever(search_type="mmr"),
            chain_type_kwargs={"prompt": self.__retrival_qa_prompt})

        result = chain.run(question)

        print(result)

        if self.__response_exclude_word in result:
            result = result.split(self.__response_exclude_word, 1)[1]

        return result

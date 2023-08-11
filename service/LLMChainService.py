from langchain import LLMChain
from langchain.chains.question_answering import load_qa_chain
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from service.ConfigurationParser import ConfigurationParser as cp


class ChatModelService:

    def __init__(self, documents, prompt):
        configurations = cp().get_configuration_properties()
        self.__open_ai_api_key = configurations["openai"]["apiKey"]
        self.__open_ai_timeout = configurations["openai"]["timeout"]
        self.__open_ai_temperature = configurations["openai"]["temperature"]
        self.__open_ai_max_retry = configurations["openai"]["maxRetry"]
        self.__open_ai_model = configurations["openai"]["model"]
        self.__chain_type = configurations["chain"]["type"]
        self.__chat = ChatOpenAI(model_name=self.__open_ai_model, streaming=True,
                                 temperature=self.__open_ai_temperature,
                                 openai_api_key=self.__open_ai_api_key, request_timeout=self.__open_ai_timeout,
                                 max_retries=self.__open_ai_max_retry)
        self.__memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        self.__question_generator = LLMChain(llm=self.__chat, prompt=prompt)
        self.__doc_chain = load_qa_chain(self.__chat, chain_type=self.__chain_type)
        self.__chain = ConversationalRetrievalChain(
            question_generator=self.__question_generator,
            retriever=documents.as_retriever(),
            memory=self.__memory,
            combine_docs_chain=self.__doc_chain,
            verbose=True
        )

    def user_input_chain(self, question):
        result = self.__chain({"question": question})

        print(result)

        response = result["answer"]

        return response

    def get_chat_history(self):
        return self.__memory.buffer

    def clear_chat_history(self):
        return self.__memory.clear()

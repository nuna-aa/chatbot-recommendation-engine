from langchain import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConstitutionalChain, RetrievalQA, SimpleSequentialChain

from service.EthicalPrinciples import EthicalPrinciples as ep

from service.ConfigurationParser import ConfigurationParser as cp


class ChatModelService:

    def __init__(self, retrival_qa_prompt, constitutional_prompt):
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
        self.__retrival_qa_prompt = retrival_qa_prompt
        self.__constitutional_prompt = constitutional_prompt
        self.__response_exclude_word = "Here is a revised response:\n\nModel:"

    def sequential_chain(self, vector_store, question):
        qa_chain = self.__retrieval_qa_chain(vector_store)
        constitutional_chain = self.__constitutional_chain()
        overall_chain = SimpleSequentialChain(chains=[qa_chain, constitutional_chain], verbose=True,
                                              input_key="question")

        result = overall_chain.run(question)

        print(result)

        if self.__response_exclude_word in result:
            result = result.split(self.__response_exclude_word, 1)[1]

        return result

    def get_chat_history(self):
        return self.__memory.buffer

    def clear_chat_history(self):
        return self.__memory.clear()

    def __constitutional_chain(self):
        qa_chain = LLMChain(llm=self.__chat, prompt=self.__constitutional_prompt)

        return ConstitutionalChain.from_llm(
            chain=qa_chain,
            constitutional_principles=ep.context_principles,
            llm= self.__chat,
            verbose=True)

    def __retrieval_qa_chain(self, vector_store):
        return RetrievalQA.from_chain_type(
            llm=self.__chat, chain_type=self.__chain_type, retriever=vector_store.as_retriever(),
            chain_type_kwargs={"prompt": self.__retrival_qa_prompt})
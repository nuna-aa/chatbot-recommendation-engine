from service.RetrievalQAPromptService import RetrievalQAPromptService as retrieval_qa_prompt
from service.QALLMChainService import ChatModelService as qms
from dto.UserMessage import UserMessage as um
from service.RecommendationService import RecommendationService as rs
from dto.ChatHistory import ChatHistory as ch


class ChatService:
    def __init__(self):
        self.__rs = rs()
        self.__retrival_qa_prompt = retrieval_qa_prompt().set_chat_message_prompt()
        self.__chain = qms(self.__retrival_qa_prompt)

    def recommend(self, user_message):
        documents = self.__rs.get_vector_collection()
        llm_response = self.__chain.retrieval_qa_chain(user_message, documents)
        return um(message=llm_response)

    def get_chat_history(self):
        response = self.__chain.get_chat_history()
        return ch(history=response)

    def clear_chat_history(self):
        self.__chain.clear_chat_history()

    def reload_datasources(self):
        return self.__rs.load_embed_store()

    def insert_one_datasource(self, file):
        return self.__rs.load_embed_store_one_file(file)

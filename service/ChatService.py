from service.PromptService import PromptService as ps
from service.LLMChainService import ChatModelService as cms
from dto.UserMessage import UserMessage as um
from service.RecommendationService import RecommendationService as rs
from dto.ChatHistory import ChatHistory as ch


class ChatService:
    def __init__(self):
        self.__documents = rs().load_embed_store()
        self.__prompt = ps().set_chat_message_prompt()
        self.__chain = cms(self.__documents, self.__prompt)

    def recommend(self, user_message):
        llm_response = self.__chain.user_input_chain(user_message)
        return um(message=llm_response)

    def get_chat_history(self):
        response = self.__chain.get_chat_history()
        return ch(history=response)

    def clear_chat_history(self):
        self.__chain.clear_chat_history()

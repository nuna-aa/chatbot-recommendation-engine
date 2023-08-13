from service.RetrivalQAPromptService import RetrievalQAPromptService as retrieval_qa_prompt
from service.ConstitutionalPromptService import ConstitutionalPromptService as constitutional_prompt
from service.LLMChainService import ChatModelService as cms
from dto.UserMessage import UserMessage as um
from service.RecommendationService import RecommendationService as rs
from dto.ChatHistory import ChatHistory as ch


class ChatService:
    def __init__(self):
        self.__rs = rs()
        self.__retrival_qa_prompt = retrieval_qa_prompt().set_chat_message_prompt()
        self.__constitutional_prompt = constitutional_prompt().set_chat_message_prompt()
        self.__chain = cms(self.__retrival_qa_prompt, self.__constitutional_prompt)

    def recommend(self, user_message):
        documents = self.__rs.get_vector_collection(user_message)
        llm_response = self.__chain.sequential_chain(documents, user_message)
        return um(message=llm_response)

    def get_chat_history(self):
        response = self.__chain.get_chat_history()
        return ch(history=response)

    def clear_chat_history(self):
        self.__chain.clear_chat_history()

    def reload_datasources(self):
        self.__rs.load_embed_store()

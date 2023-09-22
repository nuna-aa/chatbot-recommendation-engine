from service.RetrievalQAPromptService import RetrievalQAPromptService as retrieval_qa_prompt
from service.QALLMChainService import ChatModelService as qms
from dto.UserMessage import UserMessage as um
from service.RecommendationService import RecommendationService as rs

"""
Service to manage calls to LLM chain
"""
class ChatService:
    def __init__(self):
        self.__rs = rs()
        self.__retrival_qa_prompt = retrieval_qa_prompt().set_chat_message_prompt()
        self.__chain = qms(self.__retrival_qa_prompt)

    """
    Call LLM to process recommnedations
    """
    def recommend(self, user_message):
        documents = self.__rs.get_vector_collection()
        llm_response = self.__chain.retrieval_qa_chain(user_message, documents)
        return um(message=llm_response)

    """
    Refresh all embeddings in the vector store
    """
    def reload_datasources(self):
        return self.__rs.load_embed_store()

    """
    Insert one document in the vector store
    """
    def insert_one_datasource(self, file):
        return self.__rs.load_embed_store_one_file(file)

from langchain.embeddings import OpenAIEmbeddings
from service.ConfigurationParser import ConfigurationParser as cp
from repository.VectorStoreRepository import VectorStoreRepository as vsp


class TextEmbedderService:

    def __init__(self):
        configurations = cp().get_configuration_properties()
        self.__open_ai_api_key = configurations["openai"]["apiKey"]
        self.__embedding_model = OpenAIEmbeddings(openai_api_key=self.__open_ai_api_key)
        self.__vector_store_repository = vsp()

    def embed(self, tokens):
        return self.__vector_store_repository.store(tokens, self.__embedding_model)

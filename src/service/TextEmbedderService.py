from langchain.embeddings import OpenAIEmbeddings
from service.ConfigurationParser import ConfigurationParser as cp

"""
Service to handle embedding text chunks
"""
class TextEmbedderService:

    def __init__(self):
        configurations = cp().get_configuration_properties()
        self.__open_ai_api_key = configurations["openai"]["apiKey"]
        self.embedding_model = OpenAIEmbeddings(openai_api_key=self.__open_ai_api_key)

    """
    Return embedding model
    """
    def embed(self):
        return self.embedding_model

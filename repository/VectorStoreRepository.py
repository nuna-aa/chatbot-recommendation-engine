from langchain.vectorstores import Chroma
from service.ConfigurationParser import ConfigurationParser as cp
import os


class VectorStoreRepository:

    def __init__(self):
        configurations = cp().get_configuration_properties()
        self.__collection = configurations["chroma"]["collection"]
        self.__persistence_directory = configurations["chroma"]["directory"]
        root_directory = os.path.dirname(os.path.dirname(__file__))
        vector_path = os.path.join(root_directory, self.__persistence_directory)
        self.__vectorstore = Chroma(collection_name=self.__collection,
                                    persist_directory=vector_path)

    def store(self, tokens, embedding):
        return self.__vectorstore.from_documents(documents=tokens, embedding=embedding)

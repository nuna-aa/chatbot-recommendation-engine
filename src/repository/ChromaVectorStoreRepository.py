import chromadb
import uuid
from langchain.vectorstores import Chroma
from service.ConfigurationParser import ConfigurationParser as cp

"""
Repository to manage chroma vector database processing
"""
class ChromaVectorStoreRepository:

    def __init__(self, embedding_function):
        configurations = cp().get_configuration_properties()
        self.__collection_name = configurations["chroma"]["collection"]
        self.__persistence_host = configurations["chroma"]["host"]
        self.__persistence_port = configurations["chroma"]["port"]
        self.__index_name = configurations["chroma"]["index"]
        self.__embedding_function = embedding_function
        self.__chroma_http_client = chromadb.HttpClient(host=self.__persistence_host, port=self.__persistence_port)
        self.__collection = self.__chroma_http_client.get_or_create_collection(self.__collection_name,
                                                                               embedding_function=self.__embedding_function.embed_documents)

    """
    Save embeddings for one document
    """
    def store_one_doc(self, token):
        return self.__insert(token)

    """
    Retrieve embedding collection
    """
    def get_document_collection(self):
        return Chroma(
            client=self.__chroma_http_client, collection_name=self.__collection_name,
            embedding_function=self.__embedding_function)

    """
    Refresh embeddings in collection
    """
    def reload_store(self, tokens):
        self.__chroma_http_client.delete_collection(self.__collection_name)
        self.__collection = self.__chroma_http_client.create_collection(self.__collection_name,
                                                                 embedding_function=self.__embedding_function.embed_documents)
        return self.__insert(tokens)


    def __insert(self, tokens):
        uuids = []
        metadatas = []
        documents = []
        for doc in tokens:
            uuids.append(str(uuid.uuid1()))
            metadatas.append(doc.metadata)
            documents.append(doc.page_content)

        self.__collection.add(ids=uuids, metadatas=metadatas, documents=documents)
        return self.__collection.id

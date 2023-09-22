import pinecone
from langchain.vectorstores import Pinecone
from service.ConfigurationParser import ConfigurationParser as cp

"""
Repository to manage pinecone vector database processing
"""
class PineconeVectorStoreRepository:

    def __init__(self):
        configurations = cp().get_configuration_properties()
        self.__collection = configurations["pinecone"]["collection"]
        self.__persistence_key = configurations["pinecone"]["key"]
        self.__persistence_env = configurations["pinecone"]["env"]
        self.__index_name = configurations["pinecone"]["index"]

    """
    Save embeddings documents in the collection
    """
    def store(self, tokens, embedding):
        pinecone.init(
            api_key=self.__persistence_key,
            environment=self.__persistence_env)
        if self.__index_name not in pinecone.list_indexes():
            # we create a new index
            pinecone.create_index(
                name=self.__index_name,
                metric='cosine',
                dimension=1536
            )
        return self.reload_store(tokens, embedding)


    """
    Retrieve embedding collection
    """
    def get_document_collection(self, query, embeddings):
        pinecone.init(
            api_key=self.__persistence_key,
            environment=self.__persistence_env)
        index = pinecone.Index(self.__index_name)
        vectorstore = Pinecone(
            index, embeddings.embed_query, "text"
        )
        return vectorstore.as_retriever()

    """
    Refresh embeddings in collection
    """
    def reload_store(self, tokens, embedding):
        pinecone.init(
            api_key=self.__persistence_key,
            environment=self.__persistence_env)
        return Pinecone.from_documents(tokens, embedding, index_name=self.__index_name)

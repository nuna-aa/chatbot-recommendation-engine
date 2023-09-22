"""
Orchestrator service that handles the flow to generate recommendation message
"""
from service.S3DirectoryTextLoaderService import S3DirectoryTextLoaderService as dtls
from service.S3FileTextLoaderService import S3FileTextLoaderService as ftls
from service.TextSplitterService import TextSplitterService as tss
from service.TextEmbedderService import TextEmbedderService as tes
from repository.ChromaVectorStoreRepository import ChromaVectorStoreRepository as cvsp


class RecommendationService:

    """
    Initialise constructor
    """
    def __init__(self):
        self.__directory_text_loader = dtls()
        self.__file_text_loader = ftls()
        self.__text_splitter = tss()
        self.__text_embedder = tes().embed()
        self.__vector_store_repository = cvsp(self.__text_embedder)

    """
    Applies to all the documents in S3 Bucket
    Load files from S3 Bucket
    Split files into text chunks
    Convert to embeddings
    Store in vector database
    """
    def load_embed_store(self):
        datasource_documents = self.__directory_text_loader.load()
        tokens = self.__text_splitter.split(datasource_documents)
        return self.__vector_store_repository.reload_store(tokens)

    """
    Applies to only one document in S3 Bucket
    Load files from S3 Bucket
    Split files into text chunks
    Convert to embeddings
    Store in vector database
    """
    def load_embed_store_one_file(self, file_name):
        datasource_document = self.__file_text_loader.load_one(file_name)
        tokens = self.__text_splitter.split(datasource_document)
        return self.__vector_store_repository.store_one_doc(tokens)

    """
    Fetch the embeddings collection from vector database
    """
    def get_vector_collection(self):
        return self.__vector_store_repository.get_document_collection()

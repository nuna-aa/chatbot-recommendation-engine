from service.S3DirectoryTextLoaderService import S3DirectoryTextLoaderService as dtls
from service.S3FileTextLoaderService import S3FileTextLoaderService as ftls
from service.TextSplitterService import TextSplitterService as tss
from service.TextEmbedderService import TextEmbedderService as tes
from repository.ChromaVectorStoreRepository import ChromaVectorStoreRepository as cvsp


class RecommendationService:

    def __init__(self):
        self.__directory_text_loader = dtls()
        self.__file_text_loader = ftls()
        self.__text_splitter = tss()
        self.__text_embedder = tes().embed()
        self.__vector_store_repository = cvsp(self.__text_embedder)

    def load_embed_store(self):
        datasource_documents = self.__directory_text_loader.load()
        tokens = self.__text_splitter.split(datasource_documents)
        return self.__vector_store_repository.reload_store(tokens)

    async def load_embed_store_one_file(self, file_name):
        datasource_document = self.__file_text_loader.load_one(file_name)
        tokens = self.__text_splitter.split(datasource_document)
        return self.__vector_store_repository.store_one_doc(tokens)

    def get_vector_collection(self):
        return self.__vector_store_repository.get_document_collection()

from service.TextLoaderService import TextLoaderService as tls
from service.TextSplitterService import TextSplitterService as tss
from service.TextEmbedderService import TextEmbedderService as tes
from repository.VectorStoreRepository import VectorStoreRepository as vsp


class RecommendationService:

    def __init__(self):
        self.__text_loader = tls()
        self.__text_splitter = tss()
        self.__text_embedder = tes().embed()
        self.__vector_store_repository = vsp()

    def load_embed_store(self):
        datasource_documents = self.__text_loader.load()
        tokens = self.__text_splitter.split(datasource_documents)
        return self.__vector_store_repository.store(tokens, self.__text_embedder)

    def get_vector_collection(self, query):
        return self.__vector_store_repository.get_document_collection(query, self.__text_embedder)

from service.TextLoaderService import TextLoaderService as tls
from service.TextSplitterService import TextSplitterService as tss
from service.TextEmbedderService import TextEmbedderService as tes


class RecommendationService:

    def __init__(self):
        self.__text_loader = tls()
        self.__text_splitter = tss()
        self.__text_embedder = tes()

    def load_embed_store(self):
        documents = self.__text_loader.load()
        tokens = self.__text_splitter.split(documents)
        return self.__text_embedder.embed(tokens)

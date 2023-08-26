from langchain.document_loaders import DirectoryLoader
import os


class TextLoaderService:
    def __init__(self):
        self.__file_name = 'datasources'
        root_directory = os.path.dirname(os.path.dirname(__file__))
        config_path = os.path.join(root_directory, self.__file_name)
        text_loader_kwargs = {'autodetect_encoding': True}
        self.__loader = DirectoryLoader(path=config_path, glob="**/*.pdf", use_multithreading=True,
                                        loader_kwargs=text_loader_kwargs)

    def load(self):
        return self.__loader.load()

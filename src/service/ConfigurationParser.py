import yaml
import os
from pyaml_env import parse_config

"""
Class to read configurations from Configuration.yaml file
"""


class ConfigurationParser:
    """
    Class Initialization method to set the configuration properties variable
    by calling __set_configuration_properties()
    """

    def __init__(self):
        self.__file_name = 'configuration/properties.yaml'
        self.__configuration_properties = self.__set_configuration_properties()

    def __load_directory(self):
        root_directory = os.path.dirname(os.path.dirname(__file__))
        return os.path.join(root_directory,self.__file_name)

    """
    Accessor method to set the configuration properties by opening and reading the yaml file
    """

    def __set_configuration_properties(self):
        file = self.__load_directory()
        __configuration_properties = parse_config(file)
        return __configuration_properties

    """
    Accessor method to get the configuration properties 
    """

    def get_configuration_properties(self):
        return self.__configuration_properties

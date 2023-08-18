import yaml
import os

"""
Class to read configurations from Configuration.yaml file
"""


class ConfigurationParser:
    """
    Class Initialization method to set the configuration properties variable
    by calling __set_configuration_properties()
    """

    def __init__(self):
        self.__configuration_properties = self.__set_configuration_properties()
        self.__file_name = 'configuration/properties.yaml'

    def __load_directory(self):
        root_directory = os.path.dirname(os.path.dirname(__file__))
        return os.path.join(root_directory, 'configuration/properties.yaml')

    """
    Accessor method to set the configuration properties by opening and reading the yaml file
    """

    def __set_configuration_properties(self):
        file = self.__load_directory()
        with open(file, "r") as yaml_config_file:
            __configuration_properties = yaml.safe_load(yaml_config_file)
            return __configuration_properties

    """
    Accessor method to get the configuration properties 
    """

    def get_configuration_properties(self):
        return self.__configuration_properties

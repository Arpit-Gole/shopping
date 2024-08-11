"""
Enumeration of the different run modes supported by the application.
"""


from enum import Enum, unique


@unique
class RunModes(Enum):
    DEBUG = 0
    PROD = 1

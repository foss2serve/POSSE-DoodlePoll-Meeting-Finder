import abc
from typing import List

from system import Component


class System:
    def __init__(self, components: List[Component]):
        pass

    def run(self):
        pass


class Component:
    __metaclass__ = abc.ABCMeta

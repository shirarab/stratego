import abc
from typing import Set

from soldier import Soldier
from stratego_graphic import StrategoGraphic


class InitAgent(object):
    @abc.abstractmethod
    def get_initial_positions(self, soldiers: Set[Soldier], graphic: StrategoGraphic):
        return

from dataclasses import dataclass

from model.artObject import ArtObject


@dataclass
class Arco:
    nodo1: ArtObject
    nodo2: ArtObject
    peso: int
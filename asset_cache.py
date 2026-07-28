import os

import pygame

from piece import Piece


class AssetCache:
    """Lazy cache for pygame surfaces keyed by asset path."""

    def __init__(self) -> None:
        self._images: dict[str, pygame.Surface] = {}

    def image(self, path: str) -> pygame.Surface:
        if path not in self._images:
            self._images[path] = pygame.image.load(path).convert_alpha()
        return self._images[path]


asset_cache = AssetCache()


def piece_texture_path(piece: Piece, size: int) -> str:
    return os.path.join(
        "assets",
        "images",
        f"{size}px",
        f"{piece.color}_{piece.name}_{size}.png",
    )

import os

import pygame


class AssetCache:
    """Lazy cache for pygame surfaces keyed by asset path."""

    def __init__(self):
        self._images = {}

    def image(self, path):
        if path not in self._images:
            self._images[path] = pygame.image.load(path).convert_alpha()
        return self._images[path]


asset_cache = AssetCache()


def piece_texture_path(piece, size):
    return os.path.join(
        "assets",
        "images",
        f"{size}px",
        f"{piece.color}_{piece.name}_{size}.png",
    )

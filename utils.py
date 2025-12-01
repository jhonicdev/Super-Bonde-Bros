# utils.py
import pygame as pg

def scale_proporcional(imagem, max_largura, max_altura):
    """
    Redimensiona uma imagem mantendo a proporção, cabendo dentro de max_largura x max_altura.
    """
    orig_w, orig_h = imagem.get_size()
    scale = min(max_largura / orig_w, max_altura / orig_h)
    nova_w = int(orig_w * scale)
    nova_h = int(orig_h * scale)
    return pg.transform.scale(imagem, (nova_w, nova_h))


def carregar_sprite(path, max_largura, max_altura):
    """Carrega um sprite e o redimensiona proporcionalmente."""
    sprite = pg.image.load(path).convert_alpha()
    return scale_proporcional(sprite, max_largura, max_altura)
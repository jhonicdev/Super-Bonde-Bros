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


class IndicadorDano:
    """
    Uma classe para exibir um número de dano que sobe e desaparece.
    """
    def __init__(self, x, y, dano):
        self.pos = [x, y]
        self.texto = f"-{dano}"
        self.fonte = pg.font.SysFont("Courier New", 20, bold=True)
        self.cor = (255, 60, 60) # Vermelho vivo
        
        self.duracao_total = 60  # Duração em frames (1 segundo a 60FPS)
        self.duracao_restante = self.duracao_total
        self.velocidade_y = -1.5 # Velocidade com que o texto sobe

    def atualizar(self):
        """Atualiza a posição e a transparência do indicador."""
        self.pos[1] += self.velocidade_y
        self.duracao_restante -= 1

    def desenhar(self, janela, offset_x):
        """Desenha o texto de dano com efeito de fade-out."""
        if self.duracao_restante > 0:
            # Calcula a transparência (alpha) baseada no tempo restante
            alpha = 255 * (self.duracao_restante / self.duracao_total)
            texto_surf = self.fonte.render(self.texto, True, self.cor)
            texto_surf.set_alpha(alpha)
            janela.blit(texto_surf, (self.pos[0] - offset_x, self.pos[1]))


def carregar_sprite(path, max_largura, max_altura):
    """Carrega um sprite e o redimensiona proporcionalmente."""
    sprite = pg.image.load(path).convert_alpha()
    return scale_proporcional(sprite, max_largura, max_altura)
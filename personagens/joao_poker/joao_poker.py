import pygame as pg
from personagem_base import PersonagemBase
from utils import scale_proporcional
# from .joao_poker_habilidades import * # Futuras habilidades serão importadas aqui

class JoaoPoker(PersonagemBase):
    def __init__(self, x, y):
        super().__init__(x, y, velocidade=2.2, forca_pulo=-22, vida_max=2800)

        # --- Sprites e Animações (usando placeholder) ---
        sprite_placeholder = scale_proporcional(
            pg.image.load('personagens/joao_poker/sprites/idle/slendytubbie.png').convert_alpha(),
            max_largura=100, max_altura=64 # Redimensiona mantendo a proporção
        )
        self.animacoes["idle_direita"] = [sprite_placeholder]
        self.animacoes["idle_esquerda"] = [pg.transform.flip(img, True, False) for img in self.animacoes["idle_direita"]]
        self.animacoes["run_direita"] = [sprite_placeholder]
        self.animacoes["run_esquerda"] = [pg.transform.flip(img, True, False) for img in self.animacoes["run_direita"]]

        # --- Ícone para menu ---
        self.menu_icon = scale_proporcional(self.animacoes["idle_direita"][0], 150, 90)

        # --- Atributos específicos ---
        self.name = "João Poker"
        self.cooldowns_habilidades = [0] * 3

        # --- Colisor (baseado no placeholder) ---
        largura, altura = self.animacoes["idle_direita"][0].get_size()
        self.colisor = [int(largura * 0.8), int(altura * 0.9)]
        self.colisor_offset = [int(largura * 0.1), int(altura * 0.1)]

        # --- Ícones de Habilidades (placeholders) ---
        self.skill_icons = [pg.Surface((70, 70)) for _ in range(3)] # Ícones pretos vazios
        for icon in self.skill_icons:
            icon.fill((20, 20, 20))
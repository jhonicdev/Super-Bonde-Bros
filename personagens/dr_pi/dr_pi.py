import pygame as pg
from personagem_base import PersonagemBase
from utils import scale_proporcional
from config_jogo import CONFIG

# from .dr_pi_habilidades import * # Futuras habilidades serão importadas aqui

class DrPI(PersonagemBase):
    def __init__(self, x, y):
        config = CONFIG['personagens']['DrPI']
        super().__init__(x, y, velocidade=config['velocidade'], forca_pulo=config['forca_pulo'], vida_max=config['vida_max'])

        # --- Sprites e Animações (usando placeholder) ---
        sprite_placeholder = scale_proporcional(
            pg.image.load('personagens/dr_pi/sprites/idle/dilma.png').convert_alpha(),
            max_largura=128, max_altura=80 # Redimensiona mantendo a proporção
        )
        self.animacoes["idle_esquerda"] = [pg.transform.scale(pg.image.load(f'./personagens/dr_pi/sprites/idle/Idle {i}.png'), (128, 80)) for i in range(1,6)]
        self.animacoes["idle_direita"] = [pg.transform.flip(img, True, False) for img in self.animacoes["idle_esquerda"]]
        self.animacoes["run_esquerda"] = [pg.transform.scale(pg.image.load(f'./personagens/dr_pi/sprites/run/Run {i}.png'), (128, 80)) for i in range(1,7)]
        self.animacoes["run_direita"] = [pg.transform.flip(img, True, False) for img in self.animacoes["run_esquerda"]]

        # --- Ícone para menu ---
        self.menu_icon = scale_proporcional(self.animacoes["idle_direita"][0], 192, 120)

        # --- Atributos específicos ---
        self.name = "Dr. PI"
        self.cooldowns_habilidades = [0] * 3

        # --- Colisor ---
        largura, altura = self.animacoes["idle_direita"][0].get_size()
        self.colisor = [int(largura * 0.2), int(altura * 0.6)]
        self.colisor_offset = [int(largura * 0.4), int(altura * 0.2)]

        # --- Ícones de Habilidades (placeholders) ---
        self.skill_icons = [pg.Surface((70, 70)) for _ in range(3)] # Ícones pretos vazios
        for icon in self.skill_icons:
            icon.fill((20, 20, 20))
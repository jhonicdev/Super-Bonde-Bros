import pygame as pg
from vilao_base import VilaoBase
from config_jogo import CONFIG

class CarangueijoPirata(VilaoBase):
    def __init__(self, x, y):
        # Configurações específicas deste vilão
        config = CONFIG['viloes'].get('CarangueijoPirata', {})
        super().__init__(x=x, y=y, velocidade=config['velocidade'], vida_max=config['vida_max'], forca_pulo=config['forca_pulo'])

        # --- Sprites ---
        # Usaremos um emoji como placeholder por enquanto
        self.fonte_emoji = pg.font.SysFont("Segoe UI Emoji", 50)
        self.sprite_direita = self.fonte_emoji.render("🦀", True, (200, 50, 50))
        self.sprite_esquerda = pg.transform.flip(self.sprite_direita, True, False)

        # Define as animações na classe base para que o método desenhar() funcione
        self.animacoes["run_direita"] = [self.sprite_direita]
        self.animacoes["run_esquerda"] = [self.sprite_esquerda]
        self.animacoes["idle_direita"] = [self.sprite_direita]
        self.animacoes["idle_esquerda"] = [self.sprite_esquerda]

        # --- Colisor ---
        largura, altura = self.sprite_direita.get_size()
        self.colisor = [int(largura * 0.8), int(altura * 0.8)]
        self.colisor_offset = [int(largura * 0.1), int(altura * 0.2)]
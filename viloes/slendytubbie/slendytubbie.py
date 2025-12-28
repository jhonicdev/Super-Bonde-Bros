import pygame as pg
from vilao_base import VilaoBase
from config_jogo import CONFIG
from utils import scale_proporcional

class Slendytubbie(VilaoBase):
    som_ataque = None

    def __init__(self, x, y):
        # Configurações específicas deste vilão
        config = CONFIG['viloes'].get('Slendytubbie', {})
        
        # Slendytubbie herda de VilaoBase (terrestre)
        # Assume-se que ele anda no chão, então usa gravidade padrão da base (não passamos gravidade=0)
        super().__init__(
            x=x, 
            y=y, 
            velocidade=config.get('velocidade', 2.5), 
            vida_max=config.get('vida_max', 1200), 
            forca_pulo=config.get('forca_pulo', -15)
        )

        # --- Sprites ---
        # Carrega a imagem do sprite. 
        # Caminho assumido: ./viloes/slendytubbie/sprites/slendytubbie.png
        try:
            img_original = pg.image.load('./viloes/slendytubbie/sprites/slendytubbie.png').convert_alpha()
        except (FileNotFoundError, pg.error):
            print("AVISO: Sprite do Slendytubbie não encontrado. Usando placeholder.")
            img_original = pg.Surface((60, 100))
            img_original.fill((100, 50, 100)) # Roxo escuro

        # Redimensiona para um tamanho padrão de vilão grande (ajuste conforme necessário)
        self.sprite_direita = scale_proporcional(img_original, 64, 64)
        self.sprite_esquerda = pg.transform.flip(self.sprite_direita, True, False)

        # Define as animações
        # Como é um sprite único, usamos o mesmo para idle e run
        self.animacoes["idle_direita"] = [self.sprite_direita]
        self.animacoes["idle_esquerda"] = [self.sprite_esquerda]
        self.animacoes["run_direita"] = [self.sprite_direita]
        self.animacoes["run_esquerda"] = [self.sprite_esquerda]

        # --- Colisor ---
        largura, altura = self.sprite_direita.get_size()
        self.colisor = [int(largura * 0.6), int(altura * 0.9)]
        self.colisor_offset = [int(largura * 0.2), int(altura * 0.1)]

        # --- Som ---
        if Slendytubbie.som_ataque is None:
            try:
                Slendytubbie.som_ataque = pg.mixer.Sound('./viloes/slendytubbie/sound/attack.mp3')
            except (FileNotFoundError, pg.error):
                pass

    def som(self):
        if Slendytubbie.som_ataque is not None:
            Slendytubbie.som_ataque.play()
    
    # Não sobrescrevemos 'atualizar' pois a lógica padrão de VilaoBase (andar e perseguir no chão) serve bem.

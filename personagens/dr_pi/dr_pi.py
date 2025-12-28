import pygame as pg
from personagem_base import PersonagemBase
from utils import scale_proporcional
from config_jogo import CONFIG

from .dr_pi_habilidades import Trigonometricamente, ProjetilPi, ProtecaoObmepica

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
        self.cooldowns_habilidades = [0] * 3 # 3 slots de habilidade ativa

        # --- Colisor ---
        largura, altura = self.animacoes["idle_direita"][0].get_size()
        self.colisor = [int(largura * 0.2), int(altura * 0.6)]
        self.colisor_offset = [int(largura * 0.4), int(altura * 0.2)]

        # --- Habilidades ---
        self.hab_trigonometria = Trigonometricamente()
        self.hab_obmep = ProtecaoObmepica()

        # --- Ícones de Habilidades (placeholders) ---
        font_icon = pg.font.SysFont("Segoe UI Emoji", 45)
        font_pi = pg.font.SysFont("Times New Roman", 50, bold=True) # Fonte matemática para o Pi
        
        # Carrega ícone da OBMEP para o HUD
        try:
            img_obmep = pg.image.load('./personagens/dr_pi/sprites/abilities/obmep.png').convert_alpha()
            
            # Recorta apenas a área visível (remove bordas transparentes)
            rect_visivel = img_obmep.get_bounding_rect()
            img_obmep = img_obmep.subsurface(rect_visivel).copy()
            
            img_obmep = scale_proporcional(img_obmep, 50, 50)
        except Exception:
            img_obmep = font_icon.render("📚", True, (255, 255, 255))
            
        self.skill_icons = [
            font_pi.render("π", True, (255, 255, 255)), # Pi-raio (Ataque Básico)
            font_icon.render("📈", True, (255, 255, 255)), # Trigonometria
            img_obmep, # OBMEP
        ]

    def iniciar_habilidade(self, index):
        # Verifica cooldown global da classe base
        if index < len(self.cooldowns_habilidades) and self.cooldowns_habilidades[index] == 0:
            
            # Habilidade 1: Pi-raio / Ataque Básico (Índice 0)
            if index == 0:
                direcao = 1 if "direita" in self.estado_animacao else -1
                # Lança do centro do personagem
                x, y = self.get_colisor().center
                
                projetil = ProjetilPi(x, y, direcao, self)
                self.habilidades_ativas.append(projetil)
                
                cd_segundos = CONFIG['personagens']['DrPI']['habilidades']['AtaqueBasico']['cooldown_s']
                self.cooldowns_habilidades[index] = int(cd_segundos * 60)

            # Habilidade 2: Trigonometria (Índice 1)
            elif index == 1:
                self.hab_trigonometria.start(self)
                self.habilidades_ativas.append(self.hab_trigonometria)
                
                # Define o cooldown baseado na config
                cd_segundos = CONFIG['personagens']['DrPI']['habilidades']['Trigonometria']['cooldown_s']
                self.cooldowns_habilidades[index] = int(cd_segundos * 60)
            
            # Habilidade 3: OBMEP (Índice 2)
            elif index == 2:
                self.hab_obmep.start(self)
                self.habilidades_ativas.append(self.hab_obmep)
                cd_segundos = CONFIG['personagens']['DrPI']['habilidades']['ProtecaoObmepica']['cooldown_s']
                self.cooldowns_habilidades[index] = int(cd_segundos * 60)
import pygame as pg
from personagem_base import PersonagemBase
from config_jogo import CONFIG
from utils import scale_proporcional, IndicadorDano
from .capitao_clown_nose_habilidades import SacoDeMoedas, LapadaSeca, TripulanteFantasma

import random

class CapitaoClownNose(PersonagemBase):
    vozes_kill = [
        pg.mixer.Sound(f'./personagens/capitao_clown_nose/sound/voices/kill_{i}.wav')
        for i in range(1) 
    ]
    vozes_hurt = [
        pg.mixer.Sound(f'./personagens/capitao_clown_nose/sound/voices/hurt_{i}.wav')
        for i in range(1) 
    ]
    vozes_hab1 = [
        pg.mixer.Sound(f'./personagens/capitao_clown_nose/sound/voices/hab1_{i}.wav')
        for i in range(1) 
    ]
    vozes_hab2 = [
        pg.mixer.Sound(f'./personagens/capitao_clown_nose/sound/voices/hab2_{i}.wav')
        for i in range(2) 
    ]
    vozes_hab3 = [
        pg.mixer.Sound(f'./personagens/capitao_clown_nose/sound/voices/hab3_{i}.wav')
        for i in range(1) 
    ]

    def __init__(self, x, y):
        # --- Lendo valores do arquivo de configuração ---
        config = CONFIG['personagens']['CapitaoClownNose']
        super().__init__(x, y, velocidade=config['velocidade'], forca_pulo=config['forca_pulo'], vida_max=config['vida_max'])

        # --- Canal de áudio dedicado para as vozes ---
        self.canal_voz = pg.mixer.Channel(0) # Usaremos o canal 0 para as vozes do capitão
        
        # --- Carrega animações ---
        self.animacoes["idle_direita"] = [pg.transform.scale(pg.image.load(f'./personagens/capitao_clown_nose/sprites/idle/Idle {i}.png'), (128, 80)) for i in range(1,6)]
        self.animacoes["idle_esquerda"] = [pg.transform.flip(img, True, False) for img in self.animacoes["idle_direita"]]
        self.animacoes["run_direita"] = [pg.transform.scale(pg.image.load(f'./personagens/capitao_clown_nose/sprites/run/Run {i}.png'), (128, 80)) for i in range(1,7)]
        self.animacoes["run_esquerda"] = [pg.transform.flip(img, True, False) for img in self.animacoes["run_direita"]]

        # --- Ícone para menu ---
        self.menu_icon = pg.transform.scale(self.animacoes["idle_direita"][0], (150, 90))  # primeira imagem do idle

        # --- Habilidades / especificidades ---
        self.name = "Clown Nose"

        largura, altura = self.animacoes["idle_direita"][0].get_size()
        self.colisor = [int(largura * 0.36), int(altura * 0.675)]
        self.colisor_offset = [int(largura * 0.32), int(altura * 0.12)]

        # Inicializa os cooldowns com base no número de habilidades
        self.cooldowns_habilidades = [0] * 3 # Este personagem tem 3 habilidades

        # Pré-carrega os recursos das habilidades para evitar lag
        SacoDeMoedas.carregar_recursos()

        # Carrega os ícones das habilidades para o HUD
        icon_size = 70
        self.skill_icons = [
            scale_proporcional(pg.font.SysFont("Segoe UI Emoji", 60).render("💰", True, (200, 200, 220)).convert_alpha(), icon_size, icon_size),
            scale_proporcional(pg.font.SysFont("Segoe UI Emoji", 60).render("⚓", True, (200, 200, 220)).convert_alpha(), icon_size, icon_size),
            scale_proporcional(pg.font.SysFont("Segoe UI Emoji", 60).render("👻", True, (200, 200, 220)).convert_alpha(), icon_size, icon_size)
        ]

    def iniciar_habilidade(self, index):
        # Habilidade 1: Saco de Moedas (índice 0)
        if index == 0 and self.cooldowns_habilidades[0] == 0:
            if random.random() < 0.03: # 3% de chance de tocar a voz
                random.choice(self.vozes_hab1).play() # SOM DA HABILIDADE 1

            # Define a direção baseada no estado da animação
            direcao = 1 if "direita" in self.estado_animacao else -1
            
            # Posição inicial do projétil (centro do personagem)
            pos_x, pos_y = self.get_colisor().center

            # Cria e adiciona o projétil à lista
            novo_projetil = SacoDeMoedas(pos_x, pos_y, direcao, self)
            self.habilidades_ativas.append(novo_projetil)

            # Define o COOLDOWN
            cooldown_s = CONFIG['personagens']['CapitaoClownNose']['habilidades']['SacoDeMoedas']['cooldown_s']
            self.cooldowns_habilidades[0] = cooldown_s * 60

        # Habilidade 2: Lapada Seca (índice 1)
        elif index == 1 and self.cooldowns_habilidades[1] == 0:
            random.choice(self.vozes_hab2).play() # SOM DA HABILIDADE 2

            direcao = 1 if "direita" in self.estado_animacao else -1
            pos_x, pos_y = self.get_colisor().center

            # Cria e adiciona a âncora à lista
            nova_ancora = LapadaSeca(pos_x, pos_y, direcao, self)
            self.habilidades_ativas.append(nova_ancora)

            # Define o COOLDOWN
            cooldown_s = CONFIG['personagens']['CapitaoClownNose']['habilidades']['LapadaSeca']['cooldown_s']
            self.cooldowns_habilidades[1] = cooldown_s * 60

        # Habilidade 3: Tripulação Fantasma (índice 2)
        elif index == 2 and self.cooldowns_habilidades[2] == 0:
            random.choice(self.vozes_hab3).play() # SOM DA HABILIDADE 3

            direcao = 1 if "direita" in self.estado_animacao else -1
            pos_x, pos_y = self.get_colisor().center

            novo_fantasma = TripulanteFantasma(pos_x, pos_y, direcao, self)
            self.habilidades_ativas.append(novo_fantasma)

            cooldown_s = CONFIG['personagens']['CapitaoClownNose']['habilidades']['TripulanteFantasma']['cooldown_s']
            self.cooldowns_habilidades[2] = cooldown_s * 60

    def atualizar_habilidades(self, mapa_tiles, viloes=[], camera_x=0):
        # Chama o método da classe base para gerenciar cooldowns
        super().atualizar_habilidades(mapa_tiles, viloes, camera_x)

    
    def receber_dano(self, quantidade):
        # Lógica específica do Capitão: tocar som de dor
        # O método da classe base cuidará de criar o indicador de dano e reduzir a vida.
        if not self.canal_voz.get_busy():
            if random.random() < 0.2: # 20% de chance de tocar a voz
                som_a_tocar = random.choice(self.vozes_hurt)
                self.canal_voz.play(som_a_tocar) # Toca no canal dedicado
        return super().receber_dano(quantidade)
    

    def som_kill(self):
        # Só toca o som de kill se o canal de voz estiver livre
        if not self.canal_voz.get_busy():
            if random.random() < 0.2: # 20% de chance de tocar a voz
                som_a_tocar = random.choice(self.vozes_kill)
                self.canal_voz.play(som_a_tocar) # Toca no canal dedicado

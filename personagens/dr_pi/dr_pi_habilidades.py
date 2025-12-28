import pygame as pg
import math
import random
from config_jogo import CONFIG
from mapa import TILE_SIZE

class EfeitoImpactoPi:
    def __init__(self, x, y):
        self.particulas = []
        self.tempo_vida = 45
        font = pg.font.SysFont("Times New Roman", 20, bold=True)
        
        # Elementos que vão voar: dígitos de Pi e símbolos
        elementos = ["3", ".", "1", "4", "1", "5", "9", "π", "∫"]
        
        for elem in elementos:
            px = x + random.randint(-10, 10)
            py = y + random.randint(-10, 10)
            vx = random.uniform(-4, 4)
            vy = random.uniform(-5, -2)
            cor = (255, 215, 0) if random.random() > 0.5 else (0, 255, 255)
            
            surf = font.render(elem, True, cor)
            surf_borda = font.render(elem, True, (0,0,0))
            
            self.particulas.append({
                'x': px, 'y': py, 'vx': vx, 'vy': vy,
                'surf': surf, 'surf_borda': surf_borda
            })

    def update(self, **kwargs):
        self.tempo_vida -= 1
        for p in self.particulas:
            p['x'] += p['vx']
            p['y'] += p['vy']
            p['vy'] += 0.2 # Gravidade
            p['vx'] *= 0.95 # Resistência do ar

    def draw(self, window, camera_x):
        if self.tempo_vida <= 0: return
        alpha = int(255 * (self.tempo_vida / 45))
        for p in self.particulas:
            p['surf_borda'].set_alpha(alpha)
            window.blit(p['surf_borda'], (p['x'] - camera_x + 1, p['y'] + 1))
            p['surf'].set_alpha(alpha)
            window.blit(p['surf'], (p['x'] - camera_x, p['y']))

    @property
    def ativo(self):
        return self.tempo_vida > 0

class EfeitoTrig:
    def __init__(self, x, y):
        self.particulas = []
        self.tempo_vida = 60
        font = pg.font.SysFont("Times New Roman", 18, bold=True)
        
        elem = "y = sen(x)"
        surf = font.render(elem, True, (0, 255, 255))
        surf_borda = font.render(elem, True, (0, 0, 50))
        
        self.particulas.append({
            'x': x - surf.get_width() // 2, 
            'y': y - 20, 
            'vx': 0, 
            'vy': 0,
            'surf': surf, 
            'surf_borda': surf_borda
        })

    def update(self, **kwargs):
        self.tempo_vida -= 1
        for p in self.particulas:
            p['x'] += p['vx']
            p['y'] += p['vy']

    def draw(self, window, camera_x):
        if self.tempo_vida <= 0: return
        alpha = int(255 * (self.tempo_vida / 60))
        for p in self.particulas:
            p['surf_borda'].set_alpha(alpha)
            window.blit(p['surf_borda'], (p['x'] - camera_x + 1, p['y'] + 1))
            p['surf'].set_alpha(alpha)
            window.blit(p['surf'], (p['x'] - camera_x, p['y']))
    
    @property
    def ativo(self):
        return self.tempo_vida > 0

class ProjetilPi:
    def __init__(self, x, y, direcao, jogador):
        self.jogador = jogador
        config = CONFIG['personagens']['DrPI']['habilidades']['AtaqueBasico']
        self.dano = config['dano']
        
        # --- Lógica da Passiva: Crítico, mas irracional ---
        # 3.14% de chance de causar 3.14x o dano
        self.eh_critico = False
        if random.random() < 0.0314:
            self.dano *= 3.14
            self.eh_critico = True

        # Física
        self.vel_x = config['velocidade_x'] * direcao
        self.vel_y = config['velocidade_y']
        self.gravidade = config['gravidade']
        
        # Visual (Renderiza o símbolo Pi)
        # Ajuste visual: Tamanho maior, cores vibrantes e contorno preto
        tamanho = 60 if self.eh_critico else 45
        self.cor_principal = (255, 215, 0) if self.eh_critico else (0, 255, 255) # Amarelo (Crítico) ou Ciano (Normal)
        
        self.font = pg.font.SysFont("Times New Roman", tamanho, bold=True)
        surf_texto = self.font.render("π", True, self.cor_principal)
        surf_borda = self.font.render("π", True, (0, 0, 0))
        
        # Cria superfície composta para aplicar o contorno
        w, h = surf_texto.get_size()
        self.imagem = pg.Surface((w + 4, h + 4), pg.SRCALPHA)
        
        # Desenha o contorno preto em várias direções
        for ox, oy in [(-1,0), (1,0), (0,-1), (0,1), (-1,-1), (1,1), (-1,1), (1,-1)]:
            self.imagem.blit(surf_borda, (2 + ox, 2 + oy))
        self.imagem.blit(surf_texto, (2, 2))
        
        self.rect = self.imagem.get_rect(center=(x, y))
        
        self.ativo = True
        self.tempo_vida = 180 # 3 segundos em frames

    def update(self, mapa_tiles, **kwargs):
        # Aplica gravidade e movimento
        self.vel_y += self.gravidade
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        
        self.tempo_vida -= 1
        if self.tempo_vida <= 0:
            self.ativo = False

        # Colisão com o mapa (paredes/chão)
        tile_x = int(self.rect.centerx / TILE_SIZE)
        tile_y = int(self.rect.centery / TILE_SIZE)
        
        # Verifica se bateu em algo sólido
        if 0 <= tile_y < len(mapa_tiles) and 0 <= tile_x < len(mapa_tiles[0]):
            if mapa_tiles[tile_y][tile_x] != ' ':
                self.ativo = False
                self.criar_efeito()
        elif tile_y >= len(mapa_tiles): # Caiu do mapa
            self.ativo = False

    def criar_efeito(self):
        efeito = EfeitoImpactoPi(self.rect.centerx, self.rect.centery)
        self.jogador.habilidades_ativas.append(efeito)

    def acertou_alvo(self, alvo):
        """Chamado quando acerta um inimigo"""
        alvo.receber_dano(self.dano)
        self.ativo = False # Destrói o projétil
        self.criar_efeito()

    def draw(self, window, camera_x):
        window.blit(self.imagem, (self.rect.x - camera_x, self.rect.y))

class Trigonometricamente:
    def __init__(self):
        self.nome = "Trigonometria"
        self.ativo = False
        
        # Carrega configurações
        dados = CONFIG['personagens']['DrPI']['habilidades']['Trigonometria']
        self.dano = dados['dano']
        self.duracao_max = int(dados['duracao_s'] * 60) # Converte para frames
        self.amplitude = dados['amplitude_pulo']
        self.freq_onda = dados['frequencia_onda']
        self.raio_ataque = dados['raio_ataque']
        self.fade_in_frames = int(dados.get('fade_in_s', 0.2) * 60)
        self.fade_out_frames = int(dados.get('fade_out_s', 0.2) * 60)
        
        self.timer = 0
        # Rect necessário para sistema genérico, mas usaremos lógica de área customizada
        self.rect = pg.Rect(0, 0, 0, 0) 
        self.inimigos_atingidos = []
        self.y_inicial = 0
        self.x_inicial = 0
        self.subida_interrompida = False

    def start(self, jogador):
        self.ativo = True
        self.timer = 0
        self.inimigos_atingidos = []
        self.jogador_ref = jogador
        self.subida_interrompida = False
        
        # Zera velocidade atual para iniciar o movimento controlado
        jogador.vel_vertical = 0
        jogador.no_chao = False
        
        # Registra a posição de onde o pulo partiu para fixar os efeitos visuais
        self.y_inicial = jogador.get_colisor().bottom
        self.x_inicial = jogador.get_colisor().centerx

    def update(self, mapa_tiles, viloes, jogador):
        if not self.ativo:
            return

        self.timer += 1

        # Calcula progresso (0.0 a 1.0)
        progresso = self.timer / self.duracao_max

        # --- Controle de Interrupção (Teto) ---
        # Se bater no teto durante a subida, libera o controle e a física
        if self.timer > 5 and progresso < 0.5 and jogador.vel_vertical == 0:
            self.subida_interrompida = True

        # --- Física do Cosseno ---
        angulo = progresso * math.pi 
        
        # Define a velocidade vertical manualmente se não foi interrompido
        if not self.subida_interrompida:
            jogador.vel_vertical = -self.amplitude * math.cos(angulo)

        # --- Bloqueio Horizontal ---
        # Impede movimento horizontal durante a subida (até o pico ou interrupção)
        if progresso < 0.5 and not self.subida_interrompida:
            diff = self.x_inicial - jogador.get_colisor().centerx
            jogador.pos[0] += diff

        # --- Dano em Área (Função Seno) ---
        # Verifica dano continuamente enquanto a onda está visível (entre 10% e 80% do pulo)
        if self.timer > self.fade_in_frames and self.timer < self.duracao_max - self.fade_out_frames:
            centro_x = jogador.get_colisor().centerx
            for vilao in viloes:
                if vilao.esta_vivo and vilao not in self.inimigos_atingidos:
                    dist = abs(vilao.get_colisor().centerx - centro_x)
                    if dist <= self.raio_ataque:
                        # Verifica colisão vertical com a onda
                        vilao_rect = vilao.get_colisor()
                        y_onda = self.y_inicial + 80 * math.sin(self.freq_onda * vilao_rect.centerx + self.timer * 0.2)
                        
                        # Margem de acerto (espessura da onda)
                        margem = 50
                        if vilao_rect.top - margem <= y_onda <= vilao_rect.bottom + margem:
                            vilao.receber_dano(self.dano)
                            self.inimigos_atingidos.append(vilao)
                            jogador.habilidades_ativas.append(EfeitoTrig(vilao.get_colisor().centerx, vilao.get_colisor().centery))

        # Encerra habilidade
        if self.timer >= self.duracao_max:
            self.ativo = False
            jogador.vel_vertical = 0 # Zera ao pousar para evitar dano de queda

    def draw(self, window, camera_x):
        if not self.ativo:
            return

        progresso = self.timer / self.duracao_max
        
        # Cria superfície temporária para transparência (Alpha)
        surf_efeitos = pg.Surface((1280, 768), pg.SRCALPHA)

        # --- Fade In / Fade Out Unificado ---
        alpha = 0
        if self.timer < self.fade_in_frames:
            alpha = (self.timer / self.fade_in_frames) * 255
        elif self.timer > self.duracao_max - self.fade_out_frames:
            tempo_restante = self.duracao_max - self.timer
            alpha = (tempo_restante / self.fade_out_frames) * 255
        else:
            alpha = 255
        alpha = max(0, min(255, int(alpha)))
        
        if alpha > 0:
            # --- 1. Visual da Onda Cosseno (Vertical) ---
            y_atual = self.jogador_ref.get_colisor().bottom
            if abs(self.y_inicial - y_atual) > 5:
                pontos_v = []
                start_y = int(min(y_atual, self.y_inicial))
                end_y = int(max(y_atual, self.y_inicial))
                
                for y in range(start_y, end_y, 4):
                    offset_x = 20 * math.cos(0.1 * (y - self.y_inicial) + self.timer * 0.3)
                    pontos_v.append((self.x_inicial + offset_x - camera_x, y))
                
                if len(pontos_v) > 1:
                    pg.draw.lines(surf_efeitos, (255, 50, 255, alpha), False, pontos_v, 3)

            # --- 2. Visual da Onda Senoidal (Horizontal) ---
            centro_y = self.y_inicial
            pontos = []
            largura_tela = 1280
            
            for x_tela in range(0, largura_tela, 10):
                x_mundo = x_tela + camera_x
                offset_y = 80 * math.sin(self.freq_onda * x_mundo + self.timer * 0.2)
                pontos.append((x_tela, centro_y + offset_y))

            if len(pontos) > 1:
                pg.draw.lines(surf_efeitos, (0, 255, 255, alpha), False, pontos, 3)
                pg.draw.lines(surf_efeitos, (0, 100, 200, int(alpha * 0.7)), False, [(p[0], p[1]+4) for p in pontos], 2)

        # Desenha a superfície de efeitos na tela principal
        window.blit(surf_efeitos, (0, 0))





class ProtecaoObmepica:
    def __init__(self):
        self.nome = "Proteção OBMÉPICA"
        self.ativo = False
        
        config = CONFIG['personagens']['DrPI']['habilidades']['ProtecaoObmepica']
        self.duracao_max = int(config['duracao_s'] * 60)
        self.timer = 0
        self.raio = config['raio']
        self.fade_in = int(config['fade_in_s'] * 60)
        self.fade_out = int(config['fade_out_s'] * 60)
        self.forca_repulsao = config['forca_repulsao']
        
        # Carrega o sprite da OBMEP
        try:
            self.sprite = pg.image.load('./personagens/dr_pi/sprites/abilities/obmep.png').convert_alpha()
            
            # Recorta apenas a área visível (remove bordas transparentes)
            rect_visivel = self.sprite.get_bounding_rect()
            self.sprite = self.sprite.subsurface(rect_visivel).copy()
            
            self.sprite = pg.transform.scale(self.sprite, (30, 40))
        except Exception:
            # Fallback caso a imagem não exista
            self.sprite = pg.Surface((50, 50), pg.SRCALPHA)
            pg.draw.circle(self.sprite, (255, 215, 0), (25, 25), 25)
            
        self.angulo = 0
        self.jogador_ref = None

    def start(self, jogador):
        self.ativo = True
        self.timer = self.duracao_max
        self.jogador_ref = jogador
        self.angulo = 0

    def update(self, viloes, **kwargs):
        if not self.ativo: return
        
        self.timer -= 1
        if self.timer <= 0:
            self.ativo = False
            return
            
        self.angulo = (self.angulo + 2) % 360
        
        # Lógica de repelir inimigos
        cx, cy = self.jogador_ref.get_colisor().center
        for vilao in viloes:
            if not vilao.esta_vivo: continue
            
            vx, vy = vilao.get_colisor().center
            dist = math.hypot(vx - cx, vy - cy)
            
            if dist < self.raio:
                # Vetor de repulsão mais natural
                dx = vx - cx
                dy = vy - cy
                
                if dist == 0: dist = 1
                
                # Normaliza
                nx = dx / dist
                ny = dy / dist
                
                # Força ajustada para ser forte mas sem "teleportar" (suave)
                forca = self.forca_repulsao
                
                vilao.pos[0] += nx * forca
                vilao.pos[1] += ny * forca

    def draw(self, window, camera_x):
        if not self.ativo: return
        
        # Calcula Alpha para Fade In/Out
        alpha_factor = 1.0
        if self.duracao_max - self.timer < self.fade_in:
            alpha_factor = (self.duracao_max - self.timer) / self.fade_in
        elif self.timer < self.fade_out:
            alpha_factor = self.timer / self.fade_out
            
        cx, cy = self.jogador_ref.get_colisor().center
        
        # Desenha aura (círculo amarelo semi-transparente)
        surf_aura = pg.Surface((self.raio * 2, self.raio * 2), pg.SRCALPHA)
        pg.draw.circle(surf_aura, (255, 215, 0, int(40 * alpha_factor)), (self.raio, self.raio), self.raio)
        pg.draw.circle(surf_aura, (255, 215, 0, int(150 * alpha_factor)), (self.raio, self.raio), self.raio, 2)
        window.blit(surf_aura, (cx - camera_x - self.raio, cy - self.raio))
        
        # Desenha os 3 ícones girando
        raio_rotacao = self.raio * 0.8
        
        # Aplica transparência no sprite
        self.sprite.set_alpha(int(255 * alpha_factor))
        
        for i in range(3):
            theta = math.radians(self.angulo + i * 120) # 0, 120, 240 graus
            ix = cx + math.cos(theta) * raio_rotacao
            iy = cy + math.sin(theta) * raio_rotacao
            
            rect = self.sprite.get_rect(center=(ix, iy))
            window.blit(self.sprite, (rect.x - camera_x, rect.y))
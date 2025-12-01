import pygame as pg
from personagem_base import PersonagemBase
from config_jogo import CONFIG
from mapa import TILE_SIZE
import math

class VilaoBase(PersonagemBase):
    def __init__(self, x, y, velocidade, vida_max, forca_pulo=0, gravidade=1.3):
        # Vilões herdam tudo da PersonagemBase
        super().__init__(x, y, velocidade, vida_max, forca_pulo, gravidade)
        
        # --- Atributos de IA e Combate ---
        self.direcao_movimento = 1 # 1 para direita, -1 para esquerda
        # Lê os valores do config, mas assume um padrão caso não encontre
        config_vilao = CONFIG['viloes'].get(self.__class__.__name__, {})
        self.raio_deteccao = config_vilao.get('raio_deteccao', 400)
        self.dano_contato = config_vilao.get('dano_contato', 250)
        self.cooldown_ataque = 0   # Cooldown para evitar dano contínuo

    def tem_linha_de_visao(self, alvo, mapa_tiles):
        """Verifica se há uma linha de visão direta e sem obstáculos até o alvo."""
        ponto_inicial = self.get_colisor().center
        ponto_final = alvo.get_colisor().center
        
        dx = ponto_final[0] - ponto_inicial[0]
        dy = ponto_final[1] - ponto_inicial[1]
        
        distancia = math.hypot(dx, dy)
        if distancia == 0:
            return True
        
        # Normaliza o vetor de direção
        dx, dy = dx / distancia, dy / distancia
        
        # Percorre a linha de visão em pequenos passos
        passos = int(distancia / 16) # Checa a cada 16 pixels
        for i in range(1, passos):
            x = int((ponto_inicial[0] + dx * i * 16) / TILE_SIZE)
            y = int((ponto_inicial[1] + dy * i * 16) / TILE_SIZE)
            
            # Se o ponto estiver fora do mapa ou em um tile sólido, não há linha de visão
            if not (0 <= y < len(mapa_tiles) and 0 <= x < len(mapa_tiles[0])):
                return False # Fora do mapa bloqueia a visão
            if mapa_tiles[y][x] != ' ':
                return False # Tile sólido bloqueia a visão
        
        return True

    def atualizar(self, mapa_tiles, jogador):
        """Atualiza a lógica do vilão, incluindo IA, movimento e física."""
        if not self.esta_vivo:
            return

        # --- Lógica de IA: Patrulhar ou Perseguir ---
        dist_jogador = math.hypot(self.pos[0] - jogador.pos[0], self.pos[1] - jogador.pos[1]) # Distância bruta
        persegue = False

        # Só persegue se estiver perto E tiver linha de visão
        if dist_jogador < self.raio_deteccao and self.tem_linha_de_visao(jogador, mapa_tiles):
            persegue = True
            # Perseguir: move-se na direção do jogador
            if jogador.pos[0] < self.pos[0]:
                self.direcao_movimento = -1
                self.estado_animacao = "run_esquerda"
            else:
                self.direcao_movimento = 1
                self.estado_animacao = "run_direita"
        else:
            # Patrulhar: define a animação com base na direção de movimento
            if self.direcao_movimento == 1:
                self.estado_animacao = "run_direita"
            else:
                self.estado_animacao = "run_esquerda"

        # --- Movimento e Colisão ---
        dx = self.velocidade * self.direcao_movimento
        self.pos[0] += dx
        col_rect = self.get_colisor()
        for tile_rect in self.get_tiles_proximos(mapa_tiles):
            if col_rect.colliderect(tile_rect):
                # Corrige a posição para não entrar na parede
                if dx > 0: # Movendo para a direita
                    col_rect.right = tile_rect.left
                elif dx < 0: # Movendo para a esquerda
                    col_rect.left = tile_rect.right
                self.pos[0] = col_rect.x - self.colisor_offset[0]

                if persegue and self.no_chao: # Se está perseguindo e bateu, tenta pular
                    self.vel_vertical = self.forca_pulo
                elif not persegue: # Se está patrulhando e bateu, apenas vira
                    if dx > 0:
                        self.direcao_movimento = -1
                    else:
                        self.direcao_movimento = 1
                break # Para de checar após a primeira colisão
        
        # --- Cooldown de Ataque ---
        if self.cooldown_ataque > 0:
            self.cooldown_ataque -= 1

        # Aplica gravidade e colisão vertical da classe base
        super().atualizar(mapa_tiles)
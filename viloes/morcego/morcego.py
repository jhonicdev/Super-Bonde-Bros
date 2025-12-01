import pygame as pg
from vilao_base import VilaoBase
from config_jogo import CONFIG
import random
import math

class Morcego(VilaoBase):
    som_ataque = None

    def __init__(self, x, y):
        # Configurações específicas deste vilão
        config = CONFIG['viloes'].get('Morcego', {})
        # Morcegos não têm pulo e ignoram a gravidade padrão
        super().__init__(x=x, y=y, velocidade=config.get('velocidade', 2), vida_max=config.get('vida_max', 800), forca_pulo=0, gravidade=0)
        self.amplitude_flutuacao = 20  # O quanto ele sobe e desce
        self.frequencia_flutuacao = 0.01 # A velocidade da flutuação

        self.patrol_timer = random.randint(120, 300) # Tempo inicial para patrulha (2 a 5 segundos)
        self.vertical_drift = random.uniform(-0.5, 0.5) * self.velocidade * 0.5 # Desvio vertical inicial aleatório para patrulha

        # --- Sprites ---
        self.fonte_emoji = pg.font.SysFont("Segoe UI Emoji", 50)
        self.sprite_direita = pg.transform.flip(self.fonte_emoji.render("🦇", True, (210, 230, 255)), True, False)
        # DEBUG: Verifica o tamanho do sprite. Se for (0,0), o emoji não está renderizando.
        if self.sprite_direita.get_size() == (0,0):
            print("AVISO: Emoji '🦇' não renderizado. Usando círculo placeholder para Morcego.")
            self.sprite_direita = pg.Surface((50, 50), pg.SRCALPHA) # Placeholder
            pg.draw.circle(self.sprite_direita, (210, 230, 255, 180), (25, 25), 25) # Círculo semi-transparente

        self.sprite_esquerda = pg.transform.flip(self.sprite_direita, True, False)

        # Define as animações na classe base (usando o sprite_direita/esquerda, seja emoji ou placeholder)
        self.animacoes["run_direita"] = [self.sprite_direita]
        self.animacoes["run_esquerda"] = [self.sprite_esquerda]
        self.animacoes["idle_direita"] = [self.sprite_direita] # Correção: sprite_direita não deve ser flipado inicialmente
        self.animacoes["idle_esquerda"] = [self.sprite_esquerda] # Correção: usar sprite_esquerda aqui

        # --- Colisor ---
        largura, altura = self.sprite_direita.get_size()
        self.colisor = [int(largura * 0.7), int(altura * 0.9)]
        self.colisor_offset = [int(largura * 0.15), int(altura * 0.1)]


        if Morcego.som_ataque is None:
            Morcego.som_ataque = pg.mixer.Sound('./viloes/morcego/sound/attack.mp3')


    def atualizar(self, mapa_tiles, jogador):
        """Sobrescreve o método base para adicionar a lógica de flutuação."""
        if not self.esta_vivo:
            return

        # --- Lógica de IA: Patrulhar ou Perseguir (sem colisão com paredes) ---
        dist_jogador = math.hypot(self.pos[0] - jogador.pos[0], self.pos[1] - jogador.pos[1])
        persegue = False

        target_dx, target_dy = 0, 0  # Deslocamento intencional da IA

        # Persegue se estiver perto e tiver linha de visão
        if dist_jogador < self.raio_deteccao and self.tem_linha_de_visao(jogador, mapa_tiles):
            persegue = True
            # Calcula o vetor de direção normalizado para o jogador
            vetor_x, vetor_y = jogador.get_colisor().centerx - self.pos[0], jogador.get_colisor().centery - self.pos[1]
            dist = max(1, math.hypot(vetor_x, vetor_y))
            vetor_x, vetor_y = vetor_x / dist, vetor_y / dist

            # Define o deslocamento com base no vetor e velocidade
            target_dx = vetor_x * self.velocidade
            target_dy = vetor_y * self.velocidade

            # Atualiza a direção da animação
            self.estado_animacao = "run_esquerda" if target_dx < 0 else "run_direita"
            self.direcao_movimento = -1 if target_dx < 0 else 1 # Mantém o controle da direção geral

        else:
            # Patrulha: move-se horizontalmente com mudanças de direção aleatórias
            target_dx = self.velocidade * self.direcao_movimento
            self.patrol_timer -= 1
            if self.patrol_timer <= 0:
                self.direcao_movimento *= -1  # Inverte a direção
                self.patrol_timer = random.randint(120, 300)  # Novo tempo aleatório para a próxima virada
                # Também muda a direção vertical de patrulha aleatoriamente
                self.vertical_drift = random.uniform(-0.5, 0.5) * self.velocidade * 0.5

            # Define a animação com base na nova direção
            self.estado_animacao = "run_direita" if self.direcao_movimento == 1 else "run_esquerda"
            target_dy = self.vertical_drift # Adiciona o drift vertical à patrulha

        # Adiciona a flutuação ao movimento vertical intencional
        flutuacao = math.sin(pg.time.get_ticks() * self.frequencia_flutuacao) * self.amplitude_flutuacao * 0.1
        target_dy += flutuacao

        # --- Movimento e Colisão (separado por eixos) ---
        # Eixo X
        self.pos[0] += target_dx
        col_rect = self.get_colisor()
        for tile_rect in self.get_tiles_proximos(mapa_tiles):
            if col_rect.colliderect(tile_rect):
                # Corrige a posição para não entrar na parede
                if target_dx > 0:  # Movendo para a direita
                    col_rect.right = tile_rect.left
                elif target_dx < 0:  # Movendo para a esquerda
                    col_rect.left = tile_rect.right
                self.pos[0] = col_rect.x - self.colisor_offset[0]
                # Reação à colisão: inverte a direção para a próxima vez
                self.direcao_movimento *= -1
                break

        # Eixo Y
        self.pos[1] += target_dy
        col_rect = self.get_colisor() # Recalcula o colisor após o movimento X
        for tile_rect in self.get_tiles_proximos(mapa_tiles):
            if col_rect.colliderect(tile_rect):
                # Corrige a posição para não entrar na parede
                if target_dy > 0:  # Movendo para baixo (colidindo com o chão)
                    col_rect.bottom = tile_rect.top
                    # Reação: Força um movimento para cima para "desengalhar"
                    self.pos[1] -= 5 # Impulso imediato para cima
                elif target_dy < 0:  # Movendo para cima
                    col_rect.top = tile_rect.bottom
                self.pos[1] = col_rect.y - self.colisor_offset[1]
                # Reação à colisão: inverte o drift vertical para a próxima vez
                self.vertical_drift *= -1
                break

        # Atualiza o cooldown de ataque
        if self.cooldown_ataque > 0:
            self.cooldown_ataque -= 1

    def som(self):
        if Morcego.som_ataque is not None:
            Morcego.som_ataque.play()
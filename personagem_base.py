import pygame as pg
from mapa import TILE_SIZE
from utils import IndicadorDano
import math

class PersonagemBase:
    pg.mixer.init()
    som_pulo = pg.mixer.Sound('./Sounds/pulo.mp3')


    def __init__(self, x, y, velocidade=4, vida_max=2000, forca_pulo=-15, gravidade=1.3,):
        self.pos = [x, y]
        self.velocidade = velocidade
        self.vel_vertical = 0
        self.gravidade = gravidade
        self.forca_pulo = forca_pulo
        self.colisor_offset = [0,0]
        self.colisor = [0, 0]
        self.no_chao = False

        self.vida_max = vida_max
        self.vida = vida_max  # vida atual
        self.esta_vivo = True
        self.menu_icon = None

        # Lista para armazenar os indicadores de dano
        self.indicadores_dano = []

        self.skill_icons = []
        self.name = ""
        
        self.estado_animacao = "idle_direita"
        self.frame = 0

        # --- Atributos de Ataque ---
        self.atacando = False
        self.frame_ataque = 0
        self.cooldowns_habilidades = [] # Lista para os cooldowns de cada habilidade
        self.habilidades_ativas = []    # Lista para habilidades em uso (projéteis, buffs, etc.)

        # Dicionário de animações
        # Cada personagem vai definir suas próprias listas de imagens
        self.animacoes = {
            "idle_direita": [],
            "idle_esquerda": [],
            "run_direita": [],
            "run_esquerda": []
        }

    # ----------------- MOVIMENTO -----------------
    def aplicar_gravidade(self):
        self.vel_vertical += self.gravidade
        self.pos[1] += self.vel_vertical

    def mover(self, teclas, mapa_obj):
        movendo = False
        dx = 0  # Deslocamento em X

        # --- Movimento para esquerda ---
        if teclas[pg.K_a] or teclas[pg.K_LEFT]:
            dx -= self.velocidade
            self.estado_animacao = "run_esquerda"
            movendo = True

        # --- Movimento para direita ---
        if teclas[pg.K_d] or teclas[pg.K_RIGHT]:
            dx += self.velocidade
            self.estado_animacao = "run_direita"
            movendo = True

        # --- Aplica movimento horizontal ---
        self.pos[0] += dx

        # --- Checagem de Colisão com Paredes ---
        col_rect = self.get_colisor()
        for tile_rect in self.get_tiles_proximos(mapa_obj.tiles):
            if col_rect.colliderect(tile_rect):
                if dx > 0:  # Movendo para a direita
                    col_rect.right = tile_rect.left
                elif dx < 0:  # Movendo para a esquerda
                    col_rect.left = tile_rect.right
                self.pos[0] = col_rect.x - self.colisor_offset[0]

        # --- Pulo ---
        if (teclas[pg.K_w] or teclas[pg.K_UP]) and self.no_chao:
            self.som_pulo.play()
            self.vel_vertical = self.forca_pulo
            self.no_chao = False  # evita pulo duplo enquanto segura a tecla

        # --- Animação de Idle ---
        if not movendo:
            if self.estado_animacao == "run_direita":
                self.estado_animacao = "idle_direita"
            elif self.estado_animacao == "run_esquerda":
                self.estado_animacao = "idle_esquerda"

    def get_colisor(self):
        """Retorna o retângulo de colisão do personagem."""
        return pg.Rect(
            self.pos[0] + self.colisor_offset[0],
            self.pos[1] + self.colisor_offset[1],
            self.colisor[0],
            self.colisor[1]
        )

    def get_tiles_proximos(self, mapa):
        """
        Otimização CRÍTICA: Retorna apenas os tiles ao redor do personagem.
        Isso evita iterar sobre o mapa inteiro a cada frame.
        """
        # Calcula a posição do personagem em coordenadas de tile
        tile_x = int(self.get_colisor().centerx / TILE_SIZE)
        tile_y = int(self.get_colisor().centery / TILE_SIZE)

        # Itera em uma grade 3x3 ao redor do personagem
        for y_offset in range(-1, 2):
            for x_offset in range(-1, 2):
                check_x, check_y = tile_x + x_offset, tile_y + y_offset
                if 0 <= check_y < len(mapa) and 0 <= check_x < len(mapa[0]) and mapa[check_y][check_x] != ' ':
                    yield pg.Rect(check_x * TILE_SIZE, check_y * TILE_SIZE, TILE_SIZE, TILE_SIZE)

    def iniciar_habilidade(self, index):
        """Inicia a habilidade no índice especificado se não estiver em cooldown."""
        if index < len(self.cooldowns_habilidades) and self.cooldowns_habilidades[index] == 0:
            self.atacando = True
            self.frame_ataque = 0
            self.cooldowns_habilidades[index] = 60  # Cooldown padrão de 60 frames (1s)
            # Cada personagem pode sobrescrever isso com sua lógica específica

    def atualizar_habilidades(self, mapa_tiles, viloes=[], camera_x=0):
        """Atualiza a lógica das habilidades e cooldowns a cada frame."""
        # Atualiza cooldowns
        for i in range(len(self.cooldowns_habilidades)):
            if self.cooldowns_habilidades[i] > 0:
                self.cooldowns_habilidades[i] -= 1

        # Atualiza estado de ataque
        if self.atacando:
            self.frame_ataque += 1
            # Simplesmente termina o ataque após alguns frames (ex: 15 frames)
            if self.frame_ataque > 15:
                self.atacando = False

        # Atualiza as habilidades ativas
        for habilidade in self.habilidades_ativas:
            # Passa os argumentos necessários para o update da habilidade
            if hasattr(habilidade, 'update'):
                # Esta é uma forma flexível de chamar o update,
                # passando o que for necessário para cada tipo de habilidade.
                habilidade.update(mapa_tiles=mapa_tiles, viloes=viloes, jogador=self)

        # Remove habilidades inativas
        self.habilidades_ativas = [h for h in self.habilidades_ativas if hasattr(h, 'ativo') and h.ativo]

    def receber_dano(self, quantidade):
        """Reduz a vida do personagem e lida com a morte."""
        # Cria um novo indicador de dano na posição do personagem
        pos_x, pos_y = self.get_colisor().midtop
        novo_indicador = IndicadorDano(pos_x, pos_y, quantidade)
        self.indicadores_dano.append(novo_indicador)

        self.vida -= quantidade
        if self.vida <= 0:
            self.vida = 0
            self.esta_vivo = False
            # Aqui poderíamos adicionar um som de morte ou uma animação

    def checar_queda(self, altura_mapa):
        """Verifica se o personagem caiu para fora do mapa."""
        if self.pos[1] > altura_mapa:
            self.esta_vivo = False

    def manter_nos_limites_mapa(self, mapa_obj):
        """Garante que a entidade não saia das bordas X do mapa."""
        colisor = self.get_colisor()
        # Borda esquerda
        if colisor.left < 0:
            self.pos[0] = -self.colisor_offset[0]
        # Borda direita
        elif colisor.right > mapa_obj.map_width:
            self.pos[0] = mapa_obj.map_width - self.colisor[0] - self.colisor_offset[0]

    def atualizar(self, mapa):
        # Atualiza e remove os indicadores de dano que já expiraram
        for indicador in self.indicadores_dano:
            indicador.atualizar()
        self.indicadores_dano = [ind for ind in self.indicadores_dano if ind.duracao_restante > 0]

        # --- Aplica gravidade e checa colisão vertical ---
        self.no_chao = False
        self.aplicar_gravidade()
        col_rect = self.get_colisor()

        for tile_rect in self.get_tiles_proximos(mapa):
            if col_rect.colliderect(tile_rect):
                if self.vel_vertical > 0:  # Caindo (colisão com o chão)
                    col_rect.bottom = tile_rect.top
                    self.no_chao = True
                    self.vel_vertical = 0
                elif self.vel_vertical < 0:  # Subindo (colisão com o teto)
                    col_rect.top = tile_rect.bottom
                    self.vel_vertical = 0  # Zera a velocidade para começar a cair
                self.pos[1] = col_rect.y - self.colisor_offset[1]
        
        # --- Checa se o personagem caiu do mapa ---
        self.checar_queda(len(mapa) * TILE_SIZE)
        
        # --- Mantém a entidade dentro dos limites do mapa ---
        # self.manter_nos_limites_mapa(mapa) # Esta linha será chamada no main.py

    # ----------------- DESENHO -----------------
    def desenhar(self, janela, offset_x=0):
        frames = self.animacoes.get(self.estado_animacao, [])
        if len(frames) == 0:
            return  # evita erro se o personagem ainda não carregou animação

        # Desenha as habilidades ativas
        for habilidade in self.habilidades_ativas:
            if hasattr(habilidade, 'draw'):
                habilidade.draw(janela, offset_x)

        # Desenha os indicadores de dano
        for indicador in self.indicadores_dano:
            indicador.desenhar(janela, offset_x)

        # Placeholder visual para o ataque (um círculo vermelho)
        if self.atacando:
            centro_personagem = self.get_colisor().center
            pg.draw.circle(janela, (255, 0, 0), (centro_personagem[0] - offset_x, centro_personagem[1]), 15)

        index = (self.frame // 7) % len(frames)
        janela.blit(frames[index], (self.pos[0] - offset_x, self.pos[1]))
        self.frame = (self.frame + 1) % (7 * len(frames))

    def draw_world_health_bar(self, window, camera_x):
        """Desenha uma barra de vida simples acima do personagem, no mundo do jogo."""
        if not self.esta_vivo:
            return

        # Configurações da barra de vida do vilão
        largura_barra = self.colisor[0]  # Largura igual à do colisor
        altura_barra = 8
        offset_y = 15  # Distância acima da cabeça do personagem

        # Posição da barra
        pos_x = self.get_colisor().x - camera_x
        pos_y = self.get_colisor().y - offset_y

        # Percentual de vida
        vida_percent = max(0, self.vida / self.vida_max)
        vida_largura_atual = int(largura_barra * vida_percent)

        # Desenha o fundo da barra e a vida
        pg.draw.rect(window, (80, 0, 0), (pos_x, pos_y, largura_barra, altura_barra))
        pg.draw.rect(window, (200, 0, 0), (pos_x, pos_y, vida_largura_atual, altura_barra))

    def draw_health_bar(self, window, x=40, y=20, largura=400, altura=70):
        # Percentual de vida
        vida_percent = max(0, self.vida / self.vida_max)  # nunca negativo
        vida_largura = int(largura * vida_percent)

        # Fonte
        font = pg.font.SysFont("Segoe UI Emoji", 20, bold=True)

        # Fundo da barra
        pg.draw.rect(window, (60, 60, 60), (x, y, largura, altura), border_radius=5)
        # Barra de vida
        pg.draw.rect(window, (200, 0, 0), (x, y, vida_largura, altura), border_radius=5)
        # Borda da barra
        pg.draw.rect(window, (255, 255, 255), (x, y, largura, altura), 2, border_radius=5)


        # Texto da vida dentro da barra
        texto = font.render(f"{self.vida} / {self.vida_max}", True, (255, 255, 255))
        texto_rect = texto.get_rect(center=(x + largura // 2, y + altura // 2))
        window.blit(texto, texto_rect)

    def draw_skill_icons(self, window, x_start=500, y=20, icon_size=70, spacing=12):
        """Desenha os ícones das habilidades e seus cooldowns."""
        font = pg.font.SysFont("Segoe UI", 32, bold=True)

        for i, icon in enumerate(self.skill_icons):
            x = x_start + i * (icon_size + spacing)
            icon_rect = pg.Rect(x, y, icon_size, icon_size)

            # Centraliza o ícone (que agora é proporcional) dentro do espaço do botão
            icon_pos_rect = icon.get_rect(center=icon_rect.center)
            window.blit(icon, icon_pos_rect)

            # Se a habilidade estiver em cooldown
            if i < len(self.cooldowns_habilidades) and self.cooldowns_habilidades[i] > 0:
                # Desenha uma camada escura semi-transparente
                overlay = pg.Surface((icon_size, icon_size), pg.SRCALPHA)
                # Desenha um retângulo arredondado no overlay para evitar cantos pretos
                pg.draw.rect(overlay, (0, 0, 0, 180), overlay.get_rect(), border_radius=5)
                window.blit(overlay, (x, y))

                # Desenha o tempo de recarga restante
                tempo_restante = math.ceil(self.cooldowns_habilidades[i] / 60)
                texto_cooldown = font.render(str(tempo_restante), True, (255, 255, 255))
                texto_rect = texto_cooldown.get_rect(center=icon_rect.center)
                window.blit(texto_cooldown, texto_rect)

            # Desenha um fundo para o ícone (opcional, mas ajuda na visibilidade)
            # pg.draw.rect(window, (40, 40, 70), icon_rect, 0, border_radius=5)

            # Desenha a borda e o número da tecla
            # Criamos uma superfície temporária para desenhar a borda com cantos transparentes
            border_surf = pg.Surface((icon_size, icon_size), pg.SRCALPHA)
            pg.draw.rect(border_surf, (255, 255, 255), border_surf.get_rect(), 2, border_radius=5)
            window.blit(border_surf, (x, y))

            # Desenha o número da tecla
            tecla_texto = pg.font.SysFont("Segoe UI", 16).render(str(i + 1), True, (0, 0, 0))
            pg.draw.rect(window, (255, 255, 255), (x, y + icon_size - 18, 18, 18))
            window.blit(tecla_texto, (x + 5, y + icon_size - 19))


    def som_kill(self):
        pass
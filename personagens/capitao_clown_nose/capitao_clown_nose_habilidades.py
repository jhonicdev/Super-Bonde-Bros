import pygame as pg
from mapa import TILE_SIZE
from config_jogo import CONFIG
import math

class SacoDeMoedas:
    ANIMACAO = None  # Atributo de classe para guardar a animação pré-carregada

    som_colisao_moedas = None


    @classmethod
    def carregar_recursos(cls):
        """Pré-carrega os recursos da habilidade para evitar lag."""
        if cls.ANIMACAO is None:
            # Carrega os frames da animação (assumindo 4 frames, de _1.png a _4.png)
            if cls.som_colisao_moedas is None:
                cls.som_colisao_moedas = pg.mixer.Sound('./personagens/capitao_clown_nose/sound/effects/moedas_colisao.mp3')
            '''
            cls.ANIMACAO = [
                pg.transform.rotate(
                    pg.transform.scale(pg.image.load(f'./personagens/capitao_clown_nose/sprites/attack/saco_de_moedas_{i}.png').convert_alpha(), (18, 60)),
                    270
                )
                for i in range(1, 5)
            ]
            '''
            cls.ANIMACAO = [
                pg.transform.rotate(
                    pg.font.SysFont("Segoe UI Emoji", 30).render("💰", True, (200, 200, 220)),
                    90
                )
            ]

    def __init__(self, x, y, direcao):
        """
        Inicializa o projétil.
        x, y: Posição inicial.
        direcao: 1 para direita, -1 para esquerda.
        """
        self.animacao = SacoDeMoedas.ANIMACAO
        # Vira a imagem se a direção for para a esquerda
        if direcao == -1:
            self.animacao = [pg.transform.flip(img, True, False) for img in self.animacao]

        self.frame_atual = 0
        self.imagem = self.animacao[self.frame_atual]


        self.fonte_emoji = pg.font.SysFont("Segoe UI Emoji", 30)
        self.imagem_original = self.fonte_emoji.render("💰", True, (200, 200, 220))
        self.imagem = pg.transform.rotate(
            self.imagem_original,
            90
        )
        self.rect = self.imagem.get_rect(center=(x, y))


        self.velocidade = 10 * direcao
        self.velocidade_animacao = 0.2
        self.ativo = True # Controla se o projétil deve ser atualizado e desenhado

        # --- Lendo valores do arquivo de configuração ---
        config = CONFIG['personagens']['CapitaoClownNose']['habilidades']['SacoDeMoedas']
        self.dano = config['dano']
        self.velocidade = config['velocidade'] * direcao

    def acertou_alvo(self, alvo):
        """Chamado quando a habilidade acerta um alvo."""
        alvo.receber_dano(self.dano)
        self.som_colisao_moedas.play()

    def update(self, mapa_tiles, **kwargs): # Adicionado **kwargs para ignorar argumentos extras
        """Move o projétil, atualiza sua animação e checa colisão com o mapa."""
        self.rect.x += self.velocidade

        # Atualiza o frame da animação
        self.frame_atual = (self.frame_atual + self.velocidade_animacao) % len(self.animacao)
        self.imagem = self.animacao[int(self.frame_atual)]

        # Lógica de colisão otimizada
        # Calcula em qual tile o centro do projétil está
        tile_x = int(self.rect.centerx / TILE_SIZE)
        tile_y = int(self.rect.centery / TILE_SIZE)

        # Verifica se as coordenadas do tile são válidas e se o tile não é um espaço vazio
        if 0 <= tile_y < len(mapa_tiles) and 0 <= tile_x < len(mapa_tiles[0]) and mapa_tiles[tile_y][tile_x] != ' ':
            self.som_colisao_moedas.play() # SOM DO SACO DE MOEDAS COLIDINDO
            self.ativo = False # Desativa o projétil ao colidir

    def draw(self, janela, offset_x):
        """Desenha o projétil na tela, ajustado pela câmera."""
        janela.blit(self.imagem, (self.rect.x - offset_x, self.rect.y))

    def esta_fora_da_tela(self, camera_x, largura_tela):
        """Verifica se o projétil saiu completamente da visão da câmera."""
        return self.rect.right < camera_x or self.rect.left > camera_x + largura_tela





class LapadaSeca:
    som_ancora_girando = None
    som_ancora_colisao = None


    def __init__(self, x, y, direcao, jogador):
        self.jogador = jogador
        self.fonte_emoji = pg.font.SysFont("Segoe UI Emoji", 50)
        self.imagem_original = self.fonte_emoji.render("⚓", True, (200, 200, 220))
        self.imagem = self.imagem_original
        self.rect = self.imagem.get_rect(center=(x, y))
        
        self.angulo = 0
        
        self.estado = "ida"  # 'ida' ou 'volta'
        self.distancia_percorrida = 0
        self.ativo = True
        self.alvos_acertados = [] # Lista para não acertar o mesmo alvo múltiplas vezes

        # --- Lendo valores do arquivo de configuração ---
        config = CONFIG['personagens']['CapitaoClownNose']['habilidades']['LapadaSeca']
        self.dano = config['dano']
        self.velocidade = config['velocidade'] * direcao
        self.velocidade_rotacao = config['velocidade_rotacao'] * direcao
        self.distancia_maxima = config['distancia_max']

        # Carrega os sons se ainda não foram carregados
        if LapadaSeca.som_ancora_girando is None:
            LapadaSeca.som_ancora_girando = pg.mixer.Sound('./personagens/capitao_clown_nose/sound/effects/ancora_girando.mp3')
            LapadaSeca.som_ancora_colisao = pg.mixer.Sound('./personagens/capitao_clown_nose/sound/effects/ancora_colisao.mp3')

        self.som_ancora_girando.play() # SOM DE ANCORA GIRANDO

    def acertou_alvo(self, alvo):
        """Lida com o acerto em um alvo, garantindo dano e som únicos."""
        if alvo not in self.alvos_acertados:
            alvo.receber_dano(self.dano)
            self.som_ancora_colisao.play()
            self.alvos_acertados.append(alvo)


    def update(self, mapa_tiles, **kwargs): # Adicionado **kwargs para ignorar argumentos extras
        """Move, rotaciona e atualiza o estado da âncora."""
        # Rotaciona a âncora
        self.angulo += self.velocidade_rotacao
        self.imagem = pg.transform.rotate(self.imagem_original, self.angulo)
        self.rect = self.imagem.get_rect(center=self.rect.center)

        if self.estado == "ida":
            self.rect.x += self.velocidade
            self.distancia_percorrida += abs(self.velocidade)
            if self.distancia_percorrida >= self.distancia_maxima:
                self.estado = "volta"
                self.alvos_acertados.clear() # Limpa alvos para poder acertá-los na volta
        
        elif self.estado == "volta":
            # Move de volta para o jogador
            alvo_x, alvo_y = self.jogador.get_colisor().center
            dx, dy = alvo_x - self.rect.centerx, alvo_y - self.rect.centery
            dist = max(1, (dx**2 + dy**2)**0.5) # Evita divisão por zero
            
            self.rect.x += (dx / dist) * abs(self.velocidade)
            self.rect.y += (dy / dist) * abs(self.velocidade)

            # Se colidir com o jogador, desativa
            if self.rect.colliderect(self.jogador.get_colisor()):
                self.som_ancora_girando.fadeout(200) # PARANDO O SOM DE ANCORA GIRANDO
                self.ativo = False

        # Colisão com paredes
        tile_x = int(self.rect.centerx / TILE_SIZE)
        tile_y = int(self.rect.centery / TILE_SIZE)
        if 0 <= tile_y < len(mapa_tiles) and 0 <= tile_x < len(mapa_tiles[0]) and mapa_tiles[tile_y][tile_x] != ' ':
            if self.estado == "ida": self.som_ancora_colisao.play() # SOM DE ANCORA COLIDINDO
            if self.estado == "ida":
                self.estado = "volta" # Ao bater na parede, começa a voltar
                self.alvos_acertados.clear() # Limpa alvos para poder acertá-los na volta


    def draw(self, janela, offset_x):
        janela.blit(self.imagem, (self.rect.x - offset_x, self.rect.y))

    def esta_fora_da_tela(self, camera_x, largura_tela):
        # Um bumerangue não deve ser removido se sair da tela, pois ele precisa voltar
        return False


class ProjetilFantasma:
    som_projetil_fantasma = None


    """Um projétil espectral disparado pelo TripulanteFantasma."""
    def __init__(self, x, y, alvo_x, alvo_y):
        self.config = CONFIG['personagens']['CapitaoClownNose']['habilidades']['TripulanteFantasma']['projetil']

        # Cria o rect de colisão com base no raio definido no config
        diametro = self.config['raio'] * 2
        self.rect = pg.Rect(0, 0, diametro, diametro)
        self.rect.center = (x, y)
        self.dano = self.config['dano']
        self.ativo = True
        self.duracao = self.config['duracao_s'] * 60

        # Calcula o vetor de direção normalizado
        dx, dy = alvo_x - x, alvo_y - y
        dist = max(1, math.hypot(dx, dy))
        self.vel_x = (dx / dist) * self.config['velocidade']
        self.vel_y = (dy / dist) * self.config['velocidade']


    def update(self, mapa_tiles, **kwargs): # Aceita argumentos extras para não quebrar
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

        self.duracao -= 1
        if self.duracao <= 0:
            self.ativo = False

        # Checa colisão com paredes
        tile_x = int(self.rect.centerx / TILE_SIZE)
        tile_y = int(self.rect.centery / TILE_SIZE)
        if 0 <= tile_y < len(mapa_tiles) and 0 <= tile_x < len(mapa_tiles[0]) and mapa_tiles[tile_y][tile_x] != ' ':
            self.ativo = False

    def draw(self, janela, offset_x):
        # Desenha um círculo simples como projétil
        pg.draw.circle(janela, (180, 220, 255), (self.rect.centerx - offset_x, self.rect.centery), self.config['raio'])


class TripulanteFantasma:
    som_spawn_fantasma = pg.mixer.Sound('./personagens/capitao_clown_nose/sound/effects/spawn_fantasma.mp3')

    """
    Um fantasma invocado que flutua perto do jogador para protegê-lo.
    """
    def __init__(self, x, y, direcao, jogador):
        self.jogador = jogador
        self.fonte_emoji = pg.font.SysFont("Segoe UI Emoji", 50)
        self.imagem_original = self.fonte_emoji.render("👻", True, (200, 200, 220))
        
        self.imagem = pg.transform.flip(self.imagem_original, direcao == -1, False)
        self.rect = self.imagem.get_rect(center=(x, y))
        
        # --- Atributos para flutuação (onda senoide) ---
        self.amplitude = 15      # Quão alto e baixo ele flutua
        self.frequencia = 0.05   # Velocidade da flutuação
        self.tempo = 0           # Contador para a função seno
        
        # --- Posição relativa ao jogador ---
        self.offset_x_base = 60  # Distância horizontal do jogador
        self.offset_y_base = -20 # Distância vertical (acima da cabeça)
        
        # --- Atributos para movimento suave (física de mola) ---
        self.vel_x = 0
        self.vel_y = 0
        self.forca_atracao = 0.003  # Quão rápido ele segue o jogador
        self.amortecimento = 0.92  # Evita que ele oscile demais (damping)
        
        # --- Lendo valores do arquivo de configuração ---
        config = CONFIG['personagens']['CapitaoClownNose']['habilidades']['TripulanteFantasma']
        self.duracao = config['duracao_s'] * 60
        self.raio_deteccao = config['raio_deteccao']
        self.cooldown_ataque_max = config['cooldown_ataque_s'] * 60

        # --- Atributos de ciclo de vida e animação ---
        self.ativo = True
        self.cooldown_ataque = 0
        self.estado_vida = 'ENTRANDO' # 'ENTRANDO', 'ATIVO', 'SAINDO'
        self.alpha = 0 # Transparência inicial
        self.velocidade_fade = 5 # Velocidade do fade-in/out

        if not TripulanteFantasma.som_spawn_fantasma is None:
            TripulanteFantasma.som_spawn_fantasma.play()
            

    def tem_linha_de_visao(self, alvo, mapa_tiles):
        """Verifica se há uma linha de visão direta e sem obstáculos até o alvo."""
        # Otimização: Se o fantasma não estiver visível, não precisa checar
        if self.alpha < 255:
            return False

        ponto_inicial = self.rect.center
        ponto_final = alvo.get_colisor().center
        dx, dy = ponto_final[0] - ponto_inicial[0], ponto_final[1] - ponto_inicial[1]
        distancia = math.hypot(dx, dy)
        if distancia == 0: return True
        dx, dy = dx / distancia, dy / distancia
        passos = int(distancia / 16)
        for i in range(1, passos):
            x = int((ponto_inicial[0] + dx * i * 16) / TILE_SIZE)
            y = int((ponto_inicial[1] + dy * i * 16) / TILE_SIZE)
            if not (0 <= y < len(mapa_tiles) and 0 <= x < len(mapa_tiles[0])) or mapa_tiles[y][x] != ' ':
                return False
        return True

    def update(self, mapa_tiles, viloes, jogador, **kwargs):
        """
        Atualiza a posição do fantasma e sua lógica de ataque.
        Recebe a lista de vilões e a referência do jogador para adicionar novos projéteis.
        """
        # --- Gerenciamento do Ciclo de Vida ---
        if self.estado_vida == 'ENTRANDO':
            self.alpha += self.velocidade_fade
            if self.alpha >= 255:
                self.alpha = 255
                self.estado_vida = 'ATIVO'
        
        elif self.estado_vida == 'ATIVO':
            # --- Lógica de Ataque (só ataca quando totalmente visível) ---
            if self.cooldown_ataque > 0:
                self.cooldown_ataque -= 1
            elif self.cooldown_ataque <= 0:
                for vilao in viloes:
                    if vilao.esta_vivo and math.hypot(vilao.get_colisor().centerx - self.rect.centerx, vilao.get_colisor().centery - self.rect.centery) < self.raio_deteccao:
                        if self.tem_linha_de_visao(vilao, mapa_tiles):
                            alvo_x, alvo_y = vilao.get_colisor().center
                            novo_projetil = ProjetilFantasma(self.rect.centerx, self.rect.centery, alvo_x, alvo_y)
                            jogador.habilidades_ativas.append(novo_projetil)
                            self.cooldown_ataque = self.cooldown_ataque_max
                            break
            
            # --- Duração ---
            self.duracao -= 1
            # Começa a sair 2 segundos antes de acabar
            if self.duracao <= 120: 
                self.estado_vida = 'SAINDO'

        elif self.estado_vida == 'SAINDO':
            # Efeito de piscar e fade-out
            self.alpha -= self.velocidade_fade
            if self.alpha <= 0:
                self.alpha = 0
                self.ativo = False # Desativa o fantasma permanentemente

        # --- Posição Horizontal (sempre atrás do jogador) ---
        direcao_jogador = 1 if "direita" in self.jogador.estado_animacao else -1
        offset_x_alvo = -self.offset_x_base * direcao_jogador
        
        # --- Posição Vertical Alvo (com flutuação) ---
        self.tempo += 1
        flutuacao = math.sin(self.tempo * self.frequencia) * self.amplitude        
        
        # --- Calcula a posição alvo ---
        alvo_x = self.jogador.get_colisor().centerx + offset_x_alvo
        alvo_y = self.jogador.get_colisor().centery + self.offset_y_base + flutuacao
        
        # --- Calcula a força de atração em direção ao alvo ---
        self.vel_x += (alvo_x - self.rect.centerx) * self.forca_atracao
        self.vel_y += (alvo_y - self.rect.centery) * self.forca_atracao
        
        # --- Aplica amortecimento e atualiza a posição ---
        self.vel_x *= self.amortecimento
        self.vel_y *= self.amortecimento
        self.rect.move_ip(self.vel_x, self.vel_y)
        
    def acertou_alvo(self, alvo):
        # O fantasma em si não causa dano de contato, apenas seus projéteis.
        pass

    def draw(self, janela, offset_x):
        """Desenha o fantasma na tela, ajustado pela câmera."""
        # Cria uma cópia da imagem para não modificar a original
        imagem_temp = self.imagem.copy()
        # Aplica a transparência
        imagem_temp.set_alpha(self.alpha)
        janela.blit(imagem_temp, (self.rect.x - offset_x, self.rect.y))
import pygame as pg
from mapa import Mapa
from menu import MenuInicial
from menu_personagens import TelaPersonagens
from configuracoes import TelaConfiguracoes
from personagem_info import TelaInfoPersonagem

from personagens.capitao_clown_nose.capitao_clown_nose_habilidades import TripulanteFantasma
# Importa classes específicas de personagens
from personagens.capitao_clown_nose.capitao_clown_nose import CapitaoClownNose
from personagens.joao_poker.joao_poker import JoaoPoker
from personagens.dr_pi.dr_pi import DrPI
from personagens.capitao_clown_nose.capitao_clown_nose_habilidades import SacoDeMoedas
from viloes.carangueijo_pirata.caranguejo_pirata import CaranguejoPirata

# ---------------------- Inicialização ----------------------
pg.init()
pg.mixer.init()
janela = pg.display.set_mode((1280, 768))
pg.display.set_caption("Super Bonde Bros")
clock = pg.time.Clock()

# ---------------------- Instâncias únicas ----------------------
jogador = None
mapa = Mapa()  # Carregado uma vez
viloes = mapa.carregar_viloes() # O mapa agora é responsável por criar os vilões

menu = MenuInicial(janela)

# Inicializa tela com menu imediatamente
janela.fill((0, 0, 0))   # fundo preto temporário
menu.desenhar()           # desenha o menu inicial
pg.display.update()       # atualiza a tela

personagens_tela = TelaPersonagens(janela)
config = TelaConfiguracoes(janela)
tela_info = None
personagem_selecionado = None

# ---------------------- Estado da tela ----------------------
tela_atual = "menu"  # menu, jogo, personagens, info_personagem, config

# ---------------------- Parâmetros de câmera ----------------------
def calcular_camera(jogador):
    camera_x = jogador.pos[0] - 640 + 64
    if camera_x < 0:
        camera_x = 0
    elif camera_x > mapa.map_width - 1280:
        camera_x = mapa.map_width - 1280
    return camera_x

# ---------------------- Loop principal ----------------------
running = True
while running:
    clock.tick(60)
    
    # ---------------------- Eventos ----------------------
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        # Evento de tecla pressionada para ações únicas (como ataque)
        if event.type == pg.KEYDOWN:
            if tela_atual == "jogo" and jogador:
                # Mapeia teclas K_1 a K_9 para habilidades 0 a 8
                if pg.K_1 <= event.key <= pg.K_9:
                    habilidade_index = event.key - pg.K_1
                    jogador.iniciar_habilidade(habilidade_index)
                elif event.key == pg.K_0: # Tecla 0 para habilidade 9
                    jogador.iniciar_habilidade(9)

        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            pos = pg.mouse.get_pos()

            # Menu principal
            if tela_atual == "menu":
                res = menu.checar_clique(pos)
                if res == "start" and not jogador is None:
                    tela_atual = "jogo"
                elif res == "personagens":
                    tela_atual = "personagens"
                elif res == "config":
                    tela_atual = "config"
                elif res == "sair":
                    running = False

            # Tela de personagens
            elif tela_atual == "personagens":
                res = personagens_tela.checar_clique(pos)
                if res == "menu":
                    tela_atual = "menu"
                elif isinstance(res, tuple) and res[0] == "info_personagem":
                    personagem_selecionado = res[1]
                    tela_info = TelaInfoPersonagem(janela, personagem_selecionado)
                    tela_atual = "info_personagem"

            # Modal de informações do personagem
            elif tela_atual == "info_personagem" and tela_info:
                res = tela_info.checar_clique(pos)
                if res == "personagens":
                    tela_atual = "personagens"
                elif res == "selecionar":
                    nome = personagem_selecionado["nome"]
                    if nome == "Capitão Clown Nose":
                        jogador = CapitaoClownNose(100, 500)
                    elif nome == "João Poker":
                        jogador = JoaoPoker(100, 500)
                    elif nome == "Dr. PI":
                        jogador = DrPI(100, 500)
                    tela_atual = "menu"  # volta para o menu

            # Tela de configurações
            elif tela_atual == "config":
                res = config.checar_clique(pos)
                if res == "menu":
                    tela_atual = "menu"

    # ---------------------- Teclado ----------------------
    teclas = pg.key.get_pressed()
    jogador_movendo = False
    if tela_atual == "jogo" and jogador:
        # Se o jogador apertar teclas de movimento
        if teclas[pg.K_a] or teclas[pg.K_LEFT] or teclas[pg.K_d] or teclas[pg.K_RIGHT]:
            jogador_movendo = True

        jogador.mover(teclas, mapa)
        jogador.atualizar(mapa.tiles)
        jogador.manter_nos_limites_mapa(mapa)

        # Otimização: Calcula a câmera uma vez e reutiliza
        camera_x = calcular_camera(jogador)
        # A classe base agora lida com passar os vilões para as habilidades
        jogador.atualizar_habilidades(mapa.tiles, viloes, camera_x)

        # --- Atualiza todos os vilões ---
        for vilao in viloes:
            # Otimização: Só atualiza vilões que estão perto da tela
            dist_vilao_cam = vilao.pos[0] - camera_x
            if -200 < dist_vilao_cam < 1280 + 200: # 1280 é a largura da tela
                vilao.atualizar(mapa.tiles, jogador)
                vilao.manter_nos_limites_mapa(mapa)

        # --- Lógica de Combate e Colisões ---
        # 1. Habilidades do jogador acertando vilões
        for habilidade in jogador.habilidades_ativas:
            if hasattr(habilidade, 'dano'): # Checa se a habilidade pode causar dano
                for vilao in viloes: # Itera sobre uma cópia para evitar problemas se um vilão morrer
                    if vilao.esta_vivo and habilidade.rect.colliderect(vilao.get_colisor()):
                        # Se a habilidade tiver um método para lidar com o acerto, use-o
                        if hasattr(habilidade, 'acertou_alvo'):
                            habilidade.acertou_alvo(vilao)
                        else: # Lógica padrão
                            vilao.receber_dano(habilidade.dano)

                        # Saco de Moedas é destruído, a âncora (LapadaSeca) não.
                        if isinstance(habilidade, SacoDeMoedas):
                            habilidade.ativo = False
                            break # Para de checar outros vilões para esta moeda

        # 2. Vilões tocando no jogador
        for vilao in viloes:
            if vilao.esta_vivo and vilao.get_colisor().colliderect(jogador.get_colisor()):
                if vilao.cooldown_ataque == 0:
                    jogador.receber_dano(vilao.dano_contato)
                    vilao.cooldown_ataque = 60 # 1 segundo de invulnerabilidade após o toque

        # --- Remoção de Entidades Mortas ---
        viloes = [v for v in viloes if v.esta_vivo]

        # --- Checa se o jogador morreu ---
        if not jogador.esta_vivo:
            tela_atual = "menu" # Volta para o menu se o jogador morrer
            viloes = mapa.carregar_viloes() # Reinicia os vilões para a próxima partida

            # Recria o jogador para resetar seu estado (vida, posição, etc.)
            # Isso permite que o jogo seja reiniciado corretamente.
            if isinstance(jogador, CapitaoClownNose):
                jogador = CapitaoClownNose(100, 500)
            elif isinstance(jogador, JoaoPoker):
                jogador = JoaoPoker(100, 500)
            elif isinstance(jogador, DrPI):
                jogador = DrPI(100, 500)
    # ---------------------- Desenho ----------------------
    janela.fill((0, 0, 0))

    if tela_atual == "jogo" and jogador:
        # Nuvens só se mexem quando o jogador se move
        mapa.draw_background(janela, camera_x, mover_nuvens=jogador_movendo)
        mapa.draw_tiles(janela, camera_x)
        jogador.desenhar(janela, camera_x)

        # --- Desenha todos os vilões ---
        for vilao in viloes:
            vilao.desenhar(janela, camera_x)
            vilao.draw_world_health_bar(janela, camera_x)
        # Desenha a barra de vida do jogador no topo da tela
        jogador.draw_health_bar(janela, x=40, y=20, largura=440, altura=70)
        jogador.draw_skill_icons(janela)

    elif tela_atual == "menu":
        menu.desenhar(personagem=jogador)

    elif tela_atual == "personagens":
        mapa.draw_background(janela)
        overlay = pg.Surface((1280, 768), pg.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        janela.blit(overlay, (0, 0))
        personagens_tela.desenhar()

    elif tela_atual == "info_personagem" and tela_info:
        mapa.draw_background(janela)
        overlay = pg.Surface((1280, 768), pg.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        janela.blit(overlay, (0, 0))
        tela_info.desenhar()

    elif tela_atual == "config":
        mapa.draw_background(janela)
        overlay = pg.Surface((1280, 768), pg.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        janela.blit(overlay, (0, 0))
        config.desenhar()

    pg.display.update()

pg.quit()

import pygame as pg
from mapa import Mapa
from utils import scale_proporcional



class TelaInfoPersonagem:
    def __init__(self, window, personagem):
        self.window = window
        self.mapa = Mapa()
        self.personagem = personagem
        self.font_title = pg.font.SysFont("Courier New", 60, bold=True)
        self.font_text = pg.font.SysFont("Segoe UI Emoji", 25)
        self.font_hab = pg.font.SysFont("Segoe UI Emoji", 16)
        self.font_emoji_hab = pg.font.SysFont("Segoe UI Emoji", 30) # Fonte para os ícones das habilidades
        self.font_button = pg.font.SysFont("Courier New", 30, bold=True)
        self.clock = pg.time.Clock()

        self.botoes = {
            "voltar": pg.Rect(390, 680, 220, 70),
            "selecionar": pg.Rect(670, 680, 220, 70)
        }

    def desenhar(self):
        # --- Fundo escuro semi-transparente ---
        overlay = pg.Surface((1280, 768))  # tamanho da tela
        overlay.set_alpha(180)  # 0 = transparente, 255 = opaco
        overlay.fill((0, 0, 0))  # cor preta
        self.window.blit(overlay, (0, 0))

        # --- Janela do modal ---
        modal_width, modal_height = 1100, 700
        modal_rect = pg.Rect(90, 30, modal_width, modal_height)
        pg.draw.rect(self.window, (30, 30, 30), modal_rect, border_radius=15)  # fundo escuro do modal
        pg.draw.rect(self.window, (200, 200, 200), modal_rect, 3, border_radius=15)  # borda clara

        p = self.personagem

        # Título
        title = self.font_title.render(p["nome"], True, (255, 255, 255))
        self.window.blit(title, (130, 70))

        # Descrição
        descricao = self.font_text.render(p["descricao"], True, (255, 255, 255))
        self.window.blit(descricao, (130, 140))

        # Imagem proporcional
        imagem = scale_proporcional(p["imagem"], 300, 200)
        img_rect = imagem.get_rect()

        # Posiciona o centro da imagem a 20% da largura do modal
        img_rect.centerx = modal_rect.left + int(modal_rect.width * 0.2)

        # Limita para não sair da borda superior do modal
        img_rect.top = modal_rect.top + 180


        self.window.blit(imagem, img_rect)


        # Características
        for i, c in enumerate(p["caracteristicas"]):
            text = self.font_text.render(f"{c}", True, (200, 255, 200))
            self.window.blit(text, (500, 210 + i * 40))
        

        for i, habilidade in enumerate(p["habilidades"]):
            # --- Ícone da Habilidade (usando o emoji) ---
            # Agora lê diretamente da chave 'icone'
            icon_surf = self.font_emoji_hab.render(habilidade['icone'], True, (220, 220, 220))
            icon_rect = icon_surf.get_rect(center=(210, 465 + i * 50))
            self.window.blit(icon_surf, icon_rect)

            # --- Textos da Habilidade ---
            hab_name = self.font_hab.render(f"{habilidade['nome']}", True, (228, 120, 51))
            hab_type = self.font_hab.render(f"{habilidade['tipo']}", True, (0, 0, 255))
            hab_description = self.font_hab.render(f"{habilidade['descricao']}", True, (255, 255, 255))
            hab_cooldown = self.font_hab.render(f"{habilidade['cooldown']}", True, (255, 255, 0))
            gap = i * 50
            self.window.blit(hab_name, (240, 445 + gap))
            self.window.blit(hab_type, (880, 445 + gap))
            self.window.blit(hab_cooldown, (1020, 445 + gap))
            self.window.blit(hab_description, (240, 464 + gap))

        # Botões
        mouse = pg.mouse.get_pos()
        for name, rect in self.botoes.items():
            color = (100, 180, 100)
            if rect.collidepoint(mouse):
                color = (150, 255, 150)
            pg.draw.rect(self.window, color, rect, border_radius=12)
            label = self.font_button.render(name.upper(), True, (0, 0, 0))
            self.window.blit(label, label.get_rect(center=rect.center))

        pg.display.update()
        self.clock.tick(60)

    def checar_clique(self, pos):
        if self.botoes["voltar"].collidepoint(pos):
            return "personagens"
        if self.botoes["selecionar"].collidepoint(pos):
            return "selecionar"
        return None

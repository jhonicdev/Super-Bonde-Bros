import pygame as pg
from mapa import Mapa
from utils import scale_proporcional

class MenuInicial:
    def __init__(self, window, personagem_selecionado=None):
        self.window = window
        self.personagem_selecionado = personagem_selecionado

        self.font_title = pg.font.SysFont("Courier New", 80, bold=True)
        self.font_button = pg.font.SysFont("Courier New", 40, bold=True)
        self.font_text = pg.font.SysFont("Courier New", 30, bold=True)
        self.font_footer = pg.font.SysFont("Courier New", 20, bold=True)

        self.white = (255, 255, 255)
        self.purple_dark = (100, 100, 180)
        self.green_light = (150, 255, 150)

        self.mapa = Mapa()
        self.clock = pg.time.Clock()

        self.buttons = {
            "start": pg.Rect(490, 320, 300, 70),
            "config": pg.Rect(490, 420, 300, 70),
            "personagens": pg.Rect(490, 520, 300, 70)
        }

        self.next_screen = None

    def desenhar(self, personagem=None):
        self.mapa.draw_background(self.window)
        
        # --- Título ---
        title = self.font_title.render("SUPER BONDE BROS.", True, self.white)
        self.window.blit(title, (220, 140))
        
        # --- Rodapé ---
        footer = self.font_footer.render("Developed by Jônatas Cunha", True, self.white)
        self.window.blit(footer, (484, 700))
        version = self.font_footer.render("v0.1", True, self.white)
        self.window.blit(version, (1200, 700))

        # --- Personagem selecionado ---
        if personagem:
            # Escala proporcional da imagem (mantendo proporção dentro de 300x250)
            img_surf = scale_proporcional(personagem.menu_icon, 300, 200)
            img_rect = img_surf.get_rect()

            largura_tela, altura_tela = self.window.get_size()
            
            # Define centro do personagem
            center_x = int(largura_tela * 0.2)
            center_y = int(altura_tela * 0.6)
            img_rect.center = (center_x, center_y)

            # --- Fundo fixo atrás do personagem ---
            fundo_largura, fundo_altura = 280, 320  # tamanho fixo do fundo
            fundo_rect = pg.Rect(
                center_x - fundo_largura // 2,
                center_y - fundo_altura // 2,
                fundo_largura,
                fundo_altura
            )
            # Desenha fundo escuro
            pg.draw.rect(self.window, (100, 100, 160), fundo_rect, border_radius=12)
            # Desenha borda clara
            pg.draw.rect(self.window, (200, 200, 255), fundo_rect, 3, border_radius=12)

            # Desenha a imagem do personagem
            self.window.blit(img_surf, img_rect)

            # Nome do personagem abaixo da imagem
            name_text = self.font_text.render(personagem.name.upper(), True, self.white)
            name_rect = name_text.get_rect(midtop=(center_x, img_rect.bottom + 10))
            self.window.blit(name_text, name_rect.topleft)


        # --- Botões ---
        mouse_pos = pg.mouse.get_pos()
        for name, rect in self.buttons.items():
            color = self.purple_dark
            if rect.collidepoint(mouse_pos):
                color = (150, 150, 255)  # hover
            pg.draw.rect(self.window, color, rect, border_radius=12)

            if name == "start":
                label = "INICIAR"
            elif name == "config":
                label = "CONFIGURAR"
            elif name == "personagens":
                label = "PERSONAGENS"

            text = self.font_button.render(label, True, self.green_light)
            text_rect = text.get_rect(center=rect.center)
            self.window.blit(text, text_rect)

        pg.display.update()
        self.clock.tick(60)


    def checar_clique(self, mouse_pos):
        for name, rect in self.buttons.items():
            if rect.collidepoint(mouse_pos):
                return name  # retorna o botão clicado
        return None

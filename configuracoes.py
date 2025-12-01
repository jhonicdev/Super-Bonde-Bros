import pygame as pg
from mapa import Mapa

class TelaConfiguracoes:
    def __init__(self, window):
        self.window = window
        self.font_title = pg.font.SysFont("Courier New", 60, bold=True)
        self.font_button = pg.font.SysFont("Courier New", 40, bold=True)
        self.mapa = Mapa()
        self.clock = pg.time.Clock()

        self.buttons = {
            "voltar": pg.Rect(490, 600, 300, 70)
        }

    def desenhar(self):
        title = self.font_title.render("CONFIGURAÇÕES", True, (255, 255, 255))
        self.window.blit(title, (400, 200))

        mouse_pos = pg.mouse.get_pos()
        for name, rect in self.buttons.items():
            color = (100, 100, 180)
            if rect.collidepoint(mouse_pos):
                color = (150, 150, 255)
            pg.draw.rect(self.window, color, rect, border_radius=12)
            text = self.font_button.render(name.upper(), True, (180, 255, 180))
            self.window.blit(text, text.get_rect(center=rect.center))

        pg.display.update()
        self.clock.tick(60)

    def checar_clique(self, mouse_pos):
        if self.buttons["voltar"].collidepoint(mouse_pos):
            return "menu"
        return None

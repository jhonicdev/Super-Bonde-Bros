import pygame as pg
from mapa import Mapa
from personagens_data import DadosPersonagens
from utils import scale_proporcional


class TelaPersonagens:
    def __init__(self, window):
        self.window = window
        self.font_title = pg.font.SysFont("Courier New", 60, bold=True)
        self.font_name = pg.font.SysFont("Courier New", 26, bold=True)
        self.font_button = pg.font.SysFont("Courier New", 30, bold=True)
        self.mapa = Mapa()
        self.clock = pg.time.Clock()
        self.dados = DadosPersonagens()

        # Posições automáticas para os ícones
        self.espacamento_x = 250
        self.base_y = 300

        self.botoes = {}
        for i, p in enumerate(self.dados.personagens):
            rect = pg.Rect(300 + i * self.espacamento_x, self.base_y, 180, 180)
            self.botoes[p["nome"]] = rect

        self.botao_voltar = pg.Rect(525, 650, 220, 70)

    def desenhar(self):
        title = self.font_title.render("ESCOLHA SEU PERSONAGEM", True, (255, 255, 255))
        self.window.blit(title, (250, 150))

        mouse_pos = pg.mouse.get_pos()
        for p in self.dados.personagens:
            rect = self.botoes[p["nome"]]
            color = (100, 100, 180)
            if rect.collidepoint(mouse_pos):
                color = (150, 150, 255)
            pg.draw.rect(self.window, color, rect, border_radius=12)

            # Ícone centralizado
            icon = scale_proporcional(p["icone"], 180, 120)
            self.window.blit(icon, icon.get_rect(center=(rect.centerx, rect.centery - 20)))

            # Nome do personagem
            nome = p["nome"]
            if len(nome) > 7:
                nome = p["nome"][0] + ". " + p["nome"].split(" ")[-1]
            text = self.font_name.render(nome.upper(), True, (255, 255, 255))
            self.window.blit(text, text.get_rect(center=(rect.centerx, rect.bottom - 20)))

        # Botão Voltar
        color = (100, 180, 100)
        if self.botao_voltar.collidepoint(mouse_pos):
            color = (150, 255, 150)
        pg.draw.rect(self.window, color, self.botao_voltar, border_radius=12)
        text = self.font_button.render("VOLTAR", True, (0, 0, 0))
        self.window.blit(text, text.get_rect(center=self.botao_voltar.center))

        pg.display.update()
        self.clock.tick(60)

    def checar_clique(self, pos):
        if self.botao_voltar.collidepoint(pos):
            return "menu"

        for p in self.dados.personagens:
            if self.botoes[p["nome"]].collidepoint(pos):
                return ("info_personagem", p)
        return None

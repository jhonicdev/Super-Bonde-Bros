import pygame as pg
from mapa import Mapa

class TelaConfiguracoes:
    def __init__(self, window):
        self.window = window
        self.font_title = pg.font.SysFont("Courier New", 60, bold=True)
        self.font_button = pg.font.SysFont("Courier New", 40, bold=True)
        self.font_label = pg.font.SysFont("Courier New", 30, bold=True)
        self.mapa = Mapa()
        self.clock = pg.time.Clock()

        self.buttons = {
            "voltar": pg.Rect(490, 600, 300, 70)
        }
        
        # Botões de controle de música
        self.btn_prev = pg.Rect(380, 350, 70, 70)
        self.btn_next = pg.Rect(830, 350, 70, 70)

        # Opções de música
        self.musicas = [
            {"titulo": "NENHUMA", "autor": "", "arquivo": None},
            {"titulo": "Inquilino das Prisões", "autor": "Edson Gomes", "arquivo": "./Musics/Inquilino das Prisões.mp3"},
            {"titulo": "Saudação à Mandioca", "autor": "Dilma, Timbu Fun", "arquivo": "./Musics/Saudação à Mandioca (Remix).mp3"},
            {"titulo": "Mosquita", "autor": "Dilma, Timbu Fun", "arquivo": "./Musics/Mosquita (Remix).mp3"},
            {"titulo": "Só Quero Dinheiro (Não Quero Amar)", "autor": "Tim Maia, Estragona - Lado B", "arquivo": "./Musics/Só Quero Dinheiro (Remix).mp3"},
            {"titulo": "Dúvidas", "autor": "Chitãozinho & Xororó, NotCami Speedruns", "arquivo": "./Musics/Evidências (Remix).mp3"},
        ]
        self.indice_musica = 1

        self.aplicar_musica()

    def desenhar(self):
        title = self.font_title.render("CONFIGURAÇÕES", True, (255, 255, 255))
        self.window.blit(title, (400, 100))

        mouse_pos = pg.mouse.get_pos()
        
        # --- Seção de Música ---
        label_musica = self.font_label.render("MÚSICA DO LOBBY", True, (200, 200, 200))
        self.window.blit(label_musica, label_musica.get_rect(center=(640, 300)))

        # Info da música atual
        musica = self.musicas[self.indice_musica]
        titulo = musica["titulo"]
        autor = musica["autor"]
        
        # Largura máxima disponível entre as setas (aprox. 360px)
        max_w = 360

        # Renderiza Título (com redimensionamento se exceder largura)
        surf_titulo = self.font_button.render(titulo, True, (255, 255, 100))
        if surf_titulo.get_width() > max_w:
            ratio = max_w / surf_titulo.get_width()
            surf_titulo = pg.transform.smoothscale(surf_titulo, (max_w, int(surf_titulo.get_height() * ratio)))

        # Posicionamento
        if autor:
            self.window.blit(surf_titulo, surf_titulo.get_rect(center=(640, 370)))
            
            surf_autor = self.font_label.render(autor, True, (200, 200, 200))
            if surf_autor.get_width() > max_w:
                ratio = max_w / surf_autor.get_width()
                surf_autor = pg.transform.smoothscale(surf_autor, (max_w, int(surf_autor.get_height() * ratio)))
            self.window.blit(surf_autor, surf_autor.get_rect(center=(640, 410)))
        else:
            self.window.blit(surf_titulo, surf_titulo.get_rect(center=(640, 385)))

        # Botões de seta
        for btn, symbol in [(self.btn_prev, "<"), (self.btn_next, ">")]:
            color = (100, 100, 180)
            if btn.collidepoint(mouse_pos):
                color = (150, 150, 255)
            pg.draw.rect(self.window, color, btn, border_radius=12)
            text_sym = self.font_button.render(symbol, True, (255, 255, 255))
            self.window.blit(text_sym, text_sym.get_rect(center=btn.center))

        # --- Botões Genéricos ---
        for name, rect in self.buttons.items():
            color = (100, 100, 180)
            if rect.collidepoint(mouse_pos):
                color = (150, 150, 255)
            pg.draw.rect(self.window, color, rect, border_radius=12)
            text = self.font_button.render(name.upper(), True, (180, 255, 180))
            self.window.blit(text, text.get_rect(center=rect.center))

        pg.display.update()
        self.clock.tick(60)

    def aplicar_musica(self):
        selecao = self.musicas[self.indice_musica]
        arquivo = selecao["arquivo"]
        
        if arquivo:
            try:
                pg.mixer.music.load(arquivo)
                pg.mixer.music.play(-1)
                pg.mixer.music.set_volume(0.5)
            except pg.error:
                print(f"Erro ao carregar música: {arquivo}")
        else:
            pg.mixer.music.stop()

    def checar_clique(self, mouse_pos):
        if self.buttons["voltar"].collidepoint(mouse_pos):
            return "menu"
        
        if self.btn_prev.collidepoint(mouse_pos):
            self.indice_musica = (self.indice_musica - 1) % len(self.musicas)
            self.aplicar_musica()
        elif self.btn_next.collidepoint(mouse_pos):
            self.indice_musica = (self.indice_musica + 1) % len(self.musicas)
            self.aplicar_musica()
            
        return None

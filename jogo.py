import pygame as pg
from mapa import Mapa
from personagem_base import Jogador

class SuperBondeBros:
    def __init__(self):
        # --- Cores ---
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)

        # --- Janela e clock ---
        self.window = pg.display.set_mode((1280, 768))
        pg.font.init()
        self.font = pg.font.SysFont("Courier New", 50, bold=True)
        self.clock = pg.time.Clock()

        # --- Mapa ---
        self.map = Mapa()
        self.tile_size = 64
        self.map_width = len(self.map.tiles[0]) * self.tile_size
        self.map_height = len(self.map.tiles) * self.tile_size

        # --- Jogador ---
        self.player = Jogador(300, 600)

        # --- Estado ---
        self.last_click_status = (False, False, False)

        # --- Câmera ---
        self.camera_x = 0
        self.screen_width = 1280
        self.half_screen = self.screen_width // 2

    # ----------------------------------------------------------------------
    def mouse_has_clicked(self, input):
        left = not self.last_click_status[0] and input[0]
        middle = not self.last_click_status[1] and input[1]
        right = not self.last_click_status[2] and input[2]
        return (left, middle, right)

    # ----------------------------------------------------------------------
    def background_imgs(self):
        """Desenha o fundo com base na câmera"""
        self.map.draw_background(self.window, self.camera_x)

    # ----------------------------------------------------------------------
    def tiles(self):
        """Desenha os blocos com base na câmera"""
        self.map.draw_tiles(self.window, self.camera_x)

    # ----------------------------------------------------------------------
    def move(self, keys):
        """Movimenta o jogador conforme entrada do teclado"""
        self.player.mover(keys, self.map.tiles)

    # ----------------------------------------------------------------------
    def atualizar_jogador(self):
        """Atualiza física, câmera e renderização do jogador"""
        self.player.atualizar(self.map.tiles)
        self.atualizar_camera()
        self.player.desenhar(self.window, offset_x=self.camera_x)

    # ----------------------------------------------------------------------
    def atualizar_camera(self):
        """Mantém o jogador centralizado e limita nas bordas"""
        player_center = self.player.pos[0] + 64  # centro do personagem
        self.camera_x = player_center - self.half_screen

        # Limites: não passar das bordas do mapa
        if self.camera_x < 0:
            self.camera_x = 0
        elif self.camera_x > self.map_width - self.screen_width:
            self.camera_x = self.map_width - self.screen_width

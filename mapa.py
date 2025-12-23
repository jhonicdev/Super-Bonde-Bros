import pygame as pg
import random
import math

CHUNK_SIZE = 10  # Número de tiles por chunk horizontal
TILE_SIZE = 64   # Tamanho de cada tile

# Importa as classes dos vilões para que o mapa possa criá-los
from viloes.carangueijo.carangueijo import Carangueijo
from viloes.morcego.morcego import Morcego

class Mapa:
    def __init__(self):
        # --- Tiles do mapa (exemplo inicial) ---
        self.tiles = [
            "                                                                                                                                                                                ",
            "                                                                                                                                                                                ",
            "                                                                                                                                                                                ",
            "                                                                                                                                                                                ",
            "                                                                                                                                                                                ",
            "                                                                                                                                                                                ",
            "                                                                                                                                                                                ",
            "                   13 1223                                                                                                                                                      ",
            "               123 79 45552223                                                                                                                                                  ",
            "          123  789    45555556                                                                                                                                                  ",
            "     1223 456         45555556                                                                                                                                                  ",
            "22222555525552222222225555555522222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222"
        ]
        self.tiles = [list(row) for row in self.tiles]

        # --- Fundo fixo ---
        self.background = pg.transform.scale(
            pg.image.load('./Sprites/Palm Tree Island/Background/BG Image.png').convert(),
            (1280, 768)
        )

        # --- Nuvens ---
        self.big_clouds = pg.transform.scale(pg.image.load('./Sprites/Palm Tree Island/Background/Big Clouds.png').convert_alpha(), (896, 202))
        self.small_cloud_1 = pg.transform.scale(pg.image.load('./Sprites/Palm Tree Island/Background/Small Cloud 1.png').convert_alpha(), (148, 48))
        self.small_cloud_2 = pg.transform.scale(pg.image.load('./Sprites/Palm Tree Island/Background/Small Cloud 2.png').convert_alpha(), (266, 70))
        self.small_cloud_3 = pg.transform.scale(pg.image.load('./Sprites/Palm Tree Island/Background/Small Cloud 3.png').convert_alpha(), (280, 78))
        self.cloud_offset = 0
        self.cloud_speed = 0.1

        # --- Água animada ---
        self.big_water = [pg.transform.scale(pg.image.load(f'./Sprites/Palm Tree Island/Background/Water Reflect Big 0{i}.png').convert_alpha(), (340, 20)) for i in range(1,5)]
        self.medium_water = [pg.transform.scale(pg.image.load(f'./Sprites/Palm Tree Island/Background/Water Reflect Medium 0{i}.png').convert_alpha(), (106, 6)) for i in range(1,5)]
        self.small_water = [pg.transform.scale(pg.image.load(f'./Sprites/Palm Tree Island/Background/Water Reflect Small 0{i}.png').convert_alpha(), (70, 6)) for i in range(1,5)]
        self.big_water_frame = 0
        self.medium_water_frame = 0
        self.small_water_frame = 0

        # --- Terreno ---
        self.ground = [pg.transform.scale(pg.image.load(f'./Sprites/Palm Tree Island/Terrain/ground_{i}.png').convert_alpha(), (TILE_SIZE, TILE_SIZE)) for i in range(1,10)]

        # --- Cache de chunks ---
        self.chunk_surfaces = {}

        self.map_width = len(self.tiles[0]) * TILE_SIZE
        self.map_height = len(self.tiles) * TILE_SIZE

        # --- Dados dos Vilões (específico para este mapa) ---
        # No futuro, isso pode ser carregado de um arquivo de mapa (JSON, TMX, etc.)
        self.dados_viloes = [
            {'tipo': 'Carangueijo', 'x': 800, 'y': 600},
            {'tipo': 'Morcego', 'x': 800, 'y': 450},
            {'tipo': 'Morcego', 'x': 1200, 'y': 400},
            {'tipo': 'Carangueijo', 'x': 1200, 'y': 500},
            {'tipo': 'Carangueijo', 'x': 1500, 'y': 500},
            {'tipo': 'Morcego', 'x': 1800, 'y': 450},
            {'tipo': 'Carangueijo', 'x': 1900, 'y': 500},
            {'tipo': 'Morcego', 'x': 2000, 'y': 500},
            {'tipo': 'Morcego', 'x': 2400, 'y': 500},
            {'tipo': 'Carangueijo', 'x': 2500, 'y': 500},
            {'tipo': 'Carangueijo', 'x': 2600, 'y': 500},
            {'tipo': 'Morcego', 'x': 2700, 'y': 500},
            {'tipo': 'Carangueijo', 'x': 2800, 'y': 500},
            {'tipo': 'Carangueijo', 'x': 2900, 'y': 500},
            {'tipo': 'Carangueijo', 'x': 3000, 'y': 500},
            {'tipo': 'Morcego', 'x': 3200, 'y': 500},
            {'tipo': 'Carangueijo', 'x': 3300, 'y': 500},
            {'tipo': 'Carangueijo', 'x': 3400, 'y': 500},
            {'tipo': 'Morcego', 'x': 3500, 'y': 500},
            {'tipo': 'Carangueijo', 'x': 3600, 'y': 500},
            {'tipo': 'Morcego', 'x': 3700, 'y': 500},
            {'tipo': 'Carangueijo', 'x': 3800, 'y': 500},
            {'tipo': 'Morcego', 'x': 3900, 'y': 500},
            {'tipo': 'Carangueijo', 'x': 4000, 'y': 500},
            {'tipo': 'Morcego', 'x': 4200, 'y': 500},
            {'tipo': 'Carangueijo', 'x': 4300, 'y': 500},
        ]

        # Mapeamento de strings para classes de vilões
        self.classes_viloes = {
            'Carangueijo': Carangueijo,
            'Morcego': Morcego
        }

    # ----------------------------------------------------------------------
    def get_chunk_surface(self, chunk_index):
        """Cria ou retorna a superfície de um chunk."""
        if chunk_index in self.chunk_surfaces:
            return self.chunk_surfaces[chunk_index]

        start_x = chunk_index * CHUNK_SIZE
        end_x = min(start_x + CHUNK_SIZE, len(self.tiles[0]))
        width = (end_x - start_x) * TILE_SIZE
        height = len(self.tiles) * TILE_SIZE
        surface = pg.Surface((width, height), pg.SRCALPHA)

        for y, row in enumerate(self.tiles):
            for x in range(start_x, end_x):
                t = row[x]
                if t != ' ':
                    surface.blit(self.ground[int(t)-1], ((x - start_x) * TILE_SIZE, y * TILE_SIZE))

        self.chunk_surfaces[chunk_index] = surface
        return surface

    # ----------------------------------------------------------------------
    def draw_background(self, window, camera_x=0, mover_nuvens=False):
        """Desenha fundo fixo com nuvens animadas e água. Nuvens só se movem se mover_nuvens=True."""
        window.blit(self.background, (0, 0))  # fundo fixo

        # Atualiza offset das nuvens apenas se jogador se moveu
        if mover_nuvens:
            self.cloud_offset += self.cloud_speed

        # Nuvens grandes
        for i in range(-1, 3):
            x_pos = i * 896 - (self.cloud_offset % 896)
            window.blit(self.big_clouds, (int(x_pos - camera_x * 0.1), 315))

        # Nuvens pequenas
        small_offsets = [self.cloud_offset*0.5, self.cloud_offset*0.3, self.cloud_offset*0.2]
        for i in range(-1, 3):
            x_pos = i * 1500 - (small_offsets[0] % 1500)
            window.blit(self.small_cloud_1, (int(x_pos - camera_x * 0.05), 100))
            x_pos = i * 1500 - (small_offsets[1] % 1500)
            window.blit(self.small_cloud_2, (int(x_pos - camera_x * 0.03), 200))
            x_pos = i * 1500 - (small_offsets[2] % 1500)
            window.blit(self.small_cloud_3, (int(x_pos - camera_x * 0.02), 250))

        # Água animada
        window.blit(self.big_water[int(self.big_water_frame // 12)], (300, 550))
        window.blit(self.medium_water[int(self.medium_water_frame // 12)], (250, 600))
        window.blit(self.small_water[int(self.small_water_frame // 12)], (1000, 600))

        # Atualiza frames da água
        self.big_water_frame = (self.big_water_frame + 1) % 48
        self.medium_water_frame = (self.medium_water_frame + 1) % 48
        self.small_water_frame = (self.small_water_frame + 1) % 48

    # ----------------------------------------------------------------------
    def draw_tiles(self, window, camera_x=0):
        """Desenha apenas tiles visíveis usando chunks."""
        start_chunk = int(max(camera_x // (CHUNK_SIZE * TILE_SIZE), 0))
        end_chunk = int((camera_x + 1280) // (CHUNK_SIZE * TILE_SIZE) + 1)

        for chunk_index in range(start_chunk, end_chunk):
            chunk_surface = self.get_chunk_surface(chunk_index)
            window.blit(chunk_surface, (chunk_index * CHUNK_SIZE * TILE_SIZE - camera_x, 0))

    # ----------------------------------------------------------------------
    def carregar_viloes(self):
        """Cria e retorna uma lista de instâncias de vilões com base nos dados do mapa."""
        lista_viloes = []
        for dados_vilao in self.dados_viloes:
            tipo_vilao = dados_vilao['tipo']
            if tipo_vilao in self.classes_viloes:
                classe = self.classes_viloes[tipo_vilao]
                vilao = classe(x=dados_vilao['x'], y=dados_vilao['y'])
                lista_viloes.append(vilao)
        return lista_viloes

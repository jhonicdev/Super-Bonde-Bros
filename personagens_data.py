# personagens_data.py
import pygame as pg

class DadosPersonagens:
    def __init__(self):
        # --- Helper para gerar ícones customizados ---
        def criar_icone_pi(cor=(0, 255, 255)):
            font_pi = pg.font.SysFont("Times New Roman", 35, bold=True)
            surf_texto = font_pi.render("π", True, cor)
            surf_borda = font_pi.render("π", True, (0, 0, 0))
            w, h = surf_texto.get_size()
            surf = pg.Surface((w + 4, h + 4), pg.SRCALPHA)
            for ox, oy in [(-1,0), (1,0), (0,-1), (0,1), (-1,-1), (1,1), (-1,1), (1,-1)]:
                surf.blit(surf_borda, (2 + ox, 2 + oy))
            surf.blit(surf_texto, (2, 2))
            return surf
        
        def carregar_recortado(path):
            try:
                img = pg.image.load(path).convert_alpha()
                rect = img.get_bounding_rect()
                return img.subsurface(rect).copy()
            except Exception:
                return pg.Surface((64, 64))

        icone_pi_img = criar_icone_pi()
        icone_pi_critico_img = criar_icone_pi((255, 215, 0))

        # Carrega ícone da OBMEP
        try:
            icone_obmep = pg.image.load('./personagens/dr_pi/sprites/abilities/obmep.png').convert_alpha()
            
            # Recorta apenas a área visível (remove bordas transparentes)
            rect_visivel = icone_obmep.get_bounding_rect()
            icone_obmep = icone_obmep.subsurface(rect_visivel).copy()
            
            # Redimensiona mantendo proporção para caber em 40x40 (tamanho aprox do ícone na info)
            w, h = icone_obmep.get_size()
            scale = min(40/w, 40/h)
            icone_obmep = pg.transform.scale(icone_obmep, (int(w*scale), int(h*scale)))
        except Exception:
            icone_obmep = "📚"

        self.personagens = [
            {
                "nome": "Capitão Clown Nose",
                "descricao": "Um pirata astuto e ágil. Ilusionista nas horas vagas.",
                "caracteristicas": [
                    "ATAQUE: 🟥🟥🟥🟥🟥🟥",
                    "DEFESA: 🟩🟩🟩🟩🟩",
                    "UTILIDADE: 🟦🟦🟦",
                    "PULO: 🟨🟨🟨🟨🟨🟨🟨🟨",
                    "VELOCIDADE: 🟧🟧🟧🟧🟧🟧🟧",
                ],
                "habilidades": [
                    {
                        "nome": "Saco de moedas",
                        "icone": "💰️",
                        "tipo": "Ataque básico",
                        "descricao": "Um saco de ouro voa como projétil improvisado. Ele literalmente luta jogando dinheiro fora.",
                        "cooldown": "0,5s"
                    },
                    {
                        "nome": "Lapada seca!",
                        "icone": "⚓",
                        "tipo": "Ativa",
                        "descricao": "Arremessa sua âncora como um bumerangue brutal (surpreendentemente ágil para algo tão pesado)!",
                        "cooldown": "15s"
                    },
                    {
                        "nome": "Tripulação fantasma",
                        "icone": "👻",
                        "tipo": "Ativa",
                        "descricao": "Invoca um tripulante fantasma que luta ao seu lado por breves instantes.",
                        "cooldown": "40s"
                    }
                ],
                "icone": carregar_recortado("./personagens/capitao_clown_nose/sprites/idle/Idle 1.png"),
                "imagem": carregar_recortado("./personagens/capitao_clown_nose/sprites/idle/Idle 1.png")
            },
            {
                "nome": "Dr. PI",
                "descricao": "Um gênio matemático. Costuma resolver seus problemas de maneira irracional.",
                "caracteristicas": [
                    "ATAQUE: 🟥🟥🟥🟥🟥🟥🟥🟥",
                    "DEFESA: 🟩🟩",
                    "UTILIDADE: 🟦🟦🟦🟦🟦🟦🟦🟦",
                    "PULO: 🟨🟨🟨🟨🟨🟨🟨",
                    "VELOCIDADE: 🟧🟧🟧🟧🟧🟧🟧🟧🟧🟧",
                ],
                "habilidades": [
                    {
                        "nome": "Pi",
                        "icone": icone_pi_img,
                        "tipo": "Ataque básico",
                        "descricao": "Lança um Pi bem na cara nos oponentes. QED.",
                        "cooldown": "0,5s"
                    },
                    {
                        "nome": "Trigonometricamente",
                        "icone": "📈",
                        "tipo": "Ativa",
                        "descricao": "A função seno causa dano horizontal nos oponentes enquanto o Dr. PI dá um salto pegando carona na função cosseno!",
                        "cooldown": "20s"
                    },
                    {
                        "nome": "Proteção OBMÉPICA!",
                        "icone": icone_obmep,
                        "tipo": "Ativa",
                        "descricao": "Dr. PI agora fica protegido pelo aura OBMÉPICA por 8 segundos, repelindo qualquer oponente que ousar em se aproximar!",
                        "cooldown": "40s"
                    },
                    {
                        "nome": "Só pode ser Pi-ada...",
                        "icone": icone_pi_critico_img,
                        "tipo": "Passiva",
                        "descricao": "O ataque básico do Dr. PI possui 3,14% de probabilidade de causar 3,14 vezes mais dano que o normal.",
                        "cooldown": "Nenhum"
                    }
                ],
                "icone": carregar_recortado("./personagens/dr_pi/sprites/idle/Idle 1.png"),
                "imagem": carregar_recortado("./personagens/dr_pi/sprites/idle/Idle 1.png")
            },
            {
                "nome": "João Poker",
                "descricao": "Um duelista calmo na maior parte das vezes. Tem um lado excessivamente risonho.",
                "caracteristicas": [
                    "ATAQUE: 🟥🟥🟥🟥🟥🟥🟥",
                    "DEFESA: 🟩🟩🟩🟩🟩🟩🟩",
                    "UTILIDADE: 🟦🟦🟦🟦🟦🟦🟦",
                    "PULO: 🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨",
                    "VELOCIDADE: 🟧🟧🟧🟧",
                ],
                "habilidades": [
                    {
                        "nome": "Embaralhar",
                        "icone": "🔄",
                        "tipo": "Ataque básico",
                        "descricao": "Arremessa uma carta afiada com precisão absurda.",
                        "cooldown": "0,2s"
                    },
                    {
                        "nome": "KABOOM!",
                        "icone": "💥",
                        "tipo": "Ativa",
                        "descricao": "Explode o chão e sai voando junto. Por que não?",
                        "cooldown": "15s"
                    },
                    {
                        "nome": "WILD CARD!",
                        "icone": "🃏",
                        "tipo": "Ativa",
                        "descricao": "O Coringa assume o comando por 10 segundos!",
                        "cooldown": "80s"
                    }
                ],
                "icone": carregar_recortado('./personagens/joao_poker/sprites/idle/slendytubbie.png'),
                "imagem": carregar_recortado('./personagens/joao_poker/sprites/idle/slendytubbie.png')
            }
        ]

# personagens_data.py
import pygame as pg

class DadosPersonagens:
    def __init__(self):
        self.personagens = [
            {
                "nome": "Capitão Clown Nose",
                "descricao": "Um pirata astuto e ágil. Ilusionista nas horas vagas.",
                "caracteristicas": [
                    "ATAQUE: 🟥🟥🟥🟥🟥",
                    "DEFESA: 🟩🟩🟩🟩",
                    "UTILIDADE: 🟦🟦🟦",
                    "PULO: 🟨🟨🟨🟨🟨🟨🟨🟨🟨",
                    "VELOCIDADE: 🟧🟧🟧🟧🟧🟧🟧",
                ],
                "habilidades": [
                    {
                        "nome": "Saco de Moedas",
                        "icone": "💰️",
                        "tipo": "Ataque básico",
                        "descricao": "Um saco de ouro voa como projétil improvisado. Ele literalmente luta jogando dinheiro fora.",
                        "cooldown": "0,5s"
                    },
                    {
                        "nome": "Lapada seca",
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
                "icone": pg.image.load("./personagens/capitao_clown_nose/sprites/idle/Idle 1.png"),
                "imagem": pg.image.load("./personagens/capitao_clown_nose/sprites/idle/Idle 1.png")
            },
            {
                "nome": "João Poker",
                "descricao": "Um duelista calmo na maior parte das vezes. Tem um lado excessivamente risonho.",
                "caracteristicas": [
                    "ATAQUE: 🟥🟥🟥🟥🟥🟥🟥",
                    "DEFESA: 🟩🟩🟩🟩🟩🟩🟩",
                    "UTILIDADE: 🟦🟦🟦🟦🟦🟦🟦",
                    "PULO: 🟨🟨🟨🟨🟨🟨🟨",
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
                "icone": pg.image.load(f'./personagens/joao_poker/sprites/idle/slendytubbie.png'),
                "imagem": pg.image.load(f'./personagens/joao_poker/sprites/idle/slendytubbie.png')
            },
            {
                "nome": "Dr. PI",
                "descricao": "Um gênio matemático. Costuma resolver seus problemas de maneira irracional.",
                "caracteristicas": [
                    "ATAQUE: 🟥🟥🟥🟥🟥🟥🟥",
                    "DEFESA: 🟩🟩",
                    "UTILIDADE: 🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦",
                    "PULO: 🟨🟨🟨🟨",
                    "VELOCIDADE: 🟧🟧🟧🟧🟧🟧🟧🟧🟧",
                ],
                "habilidades": [
                    {
                        "nome": "Pi-raio",
                        "icone": "π",
                        "tipo": "Ataque básico",
                        "descricao": "Dispara um raio de energia irracional.",
                        "cooldown": "1s"
                    },
                    {
                        "nome": "Raiz dos problemas",
                        "icone": "√",
                        "tipo": "Ativa",
                        "descricao": "Invoca raízes do chão que prendem inimigos.",
                        "cooldown": "10s"
                    },
                    {
                        "nome": "Inversão de sinais",
                        "icone": "±",
                        "tipo": "Ativa",
                        "descricao": "Cria um campo que reflete projéteis inimigos.",
                        "cooldown": "50s"
                    }
                ],
                "icone": pg.image.load(f'./personagens/dr_pi/sprites/idle/dilma.png'),
                "imagem": pg.image.load(f'./personagens/dr_pi/sprites/idle/dilma.png')
            }
        ]

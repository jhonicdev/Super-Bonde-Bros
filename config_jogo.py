# config_jogo.py

"""
Arquivo central para todas as constantes de balanceamento do jogo.
Alterar valores aqui afetará o comportamento de personagens, habilidades e vilões.
"""

CONFIG = {
    'personagens': {
        'CapitaoClownNose': {
            'velocidade': 3.3,
            'forca_pulo': -23,
            'vida_max': 3200,
            'habilidades': {
                'SacoDeMoedas': {
                    'cooldown_s': 0.5,
                    'dano': 200,
                    'velocidade': 10,
                },
                'LapadaSeca': {
                    'cooldown_s': 15,
                    'dano': 450,
                    'velocidade': 8,
                    'velocidade_rotacao': 30,
                    'distancia_max': 500,
                },
                'TripulanteFantasma': {
                    'cooldown_s': 35,
                    'duracao_s': 13,
                    'raio_deteccao': 600,
                    'cooldown_ataque_s': 0.8,
                    'projetil': {
                        'dano': 30,
                        'velocidade': 6,
                        'raio': 21,
                        'duracao_s': 4,
                    }
                }
            }
        },
        # Configurações para JoaoPoker e DrPI podem ser adicionadas aqui no futuro.
    },
    'viloes': {
        'CarangueijoPirata': {
           'velocidade': 1.8,
           'vida_max': 1000,
           'forca_pulo': -18,
           'raio_deteccao': 400,
           'dano_contato': 250,
        },
        'Morcego': {
           'velocidade': 2.2,
           'vida_max': 400,
           'forca_pulo': 0, # Não pula
           'raio_deteccao': 600,
           'dano_contato': 350,
        }
    }
}
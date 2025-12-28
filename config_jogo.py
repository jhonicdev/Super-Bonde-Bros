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
                    'cooldown_s': 40,
                    'duracao_s': 13,
                    'raio_deteccao': 600,
                    'cooldown_ataque_s': 0.6,
                    'projetil': {
                        'dano': 200,
                        'velocidade': 7,
                        'raio': 20,
                        'duracao_s': 4,
                    }
                }
            }
        },
        'DrPI': {
            'velocidade': 4.3,
            'forca_pulo': -20,
            'vida_max': 1200,
            'habilidades': {
                'AtaqueBasico': {
                    'cooldown_s': 0.5,
                    'dano': 314,
                    'velocidade_x': 14,   # Impulso para o lado
                    'velocidade_y': -5,   # Impulso para cima
                    'gravidade': 0.5      # Gravidade do projétil
                },
                'Trigonometria': {
                    'cooldown_s': 20,
                    'dano': 800,
                    'duracao_s': 0.8, 
                    'amplitude_pulo': 10,
                    'frequencia_onda': 0.05,
                    'raio_ataque': 800,
                    'fade_in_s': 0.05,
                    'fade_out_s': 0.6
                },
                'ProtecaoObmepica': {
                    'cooldown_s': 40,
                    'duracao_s': 8,
                    'raio': 100,
                    'forca_repulsao': 12,
                    'fade_in_s': 0.5,
                    'fade_out_s': 0.5
                }
            }
        },
        # Configurações para JoaoPoker e DrPI podem ser adicionadas aqui no futuro.
    },
    'viloes': {
        'Carangueijo': {
           'velocidade': 1.8,
           'vida_max': 1000,
           'forca_pulo': -18,
           'raio_deteccao': 400,
           'dano_contato': 150,
           'cooldown_ataque': 0.4, # Tempo em segundos entre ataques
        },
        'Morcego': {
           'velocidade': 2.2,
           'vida_max': 400,
           'forca_pulo': 0, # Não pula
           'raio_deteccao': 600,
           'dano_contato': 350,
           'cooldown_ataque': 1.2,
        },
        'Slendytubbie': {
           'velocidade': 4,
           'vida_max': 800,
           'forca_pulo': -16,
           'raio_deteccao': 500,
           'dano_contato': 50,
           'cooldown_ataque': 0.2,
        }
    }
}
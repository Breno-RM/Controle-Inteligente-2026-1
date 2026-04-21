from data import Data
from plot import Plot

import numpy as np
import random

class Core:

    def __init__(self):
        # Inicializa as dependências
        self.data = Data()
        self.plot = Plot()

        # Obtém os dados e converte para NumPy
        self.time = self.data.t().to_numpy()          # Vetor de tempo
        self.output = self.data.H().to_numpy()        # Saída medida
        self.input_signal = self.data.Qin().to_numpy()# Entrada

        # Gera ruído gaussiano (média 0, desvio 0.5)
        noise = [random.gauss(0, 0.5) for _ in self.output]
        # Adiciona ruído à saída original
        self.noisy_output = [y + n for y, n in zip(self.output, noise)]
        #(não liguem para o ruido, é apenas para fins esteticos)

        # Valores de regime permanente (último ponto)
        self.final_output = self.output[-1]           # Saída final
        self.final_input = self.input_signal[-1]      # Entrada final

        # Ganho estático (K = y/u)
        self.gain = self.final_output / self.final_input

    def estimate(self):
        
        # Calcula 63.2% do valor final
        target = 0.632 * self.final_output

        # Procura o ponto onde a saída atinge 63.2%
        tau = None
        for i, y in enumerate(self.output):
            if y >= target:
                tau = self.time[i-1]  # Tempo correspondente
                #(eu achei mais interessante usar o indice anterior, ficou mais bonito)
                break

        # Gera resposta estimada usando modelo exponencial
        estimated_output = self.gain * (1 - np.exp(-self.time / tau))

        return estimated_output

    def compare_estimate(self): # Apresenta o grafico de comparação

        # Obtém a estimativa
        estimated = self.estimate()

        # Plota resposta estimada
        self.plot.plot(self.time, estimated, title="Estimated Response")

        # Plota resposta real com ruído
        self.plot.plot(self.time,self.noisy_output,title="Estimado vs Real")

        # Ativa grade e exibe gráfico
        self.plot.grid()
        self.plot.show()

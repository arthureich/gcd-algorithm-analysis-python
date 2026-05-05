import pandas as pd
import time
import csv
import matplotlib.pyplot as plt
import numpy as np

def mdc_forca_bruta(a, b):
  """
  Calcula o MDC usando força bruta.
  Complexidade = O(min(a,b))
  Argumentos:
    a (int): Primeiro número.
    b (int): Segundo número.

  Retorno:
    int: Máximo divisor comum de a e b.
  """
  mdc = 1
  # Itera até o menor entre a and b (inclusive) para checar os potenciais divisores
  for i in range(1, min(a, b) + 1):  # O(min(a, b)), numero maximo é o menor entre a e b
    if a % i == 0 and b % i == 0:   # Checa se i é um divisor comum
      mdc = i
  return mdc

def mdc_euclides(a, b):
  """
  Calcula o MDC usando o algoritmo de Euclides.
  Complexidade = O(log(min(a, b)))
  Argumentos:
    a (int): Primeiro número.
    b (int): Segundo número.
  
  Retorno:
    int: Máximo divisor comum de a e b.
  """
  if b == 0:
    return a
  # Recursivamente calcula o MDC de b e o resto da divisão de a por b
  return mdc_euclides(b, a % b)

def mdc_euclides_iterativo(a, b):
  """
  Calcula o MDC usando o algoritmo de Euclides iterativo.
  Complexidade = O(log(min(a, b)))
  Argumentos:
    a (int): Primeiro número.
    b (int): Segundo número.

  Retorno:
    int: Máximo divisor comum de a e b.
  """
  while b != 0: # Enquanto b for diferente de 0
    a, b = b, a % b  # Vai iterando e calculando o resto da divisão de a em b
  return a

def main():
  """
  Função principal.
  """
  # Tamanhos dos arquivos
  tamanhos = [10, 25, 50, 75, 100, 150, 200, 250, 300, 400, 500, 650, 800, 1000, 1500, 2000, 5000]
  tempo_medio_forca_bruta = []
  tempo_medio_euclides = []
  tempo_medio_euclides_iterativo = []

  # Dicionário para armazenar tempos de execução
  tempos = {
    "forca_bruta": [],
    "euclides": [],
    "euclides_iterativo": [],
  }

  # Loop para cada tamanho de arquivo
  for tamanho in tamanhos:
    # Leitura do arquivo
    with open(f"MDC {tamanho}.txt", "r") as f:
      numeros = []
      for line in f:
        a, b = line.strip().split()
        numeros.append((int(a), int(b)))

    # Cálculo do MDC usando força bruta
    tempos_forca_bruta = []
    for _ in range(5):
      inicio = time.perf_counter()
      for a, b in numeros:
        mdc_forca_bruta(a, b)
      fim = time.perf_counter()
      tempos_forca_bruta.append(fim - inicio)

    # Cálculo do MDC usando algoritmo de Euclides
    tempos_euclides = []
    for _ in range(5):
      inicio = time.perf_counter()
      for a, b in numeros:
        mdc_euclides(a, b)
      fim = time.perf_counter()
      tempos_euclides.append(format(fim - inicio, ".15f"))

    # Cálculo do MDC usando algoritmo de Euclides iterativo
    tempos_euclides_iterativo = []
    for _ in range(5):
      inicio = time.perf_counter()
      for a, b in numeros:
        mdc_euclides_iterativo(a, b)
      fim = time.perf_counter()
      tempos_euclides_iterativo.append(format(fim - inicio, ".15f"))

    # Armazenar tempos de cada execução
    tempos["forca_bruta"].append(tempos_forca_bruta)
    tempos["euclides"].append(tempos_euclides)
    tempos["euclides_iterativo"].append(tempos_euclides_iterativo)
    
    # Calculo tempo médio 
    tempo_medio_forca_bruta.append(sum(tempos_forca_bruta) / 5)
    tempo_medio_euclides.append(sum([float(t) for t in tempos_euclides]) / 5)
    tempo_medio_euclides_iterativo.append(sum([float(t) for t in tempos_euclides_iterativo]) / 5)

    # Converte para milissegundos
    tempo_medio_forca_bruta_ms = [tempo * 1_000 for tempo in tempo_medio_forca_bruta]
    tempo_medio_euclides_ms = [tempo * 1_000 for tempo in tempo_medio_euclides]
    tempo_medio_euclides_iterativo_ms = [tempo * 1_000 for tempo in tempo_medio_euclides_iterativo]

  # Exportar resultados para CSV
  with open("resultados_mdc.csv", "w", newline="") as f:
    escritor = csv.writer(f)
    escritor.writerow(["Tamanho", "Forca Bruta (execucoes) s", "Euclides (execucoes) s", "Euclides Iterativo (execucoes) s", "Tempo médio (força bruta) s", "Tempo médio (Euclides) s", "Tempo médio (Euclides Iterativo) s"])
    for tamanho, tempos_forca_bruta, tempos_euclides, tempos_euclides_iterativo, t_medio_forca_bruta,  t_medio_euclides, t_medio_euclides_iterativo in zip(tamanhos, tempos["forca_bruta"], tempos["euclides"], tempos["euclides_iterativo"], tempo_medio_forca_bruta, tempo_medio_euclides, tempo_medio_euclides_iterativo):
      escritor.writerow([tamanho, tempos_forca_bruta, tempos_euclides, tempos_euclides_iterativo, t_medio_forca_bruta, t_medio_euclides, t_medio_euclides_iterativo])                                                                       
  

  # Criar dataframe com Pandas
  df = pd.DataFrame({
        "Tamanho": tamanhos,
        "Forca Bruta (tempo médio) ms": tempo_medio_forca_bruta_ms,
        "Euclides (tempo médio) ms": tempo_medio_euclides_ms,
        "Euclides Iterativo (tempo médio) ms": tempo_medio_euclides_iterativo_ms,
  })

  # Exportar dataframe para CSV
  df.to_csv("resultados_mdc_pandas.csv", index=False)
  print(df.to_string())
  
  # Selecionar colunas
  df_plot = df[['Tamanho', 'Forca Bruta (tempo médio) ms', 'Euclides (tempo médio) ms', 'Euclides Iterativo (tempo médio) ms']]

  # Gráfico de linhas para comparar Força Bruta com Euclides
  plt.plot(df_plot['Tamanho'], df_plot['Forca Bruta (tempo médio) ms'], label='Força Bruta')
  plt.plot(df_plot['Tamanho'], df_plot['Euclides (tempo médio) ms'], label='Euclides')
  plt.title('Tempo médio para calcular MDC (Força Bruta vs Euclides)')
  plt.xlabel('Tamanho do arquivo')
  plt.ylabel('Tempo médio (milissegundos)')
  plt.legend()
  plt.savefig('line_chart_fb_vs_e.png')
  plt.close()

  # Gráfico de linhas para comparar Euclides com Euclides Iterativo
  plt.plot(df_plot['Tamanho'], df_plot['Euclides (tempo médio) ms'], label='Euclides')
  plt.plot(df_plot['Tamanho'], df_plot['Euclides Iterativo (tempo médio) ms'], label='Euclides Iterativo')
  plt.title('Tempo médio para calcular MDC (Euclides vs Euclides Iterativo)')
  plt.xlabel('Tamanho do arquivo')
  plt.ylabel('Tempo médio (milissegundos)')
  plt.legend()
  plt.savefig('line_chart_e_vs_ei.png')
  plt.close()

  # **Gráfico de dispersão:** Tempo individual vs. Tamanho do arquivo
  coefficients = np.polyfit(tamanhos, tempo_medio_forca_bruta_ms, 1)
  poly_line = np.poly1d(coefficients)
  tamanho_range = np.linspace(min(tamanhos), max(tamanhos), 100)
  tendencia = poly_line(tamanho_range)
  plt.scatter(tamanhos, tempo_medio_forca_bruta_ms)
  plt.plot(tamanho_range, tendencia, color='red', linestyle='--', label=f'Linha de Tendência')
  plt.title('Gráfico de Dispersão: Tamanho do Arquivo vs. Tempo Médio (Força Bruta)')
  plt.xlabel('Tamanho do Arquivo')
  plt.ylabel('Tempo Médio (milissegundos)')
  plt.legend()
  plt.savefig('scatter_plot.png')
  plt.close()

  # **Gráfico de pizza:** Proporção de tempo por algoritmo
  tempos_medios = [sum(tempo_medio_forca_bruta_ms) / len(tempo_medio_forca_bruta_ms),
                 sum(tempo_medio_euclides_ms) / len(tempo_medio_euclides_ms),
                 sum(tempo_medio_euclides_iterativo_ms) / len(tempo_medio_euclides_iterativo_ms)]
  labels = ['Força Bruta', 'Euclides', 'Euclides Iterativo']
  plt.pie(tempos_medios, labels=labels, autopct='%1.1f%%')
  plt.title('Gráfico de Pizza: Proporção dos Tempos Médios de Execução por Algoritmo')
  plt.savefig('pie_chart.png')
  plt.close()
  
  # Gráfico de barras para comparar Força Bruta com Euclides
  df_fb_vs_e = df[['Tamanho', 'Forca Bruta (tempo médio) ms', 'Euclides (tempo médio) ms']]
  plt.figure(figsize=(10, 6))
  df_fb_vs_e.plot(x='Tamanho', kind='bar')
  plt.title('Tempo médio para calcular MDC (Força Bruta vs Euclides)')
  plt.xlabel('Tamanho do Arquivo')
  plt.ylabel('Tempo Médio (milissegundos)')
  plt.savefig('bar_chart_fb_vs_e.png')
  plt.close()

  # Gráfico de barras para comparar Euclides com Euclides Iterativo
  df_e_vs_ei = df[['Tamanho', 'Euclides (tempo médio) ms', 'Euclides Iterativo (tempo médio) ms']]
  plt.figure(figsize=(10, 6))
  df_e_vs_ei.plot(x='Tamanho', kind='bar')
  plt.title('Tempo médio para calcular MDC (Euclides vs Euclides Iterativo)')
  plt.xlabel('Tamanho do Arquivo')
  plt.ylabel('Tempo Médio (milissegundos)')
  plt.savefig('bar_chart_e_vs_ei.png')
  plt.close()

  # Gráfico de área para comparar Força Bruta com Euclides
  plt.fill_between(df['Tamanho'], df['Forca Bruta (tempo médio) ms'], label='Força Bruta', alpha=0.5)
  plt.fill_between(df['Tamanho'], df['Euclides (tempo médio) ms'], label='Euclides', alpha=0.5)
  plt.title('Tempo Médio para Calcular MDC (Força Bruta vs Euclides)')
  plt.xlabel('Tamanho do Arquivo')
  plt.ylabel('Tempo Médio (milissegundos)')
  plt.legend()
  plt.savefig('area_plot_fb_vs_e.png')
  plt.close()

  # Gráfico de área para comparar Euclides com Euclides Iterativo
  plt.fill_between(df['Tamanho'], df['Euclides (tempo médio) ms'], label='Euclides', alpha=0.5)
  plt.fill_between(df['Tamanho'], df['Euclides Iterativo (tempo médio) ms'], label='Euclides Iterativo', alpha=0.5)
  plt.title('Tempo Médio para Calcular MDC (Euclides vs Euclides Iterativo)')
  plt.xlabel('Tamanho do Arquivo')
  plt.ylabel('Tempo Médio (milissegundos)')
  plt.legend()
  plt.savefig('area_plot_e_vs_ei.png')
  plt.close()

if __name__ == "__main__":
  main()
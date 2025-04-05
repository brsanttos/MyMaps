# INTERFACE TKINTER + MAPA COM DADOS POR CONSULTOR, REGIÃO E CLIENTE

import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from geobr import read_municipality
import unicodedata

# Caminhos
arquivo_consultores = r"C:\Users\bruno.santos\OneDrive - MOTORMAC\DEMANDAS\MyMaps\REGIOES POR CONSULTOR.xlsx"

# Carrega dados de consultores
clientes_df = pd.read_excel(arquivo_consultores)
clientes_df.columns = clientes_df.columns.str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
clientes_df.columns = clientes_df.columns.str.strip().str.lower()

# Cria coluna unificada "consultor"
clientes_df['consultor'] = clientes_df[['consultor_externo', 'consultor_interno_pecas', 'consultor_interno_servicos']].bfill(axis=1).iloc[:, 0]
clientes_df.dropna(subset=['consultor'], inplace=True)

# Carrega municípios
municipios = read_municipality(year=2020, simplified=True)
municipios.set_crs(epsg=4674, inplace=True)

# Interface
janela = tk.Tk()
janela.title("Carteira por Consultor, Região ou Tipo de Cliente")
janela.geometry("900x600")

# Filtros
frame_filtros = tk.Frame(janela)
frame_filtros.pack(pady=10)

# Consultor
tk.Label(frame_filtros, text="Consultor:").grid(row=0, column=0, padx=5)
combo_consultor = ttk.Combobox(frame_filtros, state="readonly", width=30)
combo_consultor.grid(row=0, column=1, padx=5)
combo_consultor['values'] = sorted(clientes_df['consultor'].dropna().unique())

# Região
tk.Label(frame_filtros, text="Região:").grid(row=0, column=2, padx=5)
combo_regiao = ttk.Combobox(frame_filtros, state="readonly", width=20)
combo_regiao.grid(row=0, column=3, padx=5)
combo_regiao['values'] = sorted(clientes_df['regiao'].dropna().unique())

# Tipo de cliente
tk.Label(frame_filtros, text="Tipo Cliente:").grid(row=0, column=4, padx=5)
combo_tipo = ttk.Combobox(frame_filtros, state="readonly", width=20)
combo_tipo.grid(row=0, column=5, padx=5)
combo_tipo['values'] = sorted(clientes_df['tipo_cliente'].dropna().unique())

# Resultado
frame_resultado = tk.Frame(janela)
frame_resultado.pack(fill='both', expand=True, padx=10, pady=10)

scroll = tk.Scrollbar(frame_resultado)
scroll.pack(side=tk.RIGHT, fill=tk.Y)

txt_resultado = tk.Text(frame_resultado, wrap='word', yscrollcommand=scroll.set)
txt_resultado.pack(side=tk.LEFT, fill='both', expand=True)
scroll.config(command=txt_resultado.yview)

def aplicar_filtros():
    txt_resultado.delete("1.0", tk.END)

    df = clientes_df.copy()
    if combo_consultor.get():
        df = df[df['consultor'] == combo_consultor.get()]
    if combo_regiao.get():
        df = df[df['regiao'] == combo_regiao.get()]
    if combo_tipo.get():
        df = df[df['tipo_cliente'] == combo_tipo.get()]

    if df.empty:
        txt_resultado.insert(tk.END, "Nenhum resultado encontrado com os filtros selecionados.")
        return

    cidades = sorted(df['cidade'].dropna().unique())
    txt_resultado.insert(tk.END, f"Total de cidades: {len(cidades)}\n")
    txt_resultado.insert(tk.END, f"Total de clientes: {df['nome_cliente'].nunique()}\n\n")

    for cidade in cidades:
        txt_resultado.insert(tk.END, f"- {cidade}\n")

    # Mapa
    municipios_filtros = municipios[municipios['name_muni'].isin(cidades)]
    fig, ax = plt.subplots(figsize=(10, 10))
    municipios.plot(ax=ax, color='lightgrey', edgecolor='white')
    municipios_filtros.plot(ax=ax, color='green', edgecolor='black', label='Cidades da Carteira')
    plt.title("Cidades da Carteira", fontsize=16)
    plt.axis('off')
    plt.tight_layout()
    plt.show()

btn_aplicar = tk.Button(janela, text="Aplicar Filtros e Mostrar", command=aplicar_filtros, font=("Arial", 12))
btn_aplicar.pack(pady=5)

janela.mainloop()
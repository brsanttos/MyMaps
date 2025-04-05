# 🗺️ MyMaps - Visualizador de Carteira por Região, Consultor e Cliente

Projeto em Python com interface Tkinter para visualização geográfica de cidades atendidas por consultores, usando dados de clientes, regiões personalizadas (via KMZ) e integração com mapas do Brasil.

---

## 💡 Funcionalidades

- Filtros por:
  - Consultor (interno/externo)
  - Região
  - Tipo de cliente
- Contagem de cidades e clientes únicos
- Visualização de cidades no mapa via `matplotlib` + `geopandas`
- Importação de regiões do Google My Maps (formato KMZ)
- Leitura de clientes via Excel
- Exportação para CSV (por região)

---

## 🖥️ Tecnologias Utilizadas

- Python 3.10+
- Tkinter
- Pandas
- GeoPandas
- Matplotlib
- Fiona
- geobr

---

## ▶️ Como Executar

1. Clone o projeto:

```bash
git clone https://github.com/brsanttos/MyMaps.git
cd MyMaps

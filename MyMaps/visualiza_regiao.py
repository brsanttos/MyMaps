# VISUALIZA UMA REGIÃO E AS CIDADES DENTRO DELA

import geopandas as gpd
import matplotlib.pyplot as plt
from geobr import read_municipality

# Nome da região a ser visualizada
regiao_nome = "ROBSON"

# Caminhos
regioes_path = r"C:\Users\bruno.santos\OneDrive - MOTORMAC\DEMANDAS\MyMaps\regioes.geojson"

# Carrega as regiões e os municípios (com maior precisão)
regioes_gdf = gpd.read_file(regioes_path)
if regioes_gdf.crs is None:
    regioes_gdf.set_crs(epsg=4326, inplace=True)

municipios = read_municipality(year=2020, simplified=False)
municipios.set_crs(epsg=4674, inplace=True)  # CRS original do geobr
municipios = municipios.to_crs(regioes_gdf.crs)

# Filtra a região desejada
regiao = regioes_gdf[regioes_gdf['Name'] == regiao_nome]

# Faz o join espacial
municipios_na_regiao = gpd.sjoin(municipios, regiao, predicate='intersects')

# Plota
fig, ax = plt.subplots(figsize=(10, 10))
regiao.boundary.plot(ax=ax, color='black', linewidth=2, label='Região')
municipios.plot(ax=ax, color='lightgrey', edgecolor='white', label='Todos Municípios')
municipios_na_regiao.plot(ax=ax, color='green', edgecolor='black', label='Munic. na Região')

plt.title(f"Região: {regiao_nome}", fontsize=16)
plt.legend()
plt.axis('off')
plt.tight_layout()
plt.show()

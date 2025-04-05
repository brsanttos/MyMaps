# PROJETO: Identificar cidades brasileiras por região definida em um KMZ do Google My Maps

import geopandas as gpd
import zipfile
from geobr import read_municipality
import os
import pandas as pd

# ===========================
# ETAPA 1 - Extração do KMZ
# ===========================
kmz_path = r"C:\Users\bruno.santos\OneDrive - MOTORMAC\DEMANDAS\MyMaps\SERVIÇOS - Regioes Consultores Internos.kmz"
extract_path = r"C:\Users\bruno.santos\OneDrive - MOTORMAC\DEMANDAS\MyMaps\kmz_extraido"

# Cria pasta de extração se não existir
os.makedirs(extract_path, exist_ok=True)

with zipfile.ZipFile(kmz_path, 'r') as kmz:
    kmz.extractall(extract_path)

kml_path = os.path.join(extract_path, "doc.kml")

# ===========================
# ETAPA 2 - Conversão para GeoDataFrame
# ===========================
# Lê todas as camadas de estados separadamente
todas_regioes = []
for layer in ['SC', 'RS', 'PR']:
    gdf_layer = gpd.read_file(kml_path, driver='KML', layer=layer)
    todas_regioes.append(gdf_layer)

# Junta todas as regiões em um só GeoDataFrame
regioes_gdf = gpd.GeoDataFrame(pd.concat(todas_regioes, ignore_index=True))
regioes_gdf.set_crs(epsg=4326, inplace=True)

# Salva as regiões como GeoJSON para uso posterior
regioes_gdf.to_file(r"C:\Users\bruno.santos\OneDrive - MOTORMAC\DEMANDAS\MyMaps\regioes.geojson", driver="GeoJSON")

# ===========================
# ETAPA 3 - Cruzamento com cidades do Brasil
# ===========================
# Carrega os limites dos municípios do Brasil
municipios = read_municipality(year=2020, simplified=True)
municipios = municipios.to_crs(epsg=4326)

# Join espacial para saber quais cidades estão em cada região
dados_combinados = gpd.sjoin(municipios, regioes_gdf, predicate='within')

# Agrupa as cidades por região
df_cidades_por_regiao = dados_combinados.groupby('Name')['name_muni'].apply(list).reset_index()

# Salva o resultado em CSV
df_cidades_por_regiao.to_csv(r"C:\Users\bruno.santos\OneDrive - MOTORMAC\DEMANDAS\MyMaps\cidades_por_regiao.csv", index=False, encoding='utf-8')

# Exibe o resultado no terminal
print(df_cidades_por_regiao)

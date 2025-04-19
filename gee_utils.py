import time

import ee
from datetime import datetime, timedelta
from config import SERVICE_ACCOUNT, KEY_FILE


def initialize_earth_engine():
    credentials = ee.ServiceAccountCredentials(SERVICE_ACCOUNT, KEY_FILE)
    ee.Initialize(credentials)


def get_best_sentinel_image(ee_polygon):
    """Seleciona a melhor imagem do Sentinel-2 com baixa cobertura de nuvens e
    garante a consistência dos tipos de dados das bandas."""

    # Data final = hoje
    end_date = datetime.utcnow().date()
    # Data inicial = 30 dias atrás
    start_date = end_date - timedelta(days=30)

    # Converte para string no formato que o GEE espera
    start_date_str = start_date.isoformat()
    end_date_str = end_date.isoformat()

    sat_image = ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED") \
        .filterDate(start_date_str, end_date_str) \
        .filterBounds(ee_polygon) \
        .filterMetadata('CLOUDY_PIXEL_PERCENTAGE', 'less_than', 15) \
        .sort('CLOUDY_PIXEL_PERCENTAGE') \
        .first()

    if sat_image is None:
        raise Exception("Nenhuma imagem encontrada para o local e período especificados.")

    # Garantir que todas as bandas da imagem sejam do tipo UInt16
    sat_image = sat_image.select(['B4', 'B3', 'B2']).toUint16()

    return sat_image


def apply_rgb_visualization(sat_image):
    """Aplica visualização RGB à imagem e garante que todas as bandas tenham o mesmo tipo de dados."""
    bands = ['B4', 'B3', 'B2']  # RGB natural
    rgb_vis = {
        'bands': bands,
        'min': 300,
        'max': 3000,
        'gamma': 2.5
    }

    # Garantir que todas as bandas sejam convertidas para UInt16
    sat_image = sat_image.select(bands).toUint16()

    return sat_image.visualize(**rgb_vis)


def export_image_to_drive(image, ee_polygon, description):
    # Ajusta o gama
    image_rgb = apply_rgb_visualization(image)
    region = ee_polygon.buffer(5000).bounds()

    task = ee.batch.Export.image.toDrive(
        image=image_rgb,
        description=description,
        folder='EarthEngine',
        fileNamePrefix=description,
        region=region,
        scale=10,
        crs='EPSG:4326',
        maxPixels=1e13
    )
    task.start()
    print("Exportação iniciada...")

    while task.active():
        print("Aguardando a finalização da exportação...")
        time.sleep(10)

    status = task.status()
    print("Status final:", status)
    return description

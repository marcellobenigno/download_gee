import ee
import folium


def create_folium_map(image, lat, lng):
    mapa = folium.Map(location=[lat, lng], zoom_start=10)
    map_id_dict = ee.Image(image).getMapId()

    folium.raster_layers.TileLayer(
        tiles=map_id_dict['tile_fetcher'].url_format,
        attr='Map Data &copy; Google Earth Engine',
        name='Sentinel-2 RGB',
        overlay=True,
        control=True
    ).add_to(mapa)

    folium.LayerControl().add_to(mapa)
    return mapa

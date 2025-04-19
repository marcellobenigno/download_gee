import ee
from shapely import wkt

from gdrive_utils import download_file, authenticate_drive, find_file_id_by_name
from gee_utils import initialize_earth_engine, get_best_sentinel_image, export_image_to_drive


def main():
    initialize_earth_engine()

    # WKT da bounding box
    wkt_string = """
    Polygon ((
        -53.30186805999999677 -20.59221528000000134,
        -53.05849750000000142 -20.59221528000000134,
        -53.05849750000000142 -20.45399778000000168,
        -53.30186805999999677 -20.45399778000000168,
        -53.30186805999999677 -20.59221528000000134
        ))
    """
    cod_imovel = '9110620268081'
    polygon = wkt.loads(wkt_string)
    coords = list(polygon.exterior.coords)
    ee_polygon = ee.Geometry.Polygon([coords])

    image = get_best_sentinel_image(ee_polygon)

    file_prefix = export_image_to_drive(image, ee_polygon, description=cod_imovel)

    service = authenticate_drive()
    file_id = find_file_id_by_name(service, folder_name='EarthEngine', file_prefix=file_prefix)

    if file_id:
        destination_path = f'images/{cod_imovel}.jpg'
        download_file(file_id, destination_path, service)
    else:
        print("⚠️ Falha ao localizar o arquivo no Drive.")


if __name__ == '__main__':
    main()

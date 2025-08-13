import urllib.request
from shapely.geometry import Point
import geopandas as gpd
import os
import rasterio
from rasterio.transform import rowcol
from datetime import datetime, timedelta
import pystac_client # 0.9.0
import planetary_computer


def calculate_window_dates(sos_date, eos_date):
    """
    Calculate window dates based on SOS and EOS dates.
    """

    sos = datetime.strptime(sos_date, '%Y-%m-%d')
    eos = datetime.strptime(eos_date, '%Y-%m-%d')

    win_a_start = (sos - timedelta(days=15)).strftime('%Y-%m-%d')
    win_a_end = (sos + timedelta(days=15)).strftime('%Y-%m-%d')
    win_b_start = (eos - timedelta(days=30)).strftime('%Y-%m-%d')
    win_b_end = eos.strftime('%Y-%m-%d')

    return win_a_start, win_a_end, win_b_start, win_b_end

def get_date_from_day_of_year(day_of_year: int, year: int) -> str:
    if day_of_year < 1 or day_of_year > 366:
        raise ValueError("day_of_year must be between 1 and 366")
    base_date = datetime(year, 1, 1)
    result_date = base_date + timedelta(days=day_of_year - 1)
    if day_of_year == 366 and result_date.year != year:
        raise ValueError(f"{year} is not a leap year.")
    return result_date.strftime("%Y-%m-%d")

def get_dates_from_tifs(point: Point, start_season_tif_path: str, end_season_tif_path: str, year=2020, season_type='winter'):
    """
    Extract start and end crop calendar dates (day-of-year and date) from GeoTIFFs using rasterio.

    Args:
        point: shapely.geometry.Point
        start_season_tif_path: path to the start season GeoTIFF
        end_season_tif_path: path to the end season GeoTIFF
        year: crop calendar reference year

    Returns:
        (start_day, end_day, start_date_str, end_date_str)
    """
    with rasterio.open(start_season_tif_path) as start_src:
        row, col = rowcol(start_src.transform, point.x, point.y)
        start_day = start_src.read(1)[row, col]

    with rasterio.open(end_season_tif_path) as end_src:
        row, col = rowcol(end_src.transform, point.x, point.y)
        end_day = end_src.read(1)[row, col]

    # Handle crop calendars that span across years, like a season starting in September and ending in March
    end_year = year + 1 if end_day < start_day else year

    start_date = get_date_from_day_of_year(int(start_day), year)
    end_date = get_date_from_day_of_year(int(end_day), end_year)

    return start_date, end_date

def download_crop_calendars(crop_calendar_dir="./"):
    os.makedirs(crop_calendar_dir, exist_ok=True)
    base_url = "https://github.com/fieldsoftheworld/ftw-qgis-plugin/raw/main/resources/global_crop_calendars/"

    for season, files in crop_calendar_files.items():
        for file_type, filename in files.items():
            local_path = os.path.join(crop_calendar_dir, filename)
            if not os.path.exists(local_path):
                try:
                    urllib.request.urlretrieve(base_url + filename, local_path)
                except Exception as e:
                    print(f"Failed to download {filename}: {str(e)}")
                    return False
    return True


def get_best_image_ids(win_a_start, win_a_end, win_b_start, win_b_end, s2_tile_id, max_cloud_cover=20):
    catalog = pystac_client.Client.open(
        "https://planetarycomputer.microsoft.com/api/stac/v1",
        modifier=planetary_computer.sign_inplace,
    )

    def find_best_image(start_date, end_date, cloud_threshold, s2_tile_id):
        time_range = f"{start_date}/{end_date}"
        print(f"Searching for images between {start_date} and {end_date} with cloud cover < {cloud_threshold}%")

        
        search = catalog.search(
            collections=["sentinel-2-l2a"],
            datetime=time_range,
            query={
              "eo:cloud_cover": {"lt": cloud_threshold},
              "s2:mgrs_tile": {"eq": s2_tile_id},
              "s2:nodata_pixel_percentage": {"lt": 10}
            },
        )

        items = search.item_collection()
        if len(items) == 0:
            print(f"No images found with cloud cover < {cloud_threshold}%")
            return None

        best_item = min(items, key=lambda item: item.properties.get("eo:cloud_cover", 100))
        cloud_cover = best_item.properties.get("eo:cloud_cover", 100)
        print(f"Found image from {best_item.datetime.date()} with {cloud_cover}% cloud coverage")
        return best_item.id

    cloud_thresholds = [max_cloud_cover, 50, 70, 100]
    win_a_id = None
    win_b_id = None

    for threshold in cloud_thresholds:
        if win_a_id is None:
            win_a_id = find_best_image(win_a_start, win_a_end, threshold, s2_tile_id)
        if win_b_id is None:
            win_b_id = find_best_image(win_b_start, win_b_end, threshold, s2_tile_id)
        if win_a_id is not None and win_b_id is not None:
            break

    if win_a_id is None:
        raise ValueError(f"Could not find suitable images for window A ({win_a_start} to {win_a_end}) even with 100% cloud cover")
    if win_b_id is None:
        raise ValueError(f"Could not find suitable images for window B ({win_b_start} to {win_b_end}) even with 100% cloud cover")

    return win_a_id, win_b_id


s2grid_url = 'https://sentiwiki.copernicus.eu/__attachments/1692737/S2A_OPER_GIP_TILPAR_MPC__20151209T095117_V20150622T000000_21000101T000000_B00.zip?inst-v=affad40c-471a-4024-9c0f-5b675004aa50'

s2grid = gpd.read_file(s2grid_url, layer='Features')

"""Download crop calendar files into ./data if they don't exist."""
crop_calendar_files = {
    "summer": {
        "start": "sc_sos_3x3_v2.tiff",
        "end": "sc_eos_3x3_v2.tiff"
    },
    "winter": {
        "start": "wc_sos_3x3_v2.tiff",
        "end": "wc_eos_3x3_v2.tiff"
    }
}

download_crop_calendars()
from metric_comp import MetricDataset, VectorDataset, get_zonal_stats_df
import geopandas as gpd
from pathlib import Path


# Using geopandas to open the shapefile
""" interior_refuges_shp_path = '/Users/ojlarson/Desktop/yf/Interior_Refuges.shp'
interior_refuges = gpd.read_file(interior_refuges_shp_path)
shape_id_column = 'NWRName' """

# Set path templates
split_metrics_dir = '/Users/ojlarson/Documents/modis-viirs/split_metrics'
viirs_metrics_dir = '/Users/ojlarson/Documents/modis-viirs/viirs_metrics/v1'
modis_metric_path = str(split_metrics_dir / Path('band_{band}') / Path(
    '{year}_snowyear_metrics_v006.tif_band{band}.tif'))
viirs_metric_path = str(
    viirs_metrics_dir / Path('{year}') / 'metrics' / Path('{metric_name}_merged_{year}.tif'))

# Metric lookup lists
viirs_metric_names = ['first_snow_day', 'last_snow_day', 'fss_range', 'longest_css_start', 'longest_css_end',
                      'longest_css_range', 'snow_days', 'no_snow_days', 'css_segment_num', None, None, 'tot_css_days']
modis_metric_names = ['first_snow_day', 'last_snow_day', 'fss_range', 'longest_css_first_day', 'longest_css_last_day',
                      'longest_css_day_range', 'snow_days', 'no_snow_days', 'css_segment_num', 'mflag', 'cloud_days', 'tot_css_days']

band = 7
year = 2015

ds1 = MetricDataset(modis_metric_path, band, year,
                    'modis', 'new-6', viirs_metric_names)
ds2 = MetricDataset(viirs_metric_path, band, year,
                    'viirs', 'v1', viirs_metric_names)
shp_ds = VectorDataset(
    '/Users/ojlarson/Desktop/yf/Interior_Refuges.shp', 'NWRName')

print(get_zonal_stats_df(ds1, ds2, shp_ds))

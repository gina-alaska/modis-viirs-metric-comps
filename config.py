import os

# Set path templates
base_path = '/Users/ojlarson/Documents/modis-viirs'
split_metrics_dir = 'split_metrics'
viirs_metrics_dir = 'viirs_metrics/v1'

modis_template = os.path.join(
    'band_{band}', '{year}_snowyear_metrics_v006.tif_band{band}.tif')
viirs_template = os.path.join(
    '{year}', 'metrics', '{metric_name}_merged_{year}.tif')


class Config:
    def __init__(self):
        self.modis_metric_path = os.path.join(
            base_path, split_metrics_dir, modis_template)
        self.viirs_metric_path = os.path.join(
            base_path, viirs_metrics_dir, viirs_template)
        self.viirs_metric_names = ['first_snow_day', 'last_snow_day', 'fss_range', 'longest_css_start', 'longest_css_end',
                                   'longest_css_range', 'snow_days', 'no_snow_days', 'css_segment_num', None, None, 'tot_css_days']
        self.modis_metric_names = ['first_snow_day', 'last_snow_day', 'fss_range', 'longest_css_first_day', 'longest_css_last_day',
                                   'longest_css_day_range', 'snow_days', 'no_snow_days', 'css_segment_num', 'mflag', 'cloud_days', 'tot_css_days']

import os

# Set path templates
base_path = "/Users/ojlarson/Documents/GINA_Projects/NPS/snow_assessment"
modis_metrics_dir = "modis-snow-arctic-data-center"
viirs_metrics_dir = "viirs_snow_metrics"

modis_version = "v6"
viirs_version = "v001"

modis_template = "{year}_MODIS_snow_metrics_{version}.tif"

viirs_template = "{year}_VIIRS_snow_metrics_{version}.tif"

default_output_path = "/Users/ojlarson/Documents/GINA_Projects/NPS/snow_assessment"

viirs_metric_names = [
    "first_snow_day",
    "last_snow_day",
    "fss_range",
    "longest_css_start",
    "longest_css_end",
    "longest_css_range",
    "snow_days",
    "no_snow_days",
    "css_segment_num",
    None,
    None,
    "tot_css_days",
]
modis_metric_names = [
    "first_snow_day",
    "last_snow_day",
    "fss_range",
    "longest_css_first_day",
    "longest_css_last_day",
    "longest_css_day_range",
    "snow_days",
    "no_snow_days",
    "css_segment_num",
    "mflag",
    "cloud_days",
    "tot_css_days",
]


class Config:
    base_dir = base_path
    modis_metric_path = os.path.join(base_path, modis_metrics_dir, modis_template)
    viirs_metric_path = os.path.join(base_path, viirs_metrics_dir, viirs_template)
    viirs_metric_names = viirs_metric_names
    modis_metric_names = modis_metric_names
    default_output_path = default_output_path
    modis_version = modis_version
    viirs_version = viirs_version

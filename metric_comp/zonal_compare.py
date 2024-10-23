from rasterstats import zonal_stats
import pandas as pd
from metric_comp.additional_stats import additional_statistics_functions


def get_zonal_stats_df(ds1, ds2, shp_ds, additional_statistics_functions=additional_statistics_functions):
    """
    Uses rasterstats.zonal_stats to compute statistics for a given polygon dataset from two modis/viirs MetricDatasets.

    args:
    ds1 (MetricDatastet): Raster dataset 1.
    ds2 (MetricDatastet): Raster dataset 2.
    shp_ds (VectorDataset): Polygon dataset for zonal_stats.
    additional_statistics_functions: Additional functions for the add_stats rasterstats.zonal_stats param.
    """
    ds1_array, ds1_transform = ds1.load_tiff()
    ds2_array, ds2_transform = ds2.load_tiff()
    if ds1_array is None or ds2_array is None:
        print(f"At least one of the two datasets did not open.")
        return None
    shp = shp_ds.load_shp()
    ds1_stats = zonal_stats(shp, ds1_array, affine=ds1_transform,
                            add_stats=additional_statistics_functions, nodata=0)
    ds2_stats = zonal_stats(shp, ds2_array, affine=ds2_transform,
                            add_stats=additional_statistics_functions, nodata=0)
    ds1_stats_df = pd.DataFrame(ds1_stats)
    ds1_stats_df['shapefile'] = shp_ds.file_name
    ds1_stats_df['zone'] = shp[shp_ds.id_field]
    ds2_stats_df = pd.DataFrame(ds2_stats)
    ds2_stats_df['shapefile'] = shp_ds.file_name
    ds2_stats_df['zone'] = shp[shp_ds.id_field]
    ds1_stats_df['sensor'] = ds1.sensor
    ds1_stats_df['version'] = ds1.version
    ds2_stats_df['sensor'] = ds2.sensor
    ds2_stats_df['version'] = ds2.version
    combined_stats = pd.concat([ds1_stats_df, ds2_stats_df])
    return combined_stats

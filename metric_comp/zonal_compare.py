from rasterstats import zonal_stats
import pandas as pd
from metric_comp.additional_stats import additional_statistics_functions


def get_zonal_stats_df(ds1, ds2, shp_ds, additional_statistics_functions=additional_statistics_functions):
    ds1_array, ds1_transform = ds1.load_tiff()
    ds2_array, ds2_transform = ds2.load_tiff()
    if ds1_array is None or ds2_array is None:
        print(f"At least one of the two datasets did not open.")
        return None
    shp = shp_ds.load_shp()
    ds1_stats = zonal_stats(shp, ds1_array, affine=ds1_transform,
                            add_stats=additional_statistics_functions)
    ds2_stats = zonal_stats(shp, ds2_array, affine=ds2_transform,
                            add_stats=additional_statistics_functions)
    ds1_stats_df = pd.DataFrame(ds1_stats)
    ds1_stats_df['shapefile'] = shp_ds.file_name
    ds1_stats_df['zone'] = shp[shp_ds.id_field]
    ds2_stats_df = pd.DataFrame(ds2_stats)
    ds2_stats_df['shapefile'] = shp_ds.file_name
    ds2_stats_df['zone'] = shp[shp_ds.id_field]
    print('assigning sensor and version manually')
    ds1_stats_df['sensor'] = 'modis'
    ds1_stats_df['version'] = 'new-v6'
    ds2_stats_df['sensor'] = 'viirs'
    ds2_stats_df['version'] = globals().get('viirs_metric_version', 'v1')
    combined_stats = pd.concat([ds1_stats_df, ds2_stats_df])
    return combined_stats

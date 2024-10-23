from metric_comp import MetricDataset
from metric_comp import clip_raster
from config import Config

import pandas as pd
import numpy as np
from pathlib import Path


def create_summary_stats(array: np.ndarray, nozeros: bool):
    """
    Generate a pandas dataframe with summary statistics from a 1- or 2-dimensional array.

     Args:
       array (np.ndarray): The input 1- or 2-dimensional array.
       nozeros (bool): If True, converts values of 0 to np.nan

    Returns:
       pd.dataframe: A dataframe containg a set of summary statistics
    """
    if nozeros:
        array = np.where(array == 0, np.nan, array)
    if len(array.shape) == 2:
        data = pd.Series(array.flatten())
    elif len(array.shape) > 2:
        print('Array is greater than 2-dimensional.')
        return None

    summary_stats = {
        'Statistic': ['Count', 'Min', '25th Percentile', 'Median', '75th Percentile', 'Max', 'Mean', 'Std Dev', 'Range', 'Mode'],
        'Value': [
            data.count(),
            data.min(),
            data.quantile(0.25),
            data.median(),
            data.quantile(0.75),
            data.max(),
            data.mean(),
            data.std(),
            data.max() - data.min(),
            data.mode()[0]
        ]
    }

    df = pd.DataFrame(summary_stats, columns=['Statistic', 'Value'])
    df['Statistic'] = pd.Categorical(
        df['Statistic'], categories=summary_stats['Statistic'], ordered=True)
    return (df)


def compare_summary_stats(band: int, year: int, clip: bool = False, nozeros: bool = False, output: Path = None):
    """
    Process summary statistics for the given band and year between two modis/viirs metric datasets. Uses MetricDataset class.

    Args:
    band (int): The band number of the desired modis/viirs metric.
    year (int): The year/snow year of the mods/viirs dataset.
    clip (bool): If true, the 2nd dataset will be clipped to the extent of the 1st dataset.
    nozeros (bool): If true, summary statistics will change 0 values to np.nan values to remove them from statistics.
    output (Path): A file path for a .csv file to save the dataframe output.

    Returns:
    combined_df (pd.dataframe): The merged dataframes, joined by statistic, for the two modis/viirs datasets.
    """

    config = Config()

    ds1 = MetricDataset(config.splt_modis_metric_path, band,
                        year, 'modis', 'new-6', config.modis_metric_names)

    ds2 = MetricDataset(config.viirs_metric_path, band,
                        year, 'viirs', 'v1', config.viirs_metric_names)

    print('Opening', ds1.file_path)
    ds1_array = ds1.load_tiff()[0]
    print('Opening', ds2.file_path)
    if clip:
        ds2_array = clip_raster(ds1, ds2)[0]
    else:
        ds2_array = ds2.load_tiff()[0]

    print('Creating summary statistics for', ds1.sensor)
    ds1_stats = create_summary_stats(ds1_array, nozeros)
    print(ds1_stats.columns)
    ds1_stats = ds1_stats.rename(columns={'Value': str(ds1.sensor)})
    print(ds1_stats.columns)
    print('Creating summary statistics for', ds2.sensor)
    ds2_stats = create_summary_stats(ds2_array, nozeros)
    ds2_stats = ds2_stats.rename(columns={'Value': str(ds2.sensor)})
    print('Merging summary statistics')
    combined_df = pd.merge(ds1_stats, ds2_stats, on='Statistic', how='outer')
    if output:
        combined_df.to_csv(output)
    return combined_df


if __name__ == '__main__':
    pd.set_option('display.float_format', '{:.2f}'.format)
    df = compare_summary_stats(7, 2015, clip=True, nozeros=True)

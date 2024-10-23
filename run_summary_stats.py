import click
from metric_comp import compare_summary_stats
from config import Config

import pandas as pd
import numpy as np
from pathlib import Path


@click.command()
@click.option('-b', '--band', required=True, type=int, help='Raster band to process.')
@click.option('-y', '--year', required=True, type=int, help='Year of the data to process.')
@click.option('-o', '--output', required=False, type=Path, help='.csv output path.')
@click.option('--clip', is_flag=True, help='Clip 2nd dataset to bounds of 1st dataset')
@click.option('--nozeros', is_flag=True, help='Remove zero values from arrays prior to summarizing')
def main(band, year, clip, nozeros, output):

    result = compare_summary_stats(band, year, clip, nozeros, output)
    click.echo(result)
    return (result)


if __name__ == '__main__':
    pd.set_option('display.float_format', '{:.2f}'.format)
    main()

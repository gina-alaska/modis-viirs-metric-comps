import click
from metric_comps import MetricDataset, VectorDataset
from metric_comps import get_zonal_stats_df
from config import Config


@click.command()
@click.option("-b", "--band", required=True, type=int, help="Raster band to process.")
@click.option(
    "-y", "--year", required=True, type=int, help="Year of the data to process."
)
@click.option(
    "-s",
    "--shapefile",
    required=True,
    type=click.Path(exists=True),
    help="Path to the shapefile.",
)
@click.option(
    "-f",
    "--id_field",
    required=True,
    type=str,
    help="Attribute field in shapefile for zonal comparison",
)
def process_zonal_stats(band, year, shapefile, id_field):
    """
    Process zonal statistics for the given band, year, shapefile, and raster file.
    """

    config = Config()

    ds1 = MetricDataset(
        config.modis_metric_path,
        band,
        year,
        "modis",
        config.modis_version,
        config.modis_metric_names,
    )

    ds2 = MetricDataset(
        config.viirs_metric_path,
        band,
        year,
        "viirs",
        config.viirs_version,
        config.viirs_metric_names,
    )

    shp_ds = VectorDataset(shapefile, id_field)

    result = get_zonal_stats_df(ds1, ds2, shp_ds)

    click.echo(f"Zonal stats for band {band}, year {year}: {result}")


if __name__ == "__main__":
    process_zonal_stats()

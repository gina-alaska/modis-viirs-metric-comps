from pathlib import Path
import rasterio as rio
import geopandas as gpd
import os


class MetricDataset:
    def __init__(self, file_template, band, year, sensor, version, metric_names):
        self.file_template = file_template
        self.band = band
        self.year = year
        self.sensor = sensor
        self.version = version
        self.metric_name = metric_names[band - 1]
        self.dataset = None

        self.file_path = Path(file_template.format(
            band=self.band, year=self.year, metric_name=self.metric_name))

    def load_tiff(self):
        try:
            with rio.open(self.file_path) as src:
                src_transform = src.transform
                src_array = src.read(1)
        except:
            print(
                f"Cannot find {
                    self.file_path}, probably no metric tiff file..."
            )
            return None
        return src_array, src_transform

    def open(self):
        """Open the raster file."""
        if self.dataset is None or self.dataset.closed:
            self.dataset = rio.open(self.file_path)
        return self.dataset

    def close(self):
        """Close the raster file."""
        if self.dataset is not None or self.dataset.open:
            self.dataset.close()
        return self.dataset


class VectorDataset:
    def __init__(self, file_path, id_field):
        self.file_path = file_path
        self.id_field = id_field
        self.file_name = os.path.splitext(os.path.basename(file_path))[0]

    def load_shp(self):
        try:
            gdf = gpd.read_file(self.file_path)
        except:
            print('Error loading shapefile')
            return False
        if self.id_field not in gdf.columns:
            print('ID field not in columns')
        return gdf

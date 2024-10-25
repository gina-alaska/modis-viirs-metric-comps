# modis-viirs-metric-comps

This repository is used for camparisons between MODIS and VIIRS for NDVI and Snow metrics.

This code builds upon methods initially developed by Hunter Barndt.

## Usage

To examine and compare datasets, methods have been developed in the [metric_comp](/metric_comp) module.

They can be imported into scripts and notebooks as such:
```python
from metric_comp import function_name
```

This allows these methods to be used elsewhere, for two main categories: Jupyter Notebooks in the [notebooks](/notebooks) folder, and command-line python scripts in the [root directory](/).

For setting up the repository, [config.py](/config.py) can be revised to local paths, and [requirements.txt](/requirements.txt) can be used to set up an environement. One recommendation for doing so would be to use a venv:

```
$ cd path/to/modis-viirs-metric-comps
$ python -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

## Notebooks

In the [notebooks](/notebooks) folder is a [template.ipynb](template.ipynb) file. This contains a couple of code blocks importing typically used libraries, methods from metric_comp, and sets up a few variables. Other noebooks build off of this to explore and graph various statistics.

## Command line scripts

Several python scripts have been written to streamline processing of statistics for specific years and band numbers. Building off of these would also allow comparisons to be automated. The main two as of 10/25/2024 are:

- [zonal_comp.py](zonal_comp.py)
```
  Usage: zonal_comp.py [OPTIONS]

  Process zonal statistics for the given band, year, shapefile, and raster
  file.

Options:
  -b, --band INTEGER    Raster band to process.  [required]
  -y, --year INTEGER    Year of the data to process.  [required]
  -s, --shapefile PATH  Path to the shapefile.  [required]
  -f, --id_field TEXT   Attribute field in shapefile for zonal comparison
                        [required]
  --help                Show this message and exit.
  ```

-[run_summary_stats](run_summary_stats.py)
```
Usage: run_summary_stats.py [OPTIONS]

Options:
  -b, --band INTEGER  Raster band to process.  [required]
  -y, --year INTEGER  Year of the data to process.  [required]
  -o, --output PATH   .csv output path.
  --clip              Clip 2nd dataset to bounds of 1st dataset without
                      resampling.
  --resample          Resample 2nd dataset to align with 1st dataset.
  --nozeros           Remove zero values from arrays prior to summarizing.
  --help              Show this message and exit.
```

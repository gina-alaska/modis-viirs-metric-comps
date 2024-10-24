import rasterio as rio
from metric_comp import MetricDataset
from rasterio.mask import mask
from rasterio.warp import calculate_default_transform, reproject, Resampling
from rasterio.io import MemoryFile


def clip_raster(bounding_dataset: MetricDataset, dataset: MetricDataset):
    ds1 = bounding_dataset.open()
    ds2 = dataset.open()
    bounds = ds1.bounds
    ds1.close()
    bbox_geom = {
        "type": "Polygon",
        "coordinates": [[
            [bounds.left, bounds.bottom],
            [bounds.left, bounds.top],
            [bounds.right, bounds.top],
            [bounds.right, bounds.bottom],
            [bounds.left, bounds.bottom]
        ]]
    }

    clipped_image, clipped_transform = mask(ds2, [bbox_geom], crop=True)
    ds2.close()

    return clipped_image[0], clipped_transform


def resample_raster(reference_dataset: MetricDataset, dataset: MetricDataset):
    ds1 = dataset.open()
    ds2 = reference_dataset.open()
    # Get the transform, width, and height from the ds2erence raster
    # Get the transform, width, and height from the ds2erence raster
    transform, width, height = calculate_default_transform(
        ds1.crs, ds2.crs, ds2.width, ds2.height, *ds2.bounds)

    # Create an array to hold the resampled data
    resampled_image = ds1.read(1, out_shape=(height, width))

    # Perform the resampling
    reproject(
        source=ds1.read(1),
        destination=resampled_image,
        src_transform=ds1.transform,
        src_crs=ds1.crs,
        dst_transform=transform,
        dst_crs=ds2.crs,
        resampling=Resampling.nearest  # Adjust resampling method if needed
    )
    ds1.close()
    ds2.close()
    # Return the resampled image and its new transform
    return resampled_image, transform

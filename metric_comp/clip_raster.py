import rasterio as rio
from metric_comp import MetricDataset
from rasterio.mask import mask


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

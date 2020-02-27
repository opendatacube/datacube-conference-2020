
from datacube.utils.geometry import GeoBox, Geometry, CRS
from collections.abc import Mapping
from datacube.virtual.impl import reproject_array, reproject_band, compute_reproject_roi
import numpy as np


def reproject(ds, output_crs, output_res=None, resampling=None, dask_chunks=None):
    if isinstance(ds, xr.DataArray):
        return reproject_slice(ds, output_crs, output_res, resampling, dask_chunks)
    
    output_crs = CRS(output_crs)
    
    if output_res is None:
        if output_crs.units[0] not in CRS(ds.crs).units:
            raise ValueError
        else:
            output_res = ds.geobox.resolution

    output_geobox = GeoBox.from_geopolygon(ds.geobox.geographic_extent, resolution=output_res, crs=output_crs)
    
    output_bands = {}
    for band_name, band in ds.items():
        if hasattr(band.data, 'dask') and dask_chunks is None:
            dask_chunks = dict(zip(band.dims, band.data.chunksize))

        if isinstance(resampling, Mapping):
            band_resampling = resampling[band_name] if band_name in resampling else 'nearest'
        else:
            band_resampling = resampling
        output_bands[band_name] = reproject_band(band, output_geobox, resampling=band_resampling, dims=band.dims, dask_chunks=dask_chunks)
    
    return xr.Dataset(output_bands, attrs={'crs': output_crs})


def reproject_da(da, output_crs, output_res=None, resampling=None, dask_chunks=None):
    output_crs = CRS(output_crs)
    
    if output_res is None:
        if output_crs.units[0] not in CRS(da.geobox.crs).units:
            raise ValueError
        else:
            output_res = da.geobox.resolution

    output_geobox = GeoBox.from_geopolygon(da.geobox.geographic_extent, resolution=output_res, crs=output_crs)
    
    if hasattr(da.data, 'dask') and dask_chunks is None:
        dask_chunks = dict(zip(da.dims, da.data.chunksize))
        
    if 'nodata' not in da.attrs:
        da.attrs['nodata'] = np.nan

    output_band = reproject_band(da, output_geobox, resampling=resampling, dims=da.dims, dask_chunks=dask_chunks)
    output_band.attrs['crs'] = output_crs
    return output_band
    
def reproject_slice(da, output_crs, output_res, resampling, dask_chunks):
    bad_dims = [dim for dim, dim_size in da.sizes.items() if dim not in ('x', 'y') and dim_size > 1]
    if bad_dims:
        dim_name = bad_dims[0]
        return xr.concat([reproject_slice(
            da.isel(**{dim_name:i}), output_crs, output_res, resampling, dask_chunks
                   ) for i in range(da[dim_name].size)], dim=dim_name).transpose(*da.dims)
    else:
        return reproject_da(da, output_crs, output_res, resampling, dask_chunks)
    
    
# Function to colorize a single band

from matplotlib import cm
from matplotlib.colors import Normalize
import xarray as xr

def colorize(da, cmap='viridis', vmin=None, vmax=None):
    """
    Convert values in single band xarray to colormap values
    Can accept multiple time steps
    da - xarray.DataArray
    cmap - desired colormapping
    vmin / vmax - values for normalisation
    """
    normalized = Normalize(vmin=vmin, vmax=vmax)(da)
    colormapped = cm.get_cmap(cmap)(normalized, bytes=True)
    colormapped_xr = xr.DataArray(data=colormapped, 
                                  coords = da.coords, 
                                  dims=da.dims+('band',),
                                  attrs=da.attrs
                                 )
    # Mask out the no data
    colormapped_xr[...,3] = np.isfinite(da) * 255
    return colormapped_xr

import datacube
import odc.ui
from ipywidgets import IntSlider, widgets as w

def create_rgb_image_layer(data, layername, crs='epsg:3857', clamp=(3000)):
    """
    Convert values in single band xarray to colormap values
    Can accept multiple time steps
    da - xarray.DataArray
    cmap - desired colormapping
    vmin / vmax - values for normalisation
    """
    reprojected_data = reproject(data, crs, resampling='nearest')
    # Mask out invalid data
    reprojected_data = datacube.storage.masking.mask_invalid_data(reprojected_data)
    # Create the image, requires a clamp due to high values
    image = odc.ui.mk_image_overlay(reprojected_data, clamp=clamp, layer_name=layername)
    return image



def create_single_band_image_layer(data, layername, crs='epsg:3857', cmap='Greens', vmin=0, vmax=1):
    """
    Convert values in single band xarray to colormap values
    Can accept multiple time steps
    da - xarray.DataArray
    cmap - desired colormapping
    vmin / vmax - values for normalisation
    """
    reprojected_data = reproject(data, crs, resampling='nearest')
    # Mask out invalid data
    #reprojected_data = datacube.storage.masking.mask_invalid_data(reprojected_data)
    # Colorize
    cm_da = colorize(reprojected_data, vmin=vmin, vmax=vmax, cmap=cmap) 
    # Create the image, requires a clamp due to high values
    image = odc.ui.mk_image_overlay(cm_da, layer_name=layername)
    return image
    
from datacube.utils.geometry import BoundingBox

def add_layer_to_map(image, m, slider):
    # Work out the required map zoom based on the bounding box
    (top, right), (bottom, left) = image.bounds
    bounding_box = BoundingBox(left, bottom, right, top)
    zoom = odc.ui.zoom_from_bbox(bounding_box)
    # Update the map zoom
    m.zoom = zoom
    # Center map on new image
    m.center = (bounding_box[1], bounding_box[0])
    # Add the opacity slider to the new image
    w.jslink((slider, 'value'),         
             (image, 'opacity') )
    m.add_layer(image)

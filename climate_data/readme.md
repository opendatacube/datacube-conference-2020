# Climate (weather) data

There exist gridded datasets of global historical weather (model reanalysis), which could be useful for training, validation or masking of other datacube products. 

For example:
- SAR backscatter can easily detect water, except in windy conditions (as the roughness of a choppy lake can resemble a dry field).
- Rainfall time-series could be relevant to water inundation, SAR soil moisture, and bushfire regrowth.
- Temperature or wind direction may be relevant to bushfire severity and hotspot reanalysis.


The idea is to build on progress exploring ERA5 at the recent SAR hack day, and produce one or more python notebooks to document an example workflow for incorporating climate data variables with datacube xarrays. One complication is that while NetCDF ERA5 data is already available on the NCI, a sandbox solution may need to retrieve multidimensional data through web APIs.

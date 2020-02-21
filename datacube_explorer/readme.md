# Datacube Explorer STAC and More 

The Datacube Explorer is a great app that is currently used to discover what data is indexed into a datacube. This proposal is to deliver a few enhancements to this app to make it even more useful. Improvements suggested include the following:

- A STAC compatible REST API. This would create a dymanic STAC endpoint, in a form that is compatible with the sat-api application. Implementing this will provide the ODC with a way of integrating with the Pangeo systems, via their [stac-intake Intake driver](https://github.com/pangeo-data/intake-stac).
- Better web map. The web map could use a few major and minor upgrades, including the use of MapBoxGL and fixing small bugs like ensuring the map doesn’t flow off the bottom of the screen.
- Linked into the second item, ensuring that web assets are built and minified would be nice. Consider using WebPack and integrating that into the build system.
- A nice feature for users would be providing a datacube load command based on the area of interest that’s currently in view.

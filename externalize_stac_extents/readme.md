# [Externalize Spatio-Temporal Extents of Datasets](https://docs.google.com/presentation/d/16QGFw_6ARNFz0INKl1vs9LGZ-jhaq7CG7-YDZsMk_zQ/)

## Motivation
Currently web applications (OWS, Explorer) built on Datacube-Core Python API create their own spatiotemporal extent columns in self-managed schemas to avoid diving into the Datacube JSON blob metadata and extracting space/time information every time.

This project aims to make a backwards compatible / optional enhancement to the datacube / agdc schema with postgis-geometry and time range with time zone columns to capture spatiotemporal extents of Datasets.

## The roadmaps for the implementation is as follows:
- Issue is being worked on as part of [OWS codebase](https://github.com/opendatacube/datacube-ows/issues/197).
- ~Implement / reuse query to extract space-time extents per dataset with the following columns : dataset id, space_extent, time_extent.~
- Store results in a materialised view and refactor OWS to use this view in the agdc schema instead of tables in its own schema
- Implement triggers to refresh the view on new indexing events
- Evaluate ease of use / performance and consider elevating view to a table in agdc schema and possibly access via datacube python API in datacube-core 2.0
- Consider regression/backwards compatibility by adding a switch in client code to check for presence of space/time extent view/table in agdc schema.

## Caveats and considerations:
- Variability of JSON metadata will require coalesce
- Whether to maintain spatial extent in native projection not EPSG:4326. Indexing such as GIST will only be beneficial if the column is in uniform projection.
- Handling multi-datasets such as S2A/S2B.
- Indexing to be applied to space time columns.

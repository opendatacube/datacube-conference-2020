# Water Interoperability

## Motivation
Based on the feedback from numerous Africa Regional Data Cube (ARDC) hand-on Open Data Cube (ODC) trainings, we have concluded that this type of notebook will be greatly appreciated by the Digital Earth Africa users.

## Objective

Develop a notebook that uses more than one dataset to yield a single water product. This will use Landsat (WOFS), Sentinel-1 (Thresholding method) and S2 (WOFS) to detect water over time and produce a WOFS-like result. 

- Demo over a region (e.g., Ghana) where we have S1, S2 and Landsat data.
- Use the COVE tool to know when the various satellites cover the same area. 
- Consider differences in spatial resolution of missions, as Landsat (30m), Sentinel-2 (10m,20m) and Sentinel-1 (20m) are different. Do we reproject into the same grid or use some other clever approach?
- Develop WOFS-like products (# water / # clear) for individual missions and also mission combinations. 
- Heavily use statistical correlation, and not just rely on visual inspection in validating the results.

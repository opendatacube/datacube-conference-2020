# Generic Prepare Scripts

## Motivation
Easier creation of prepare scripts for new datasets.
Prepare scripts can be made more generic as most of the code is common across prepare scripts. Hardcoded values in current prepare scripts should be tied back into a product definition.

## Objectives:
- Review and improvements to current design/implementation.
- Standardise the common code across all prepare scripts.
- Product definition parsing/loading.
- Metadata extraction
- Agdc-metadata.yaml generation
- Matching a source dataset to a product definition
- Hard 0/1 scoring
- Soft 0-1 scoring
- Highest score wins
- Integrate into ODC.

## Out there:
- Auto generate product/ingest definitions, at least a baseline / starting point.
- Links to dc.save

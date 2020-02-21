# Updating Datasets
Once you have [created a dataset](create_dataset.md), it may be necessary to
update the data it contains. Whenever this happens, you should be sure to bump
the version number in the ``version.py`` file, commit to your vcs, and republish
to pypi. 

Datasets use [semantic versioning](https://semver.org/), which includes 3 numbers
separated by dots indicating MAJOR.MINOR.PATCH. Although all the guidelines don't
translate perfectly from code to data, we offer the following suggestions:

## Patch Version
Increment the patch version when the dataset has changed slightly in ways that
are not likely to affect analysis. For example, if the datacenter fills a
small gap in waveforms long before an event. This will, of course, still be
detected by the waveform files having different hashes, but wont likely huge
impacts on analysis. 

## Minor Version
Increment the minor version when small(ish) changes are made which may effect
analysis. For example, if a slightly different velocity model was used to
re-calculate event locations, or a small mistake in station coordinates was
corrected. 

## Major Version
Increment the major version when significant amounts of new data are
added/removed or major issues are fixed. For example, if many more events
were included in the dataset.

## Recreate Hashes
Most changes (big or small) will require you to recalculate file hashes. This is done
like so:

```python
import obsplus
# load dataset
ds = obsplus.load_dataset('sulphur_peak')
# reclaculate all hashes in data_path and save to source_path
ds.create_sha256_hash(path=ds.source_path)
```

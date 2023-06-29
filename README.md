All scripts require v0.62 or newer of the syGlass Python module.

## channel_to_mask.py

A script that leverages the syGlass Python module to convert a channel in a given project into a mask stored in the mask octree (`.syk` file).


### Usage

```
python channel_to_mask.py [path/to/project.syg] [channelNumber]
```

## channel_as_mask.py

A script that leverages the syGlass Python module to export one channel masked by another channel (where that channel is within the saved thresholds) in a given project.


### Usage

```
python channel_as_mask.py [path/to/project.syg] [imageChannelNumber] [maskChannelNumber]
```

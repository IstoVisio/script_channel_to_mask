import syglass as sy
import numpy as np
import tifffile
import glob
import os
import sys

from syglass import pyglass as py
from tqdm import tqdm


def main(project_path: str, channel_number: int):
    
    if not sy.is_project(project_path):
        raise ValueError("No valid syGlass project at the given path.")
    project = sy.get_project(project_path)

    resolution_map = project.get_resolution_map()
    max_resolution_level = len(resolution_map) - 1
    project_size = project.get_size(max_resolution_level)

    thresholds = project.get_thresholds()
    lower_threshold = thresholds[channel_number - 1][0]
    upper_threshold = thresholds[channel_number - 1][1]

    print("Checking for old temporary files to clean up...")
    for old_file in glob.glob("temp_*.tiff"):
        os.remove(old_file) 

    print("Writing image slices as TIFF files...")
    for z in tqdm(range(project_size[0])):
        slice = project.get_custom_block(0, max_resolution_level, np.zeros(3), np.array([1, project_size[1], project_size[2]]))
        slice = slice.data[:, :, :, channel_number - 1]
        slice[slice < lower_threshold] = 0
        slice[slice > upper_threshold] = 0
        tifffile.imwrite(f"temp_{z:07}.tiff", slice)

    print("Cleaning up temporary files...")
    for temp_file in glob.glob("temp_*.tiff"):
        os.remove(temp_file)


if __name__ == "__main__":
    
    if len(sys.argv) != 3:
        print("Usage: python channel_to_mask.py [path/to/project.syg] [channel_number]")
    else:
        main(sys.argv[1], int(sys.argv[2]))
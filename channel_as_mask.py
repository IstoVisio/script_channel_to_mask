import syglass as sy
import numpy as np
import tifffile
import glob
import os
import sys

from tqdm import tqdm


def main(project_path: str, image_channel_number: int, mask_channel_number):
    
    if not sy.is_project(project_path):
        raise ValueError("No valid syGlass project at the given path.")
    project = sy.get_project(project_path)

    resolution_map = project.get_resolution_map()
    max_resolution_level = len(resolution_map) - 1
    project_size = project.get_size(max_resolution_level)

    thresholds = project.get_thresholds()
    lower_threshold = thresholds[mask_channel_number - 1][0]
    upper_threshold = thresholds[mask_channel_number - 1][1]

    print("Checking for old mask files to clean up...")
    for old_file in glob.glob("masked_*.tiff"):
        os.remove(old_file) 

    print("Writing image slices as TIFF files...")
    for z in tqdm(range(project_size[0])):
        slice = project.get_custom_block(0, max_resolution_level, np.array([z, 0, 0]), np.array([1, project_size[1], project_size[2]]))
        image_slice = slice.data[:, :, :, image_channel_number - 1]
        mask_slice = slice.data[:, :, :, mask_channel_number - 1]
        image_slice[mask_slice < lower_threshold] = 0
        image_slice[mask_slice > upper_threshold] = 0
        tifffile.imwrite(f"masked_{z:07}.tiff", image_slice)

    print("Finished!")


if __name__ == "__main__":
    
    if len(sys.argv) != 4:
        print("Usage: python channel_as_mask.py [path/to/project.syg] [image_channel_number] [mask_channel_number]")
    else:
        main(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
import syglass as sy
import numpy as np
import tifffile
import glob
import os
import sys

from tqdm import tqdm


def main(project_path: str, tiff_directory: str, image_channel_number: int, mask_channel_number: int):
    
    if not sy.is_project(project_path):
        raise ValueError("No valid syGlass project at the given path.")
    project = sy.get_project(project_path)
    tiff_list = glob.glob(tiff_directory + "/*.tif*")

    thresholds = project.get_thresholds()
    lower_threshold = thresholds[mask_channel_number - 1][0]
    upper_threshold = thresholds[mask_channel_number - 1][1]

    print("Checking for old mask files to clean up...")
    for old_file in glob.glob("masked_*.tiff"):
        os.remove(old_file) 

    print("Writing image slices as TIFF files...")
    z = 0
    for tiff_slice in tqdm(tiff_list):
        slice = tifffile.imread(tiff_slice)
        image_slice = slice[:, :, image_channel_number - 1]
        mask_slice = slice[:, :, mask_channel_number - 1]
        image_slice[mask_slice < lower_threshold] = 0
        image_slice[mask_slice > upper_threshold] = 0
        tifffile.imwrite(f"masked_{z:07}.tiff", image_slice)
        z = z + 1

    print("Finished!")


if __name__ == "__main__":
    
    if len(sys.argv) != 5:
        print("Usage: python tiff_channel_as_mask.py [path/to/project.syg] [path/to/tiff/directory] [image_channel_number] [mask_channel_number]")
    else:
        main(sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]))
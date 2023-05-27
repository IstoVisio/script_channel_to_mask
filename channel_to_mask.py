import syglass as sy
import numpy as np
import tifffile
import time
import glob
import os
import sys

from syglass import pyglass as py
from tqdm import tqdm


# separate function needed for scope; releasing TIFF files accessed here
def create_mask_project(project_path: str):
    mask_project = py.CreateProject(py.path(project_path).parent_path(), py.path(project_path).stem().string() + ".syk", isMaskMode=True)
    directory_description = py.DirectoryDescription()
    directory_description.InspectByReferenceFile("./temp_0000000.tiff")
    data_provider = py.OpenTIFFs(directory_description.GetFileList(), timeSeries=False)
    included_channels = py.IntList(range(data_provider.GetChannelsCount()))
    data_provider.SetIncludedChannels(included_channels)

    conversion_driver = py.ConversionDriver()
    conversion_driver.SetInput(data_provider)
    conversion_driver.SetOutput(mask_project)

    conversion_driver.StartAsynchronous()

    while conversion_driver.GetPercentage() != 100:
        print(f"Creating mask layer, {conversion_driver.GetPercentage():.2f}% complete...")
        time.sleep(3)


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
        slice = project.get_custom_block(0, max_resolution_level, np.array([z, 0, 0]), np.array([1, project_size[1], project_size[2]]))
        slice = slice.data[:, :, :, channel_number - 1]
        slice[slice < lower_threshold] = 0
        slice[slice > upper_threshold] = 0
        slice[slice > 1] = 1
        tifffile.imwrite(f"temp_{z:07}.tiff", slice)

    create_mask_project(project_path)

    print("Cleaning up temporary files...")
    for temp_file in glob.glob("temp_*.tiff"):
        os.remove(temp_file)

    print("Finished!")


if __name__ == "__main__":
    
    if len(sys.argv) != 3:
        print("Usage: python channel_to_mask.py [path/to/project.syg] [channel_number]")
    else:
        main(sys.argv[1], int(sys.argv[2]))
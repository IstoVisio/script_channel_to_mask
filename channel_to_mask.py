import syglass as sy
import sys

from syglass import pyglass as py


def main(project_path: str, channel_number: int):
    
    if not sy.is_project(project_path):
        raise ValueError("No valid syGlass project at the given path.")
    project = sy.get_project(project_path)

    resolution_map = project.get_resolution_map()
    max_resolution_level = len(resolution_map) - 1
    block_count = resolution_map[max_resolution_level]

    # does not consider timeseries data for now
    for i in range(block_count):
        
        block = project.get_block(0, max_resolution_level, i)
        print(block.data.shape)
        channel_block = block.data[:, :, :, channel_number - 1]
        
				# TODO: consider threshold, add mask


if __name__ == "__main__":
    
    if len(sys.argv) != 3:
        print("Usage: python channel_to_mask.py [path/to/project.syg] [channel_number]")
    else:
        main(sys.argv[1], int(sys.argv[2]))
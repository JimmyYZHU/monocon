### Merge the folder containing detection results of individual frames into a single file

import os


def merge_detections(raw_detections_dir: str, save_path: str):
    # Create an empty list to store the contents of each file
    file_contents = []

    # Loop through each file in the folder
    filenames = os.listdir(raw_detections_dir)
    filenames.sort()
    for filename in filenames:
        if filename.endswith(".txt"):
            # Extract the frame index from the file name
            # Assiming the xxxxxx.txt format for each detection file here. If you use a different format, change this line accordingly.
            frame_index = int(filename[:6])

            # Open the file and read its contents
            with open(os.path.join(raw_detections_dir, filename), "r") as f:
                contents = f.read().strip().split(
                    "\n")  # f.read() ends with a newline character, so we remove it with strip()

            if len(contents[0]) == 0:
                continue
            # Add the frame index as the first column of the contents
            modified_contents = [f"{frame_index} {line}" for line in contents]

            # Append the modified contents to the list
            file_contents.extend(modified_contents)

    # Concatenate the contents of the list into a single string
    merged_contents = "\n".join(file_contents)

    # Write the concatenated string to a new file
    if not os.path.exists(os.path.dirname(save_path)):
        os.makedirs(os.path.dirname(save_path))
    with open(save_path, "w") as f:
        f.write(merged_contents)
    print("Wrote merged detections to:", save_path)


if __name__ == "__main__":
    import argparse

    # Arguments
    parser = argparse.ArgumentParser(
        'Merge the folder containing detection results of individual frames into a single file')
    parser.add_argument('--folder_path',
                        type=str,
                        help="Path to the folder containing the detection files for each frame. ")
    parser.add_argument('--save_path', type=str, help="Path to save the merged file")
    args = parser.parse_args()
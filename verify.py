""" Simple audit script for carousel slides, CI friendly. """

from __future__ import print_function
import glob
import json
import os
import pprint
import sys
import traceback

def verify():
    """
    Loads master list of all slides, verifies that the JSON is sane and
    the images are not missing.
    """

    # Python 2/3 compatibility for FileNotFoundError.
    try:
        FileNotFoundError
    except:
        FileNotFoundError = IOError

    try:
        file = json.load(open("json/slides.json", "r"))
    except FileNotFoundError:
        print("Error: Main slide file not found.")
        sys.exit(1)
    except json.decoder.JSONDecodeError:
        print("Error: Main slide file has a JSON error, fix file.")
        print(traceback.format_exc())
        sys.exit(1)
    except Exception:
        print("Error: Unknown error")
        sys.exit(1)

    missing_images = []
    missing_metadata = []
    invalid_mask = []
    slide_files = glob.glob("images/*.*")
    for slide in file:
        # Check if we're missing files
        if "image" in slide and not os.path.isfile("images/" + slide["image"]):
            missing_images.append(slide["image"])
        if "video" in slide and not os.path.isfile("images/" + slide["video"]):
            missing_images.append(slide["video"])

        # Check if we've got messed up metadata
        if not "image" in slide and not "video" in slide:
            missing_metadata.append(slide)
        elif any([not x in slide for x in ["title", "caption", "weight"]]):
            missing_metadata.append(slide)
        elif "mask" in slide and slide["mask"] not in ["light", "medium", "strong"]:
            invalid_mask.append(slide["title"])

        # Remove files from list of files -- if any are left, they are unused
        try:
            if "image" in slide:
                slide_files.remove("images/%s" % slide["image"])
            elif "video" in slide:
                slide_files.remove("images/%s" % slide["video"])
        except ValueError:
            pass


    if slide_files:
        print("Warning: Some images are unused.")
        pprint.pprint(slide_files)

    if missing_images:
        print("Error: Some missing images")
        pprint.pprint(missing_images)
        sys.exit(1)

    if missing_metadata:
        print("Error: Some missing metadata")
        pprint.pprint(missing_metadata)
        sys.exit(1)

    if invalid_mask:
        print("Error: invalid visual masks")
        pprint.pprint(invalid_mask)
        sys.exit(1)

if __name__ == "__main__":
    verify()

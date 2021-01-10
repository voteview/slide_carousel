""" Simple audit script for carousel slides, CI friendly. """

from __future__ import print_function
import json
import os
import sys
import traceback

def verify():
    """
    Loads master list of all slides, verifies that the JSON is sane and
    the images are not missing.
    """

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
    for slide in file:
        if "image" in slide and not os.path.isfile("images/" + slide["image"]):
            missing_images.append(slide["image"])
        if "video" in slide and not os.path.isfile("images/" + slide["video"]):
            missing_images.append(slide["video"])

    if missing_images:
        print("Error: Some missing images")
        print(missing_images)
        sys.exit(1)

if __name__ == "__main__":
    verify()

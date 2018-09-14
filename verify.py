from __future__ import print_function
import json
import os
import sys
import traceback

def verify():
	try:
		file = json.load(open("json/slides.json", "r"))
	except:
		print(traceback.format_exc())
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

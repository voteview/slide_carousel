# slide_carousel

[![Build Status](https://travis-ci.org/voteview/slide_carousel.svg?branch=master)](https://travis-ci.org/voteview/slide_carousel)


This repository holds the slides used on the voteview.com front page carousel and instructions for adding slides to the carousel.

## Images

Images can be any web-friendly format. Size should be very wide (1000+ px) and 300px tall. The carousel will by default zoom the image to fit the screen width. JPGs submitted should be saved at quality 10 and optimized before adding to the repo. Please ensure the image name does not conflict with other files. Images should be public domain or fair use.

## JSON

`json/sources.json` contains the slides themselves. Slides are sampled via weighted sampling without replacement from the file. Each individual slide has the following format:

```
{
	"image": "history.jpg", 
	"title": "Geography: District History", 
	"caption": "Learn the story of a place through the people that represented it through history", 
	"link": "/district",
	"mask": "light",
	"weight": 10
},
```

* *image*: Filename of the image for the slide.
* *video*: If given, an MP4 video rather than an image for the slide. Producing videos is described on [our repository Wiki](https://github.com/voteview/slide_carousel/wiki/Transforming-Videos-into-Video-Slides)
* *title*: Title for slide
* *caption*: Caption for slide. Text automatically wraps, but HTML is supported.
* *weight*: How likely the slide is to be sampled (higher weights are higher)
* *link*: Relative link on the site for the slide. (OPTIONAL)
* *mask*: If provided, applies a semi-transparent black mask layer on top of the image. This is used to get ensure contrast with the caption text when the background image is very light. Valid choices are "light", "medium", or "strong". (OPTIONAL)

## Checking

`verify.py` runs a simple verification loop that verifies that the slides JSON file is valid and that all images/videos referenced in the slides are present in the right place. This script is run by Continuous Integration testing on commit.

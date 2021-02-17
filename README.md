# slide_carousel

[![Build Status](https://travis-ci.org/voteview/slide_carousel.svg?branch=master)](https://travis-ci.org/voteview/slide_carousel)


This repository holds the slides used on the voteview.com front page carousel and instructions for adding slides to the carousel.

## Images and Videos

Images can be any web-friendly format. Size should be very wide (1000+ px) and 300px tall. The carousel will by default zoom the image to fit the screen width. JPGs submitted should be saved at quality 10 (PhotoShop) and optimized before adding to the repo. Please ensure the image name does not conflict with other files. Images should be public domain or fair use.

Videos should be H.264 (.mp4 container). Producing videos is described on [our repository Wiki](https://github.com/voteview/slide_carousel/wiki/Transforming-Videos-into-Video-Slides).

If images are not wide enough, the background on the slide will be ![#333333](https://via.placeholder.com/33/333333/000000?text=+) `#333333`

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
* *video*: If given, an MP4 video rather than an image for the slide. Producing videos is described on [our repository Wiki](https://github.com/voteview/slide_carousel/wiki/Transforming-Videos-into-Video-Slides).
* *title*: Title for slide.
* *caption*: Caption for slide. Text automatically wraps, but HTML is not supported.
* *weight*: How likely the slide is to be sampled. Higher weights are higher: currently, most slides are 1, 2, or 4 and major site features or news events are 10-20 -- note that adding more slides dilutes the weights of the existing weights so at some point it may be necessary to renormalize.
* *link*: Relative link on the site for the slide beginning with a slash e.g. `/rollcall/RH0010001`. (OPTIONAL)
* *mask*: If provided, applies a semi-transparent black mask layer on top of the image. This is used to get ensure contrast with the caption text when the background image is very light. Valid choices are "light" (20% opacity black), "medium" (30% opacity black), or "strong" (50% opacity black). In general slides which are light or black and white should have stronger masks, and more colourful or darker backgrounds do not need a mask. (OPTIONAL)

## Checking integrity

`verify.py` runs a simple verification loop that verifies that the slides JSON file is valid and that all images/videos referenced in the slides are present in the right place. This script is run by Continuous Integration testing on commit.

## Previewing images.

When developing slides, I found it was difficult to tell whether I had written too much text or the wrong level of mask. As a result, I made a simple preview tool allowing you to view any current slide.

First, run `gallery/build.py` to compile the current slides. This works by injecting `json/slides.json` into `gallery/resources/tester-stub.js` to make `gallery/resources/tester-compiled.js`.

Now, open `gallery/gallery.html` in a web browser. It is possible to adjust the mask for any slide on the fly, as well as changing title or caption to examine layout and flow.

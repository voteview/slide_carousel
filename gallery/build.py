""" Compiles the gallery testing code. """
import json

def compile():
    """ Compile the slide JSON into the gallery code. """
    template = open("resources/tester-stub.js", "r").read()
    slides = json.load(open("../json/slides.json", "r"))
    slides.sort(key=lambda s: s.get("title", "").lower())
    js = json.dumps(slides, indent="\t")
    with open("resources/tester-compiled.js", "w") as f:
        f.write(template.replace("INSERT_SLIDES_HERE", js))


if __name__ == "__main__":
    compile()

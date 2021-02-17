""" Compiles the gallery testing code. """

def compile():
    """ Compile the slide JSON into the gallery code. """
    template = open("resources/tester-stub.js", "r").read()
    js = open("../json/slides.json", "r").read()
    with open("resources/tester-compiled.js", "w") as f:
        f.write(template.replace("INSERT_SLIDES_HERE", js))


if __name__ == "__main__":
    compile()

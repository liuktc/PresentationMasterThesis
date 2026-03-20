# Add .. to the path to import from the parent directory
import sys
import textwrap
sys.path.append("..")

from templates import MySlide


from manim import *


class ConclusionsScene(MySlide):
    def construct(self):
        conclusions = [
            "The modality gap is more complex than just a simple global shift",
            "The modality gap is not just a geometric artifact, but it is part of how the model represents semantic information",
            "The modality gap is not a dense phenomenon, but it is concentrated in a small number of features"
        ]
        conclusions = BulletedList(*conclusions, font_size=24)
        conclusions.scale_to_fit_width(12)
        conclusions.move_to(ORIGIN)

        self.play(Write(conclusions))
        # self.wait(2)
        self.p.next_slide()
        self.p.play(Unwrite(conclusions), run_time=0.7)
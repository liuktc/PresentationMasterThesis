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
            "The modality gap is not a distributed phenomenon, but it is concentrated in a small number of features"
        ]
        future_works = [
            "Investigate the training dynamisc of the concept specific modality gap",
            "Explore the propagation of the gap in multimodal LLMs such as LLaVA"
        ]

        conclusions_title = Tex("Conclusions", font_size=36)
        conclusions_title.to_edge(UP, buff=1.2)
        conclusions = BulletedList(*conclusions, font_size=24, buff=0.2)
        conclusions.scale_to_fit_width(12)
        # conclusions.move_to(ORIGIN)
        conclusions.next_to(conclusions_title, DOWN, buff=0.5)

        future_works_title = Tex("Future Work", font_size=36)
        future_works_title.next_to(conclusions, DOWN, buff=1)
        # future_works_title.to_edge(UP, buff=1.2).to_edge(RIGHT, buff=0.5)
        future_works = BulletedList(*future_works, font_size=24, buff=0.2)
        future_works.scale_to_fit_width(12)
        # future_works.next_to(conclusions, DOWN, buff=1)
        future_works.next_to(future_works_title, DOWN, buff=0.5)

        self.p.play(Write(conclusions_title), Write(conclusions), Write(future_works_title), Write(future_works), run_time=1.5)
        # self.wait(2)
        self.p.next_slide()
        self.p.play(Unwrite(conclusions), Unwrite(future_works), Unwrite(conclusions_title), Unwrite(future_works_title), run_time=0.7)
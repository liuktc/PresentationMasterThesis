# Add .. to the path to import from the parent directory
import sys
sys.path.append("..")

from templates import MySlide


from manim import *


class SVG(MySlide):
    def construct(self):
        svg = SVGMobject("figures_dark/ablation.svg")
        svg.scale_to_fit_width(config.frame_width * 0.8)
        self.p.play(Write(svg), run_time=4.0)
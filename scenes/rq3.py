# Add .. to the path to import from the parent directory
import sys
import textwrap
sys.path.append("..")

from templates import MySlide


from manim import *
from .research_questions import get_research_questions

class RQ3Scene(MySlide):
    def construct(self):
        rq3 = get_research_questions(
            "RQ3",
            r"Can concept-specific gap corrections improve downstream task performance compared to a single global correction?",
            color=RED,
        )
        rq3.move_to(ORIGIN)
        self.p.play(Write(rq3))
        self.p.next_slide()

        new_height = (config["frame_height"]/2 - self.DEFAULT_TOP) * 0.8
        self.p.play(rq3.animate.scale_to_fit_height(new_height).to_edge(UP + LEFT, buff=0.1))

        main_text = r"We first evaluate the performance of concept-specific gap corrections on retrieval tasks."

        text = Tex(main_text, font_size=28)
        text.scale_to_fit_width(config["frame_width"] - 2)
        text.to_edge(UP, buff=1)
        self.p.play(Write(text))

        plot = SVGMobject("figures_dark/retrieval_bar_comparison_2.svg").scale_to_fit_height(5)

        plot.next_to(text, DOWN, buff=0.5)
        self.p.play(Write(plot), run_time=1.5)
        self.p.next_slide()
        self.p.play(Unwrite(text), Unwrite(plot), run_time=0.7)

                                                                        
        main_text = r"We also evaluate the performance of concept-specific gap corrections on classification tasks, highlighting the importance of tuning the coefficient $\alpha$."

        text = Tex(main_text, font_size=28)
        text.scale_to_fit_width(config["frame_width"] - 2)
        text.to_edge(UP, buff=1)
        self.p.play(Write(text))
        plot_1 = SVGMobject("figures_dark/zeroshot_alpha_sweep_3.svg").scale_to_fit_height(5)
        plot_2 = SVGMobject("figures_dark/retrieval_alpha_sweep_3.svg").scale_to_fit_height(5)
        # plot_1.next_to(text, DOWN, buff=0.5)
        plots = VGroup(plot_1, plot_2)
        plots.arrange(RIGHT, buff=0.5)
        plots.move_to(ORIGIN)
        plots.next_to(text, DOWN, buff=0.5)
        self.p.play(Write(plots), run_time=1.5)

        self.p.next_slide()
        self.p.play(Unwrite(text), Unwrite(plots), Unwrite(rq3), run_time=0.7)
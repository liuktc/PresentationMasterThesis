# Add .. to the path to import from the parent directory
import sys
import textwrap
sys.path.append("..")

from templates import MySlide


from manim import *
from .research_questions import get_research_questions

class RQ2Scene(MySlide):
    def construct(self):
        rq2 = get_research_questions(
            "RQ2",
            r"Can SAEs decomposition help us understand the geometry of the modality gap?",
            color=GREEN,
        )
        rq2.move_to(ORIGIN)
        self.p.play(Write(rq2))
        self.p.next_slide()

        new_height = (config["frame_height"]/2 - self.DEFAULT_TOP) * 0.8
        self.p.play(rq2.animate.scale_to_fit_height(new_height).to_edge(UP + LEFT, buff=0.1))

        main_text = r"The modality gap also reflects in the geometry of the sparse hidden layer of the SAE since the majority of its features are active for a single modality only ($\text{MSI} > 0.8$)"

        text = Tex(main_text, font_size=28)
        text.scale_to_fit_width(config["frame_width"] - 2)

        text.to_edge(UP, buff=1)
        self.p.play(Write(text))
        plot = SVGMobject("figures_dark/msi_distribution.svg").scale_to_fit_width(6)
        plot.next_to(text, DOWN, buff=0.5)
        self.p.play(Write(plot), run_time=1.5)

        self.p.next_slide()

        self.p.play(Unwrite(text), Unwrite(plot), run_time=0.7)

        main_text = r"The gap is concetrated in a small subset of features. Just $15$ features captures around $90\%$ of the gap energy"

        text = Tex(main_text, font_size=28)
        text.scale_to_fit_width(config["frame_width"] - 2)
        text.to_edge(UP, buff=1)
        self.p.play(Write(text))
        plot = SVGMobject("figures_dark/gap_sparsity.svg").scale_to_fit_width(6)
        plot.next_to(text, DOWN, buff=0.5)
        self.p.play(Write(plot), run_time=1.5)

        self.p.next_slide()

        self.p.play(Unwrite(text), Unwrite(plot), run_time=0.7)

        main_text = r"We also found a strong correlation between the $\text{MSI}^{(c)}$ of a concept and the norm of its modality gap $\| \vec{\Delta}^{(c)} \|$."

        text = Tex(main_text, font_size=28)
        text.scale_to_fit_width(config["frame_width"] - 2)
        text.to_edge(UP, buff=1)
        self.p.play(Write(text))
        plot = SVGMobject("figures_dark/msi_vs_gap_norm.svg").scale_to_fit_height(4)
        plot.next_to(text, DOWN, buff=0.5)
        self.p.play(Write(plot), run_time=1.5)

        self.p.next_slide()
        self.p.play(Unwrite(text), Unwrite(plot), run_time=0.7)

        main_text = r"Finally, we show that removing features with the highest MSI leads to a big reduction of the modality gap $\| \vec{\Delta} \|$ but also a significant drop in performance on downstream tasks."

        text = Tex(main_text, font_size=28)
        text.scale_to_fit_width(config["frame_width"] - 2)
        text.to_edge(UP, buff=1)
        self.p.play(Write(text))
        plot = SVGMobject("figures_dark/ablation.svg").scale_to_fit_height(4)
        plot.next_to(text, DOWN, buff=0.5)
        self.p.play(Write(plot), run_time=1.5)

        self.p.next_slide()

        self.p.play(Unwrite(text), Unwrite(plot), Unwrite(rq2), run_time=0.7)

# Add .. to the path to import from the parent directory
import sys
sys.path.append("..")

from templates import MySlide
from settings import IMAGE_COLOR, TEXT_COLOR


from manim import *

class AppendixScene(MySlide):
    def construct(self):
        main_text = r"We also evaluate the performance of concept-specific gap corrections on classification tasks, highlighting the importance of tuning the coefficient $\alpha$."

        text = Tex(main_text, font_size=28)
        text.scale_to_fit_width(config["frame_width"] - 2)
        text.to_edge(UP, buff=1)
        self.p.play(Write(text))
        plot_1 = SVGMobject("figures_dark/zeroshot_alpha_sweep_4.svg").scale_to_fit_height(5)
        plot_2 = SVGMobject("figures_dark/retrieval_alpha_sweep_4.svg").scale_to_fit_height(5)
        # plot_1.next_to(text, DOWN, buff=0.5)
        plots = VGroup(plot_1, plot_2)
        plots.arrange(RIGHT, buff=0.5)
        plots.move_to(ORIGIN)
        plots.next_to(text, DOWN, buff=0.5)
        self.p.play(Write(plots), run_time=1.5)

        self.p.next_slide()
        self.p.play(Unwrite(text), Unwrite(plots), run_time=0.7)


class AppendixGapEnergyAndSparsityScene(MySlide):
    def construct(self):
        # Left side: Gap Energy formula
        gap_energy_title = Tex("Gap Energy", font_size=36)
        gap_energy_title.to_edge(UP, buff=1.2).to_edge(LEFT, buff=0.5)

        gap_energy_formula = MathTex(
            r"E_k^{(c)} = \left( \frac{1}{N^{(c)}} \sum_{i=1}^{N^{(c)}} \left( z_k(\mathbf{v}_i^{(c)}) -  z_k(\mathbf{t}_i^{(c)}) \right) \right)^2",
            font_size=32,
            substrings_to_isolate=[r"\mathbf{v}_i^{(c)}", r"\mathbf{t}_i^{(c)}"],
        )
        gap_energy_formula.set_color_by_tex(r"\mathbf{v}_i^{(c)}", IMAGE_COLOR)
        gap_energy_formula.set_color_by_tex(r"\mathbf{t}_i^{(c)}", TEXT_COLOR)
        gap_energy_formula.next_to(gap_energy_title, DOWN, buff=0.5)
        gap_energy_formula.to_edge(LEFT, buff=0.5)

        # Right side: Gap Sparsity text and plot
        sparsity_text = r"Just $15$ features captures around $90\%$ of the gap energy"
        text = Tex(sparsity_text, font_size=26)
        text.scale_to_fit_width(config["frame_width"] / 2 - 1)
        text.to_edge(UP, buff=1.2).to_edge(RIGHT, buff=0.5)

        plot = SVGMobject("figures_dark/gap_sparsity_2.svg").scale_to_fit_height(4.5)
        plot.next_to(text, DOWN, buff=0.4)

        # Play all animations
        self.p.play(Write(gap_energy_title), Write(gap_energy_formula), Write(text), Write(plot), run_time=1.5)
        self.p.next_slide()
        self.p.play(Unwrite(gap_energy_title), Unwrite(gap_energy_formula), Unwrite(text), Unwrite(plot), run_time=0.7)


class MSIConceptScene(MySlide):
    def construct(self):
        main_text = r"We also found a strong correlation between the $\text{MSI}^{(c)}$ of a concept and the norm of its modality gap $\| \vec{\Delta}^{(c)} \|$."
        text = Tex(main_text, font_size=28)
        text.scale_to_fit_width(config["frame_width"] - 2)
        text.to_edge(UP, buff=0.8)

        msi_concept_formula = MathTex(
            r"\mathrm{MSI}^{(c)} = \frac{\sum_{k=1}^{D} \bar{a}_{k}^{(c)} \, \mathrm{MSI}_{k}}{\sum_{k=1}^{D} \bar{a}_{k}^{(c)}}",
            font_size=36,
            substrings_to_isolate=[r"\bar{a}_{k}^{(c)}", r"\mathrm{MSI}_{k}"]
        )
        # msi_concept_formula.set_color_by_tex(r"\bar{a}_{k}^{(c)}", IMAGE_COLOR)
        # msi_concept_formula.set_color_by_tex(r"\mathrm{MSI}_{k}", TEXT_COLOR)

        plot = SVGMobject("figures_dark/msi_vs_gap_norm_4.svg").scale_to_fit_height(4)

        # Group formula and plot side by side
        content = VGroup(msi_concept_formula, plot)
        content.arrange(RIGHT, buff=0.5)
        content.next_to(text, DOWN, buff=0.7)

        self.p.play(Write(text), run_time=1)
        self.p.play(Write(msi_concept_formula), Write(plot), run_time=1.5)
        self.p.next_slide()
        self.p.play(Unwrite(text), Unwrite(msi_concept_formula), Unwrite(plot), run_time=0.7)



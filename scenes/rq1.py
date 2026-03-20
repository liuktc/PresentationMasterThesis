# Add .. to the path to import from the parent directory
import sys
import textwrap
sys.path.append("..")

from templates import MySlide


from manim import *
from .research_questions import get_research_questions


class RQ1Scene(MySlide):
    def construct(self):
        rq1 = get_research_questions(
            "RQ1",
            r"Is the modality gap uniform across different semantic concepts?",
            color=BLUE,
        )
        rq1.move_to(ORIGIN)
        self.p.play(Write(rq1))
        self.p.next_slide()

        new_height = (config["frame_height"]/2 - self.DEFAULT_TOP) * 0.8
        self.p.play(rq1.animate.scale_to_fit_height(new_height).to_edge(UP + LEFT, buff=0.1))

        main_text = r"To answer this question, we compute the norm of the modality gap $\| \vec{\Delta}^{(c)} \|$ for each concept $c$ in our dataset, and show its distribution."

        text = Tex(main_text, font_size=28)
        text.scale_to_fit_width(config["frame_width"] - 2)
        text.to_edge(UP, buff=1)
        self.p.play(Write(text))

        plot = SVGMobject("figures_dark/gap_distribution.svg").scale_to_fit_width(7)
        plot.next_to(text, DOWN, buff=0.5)
        self.p.play(Write(plot), run_time=1.5)

        self.p.next_slide()

        self.p.play(Unwrite(text), Unwrite(plot), run_time=0.7)

        main_text = r"We also compute the cosine similarity between each pair of modality gap vectors $\text{cos}(\vec{\Delta}^{(c)}, \vec{\Delta}^{(c')})$ and show the resulting distribution."

        text = Tex(main_text, font_size=28)
        text.scale_to_fit_width(config["frame_width"] - 2)
        text.to_edge(UP, buff=1)
        self.p.play(Write(text))

        plot = SVGMobject("figures_dark/pairwise_cosine_distribution.svg").scale_to_fit_width(7)
        plot.next_to(text, DOWN, buff=0.5)
        self.p.play(Write(plot), run_time=1.5)

        self.p.next_slide()

        self.p.play(Unwrite(text), Unwrite(plot), run_time=0.7)

        main_text = r"We also computed the correlation between the concreteness of a concept (scored from 1 to 5[2]) and the norm of its modality gap, and found little correlation"

        # bottom_citation  = Tex(r"[1] Brysbaert, M., Warriner, A. B., & Kuperman, V. (2014). Concreteness ratings for 40 thousand generally known English word lemmas. Behavior research methods, 46(3), 904-911.", font_size=16)
        citations_texts = [
            # "[1] Piyush Sharma et al. ``Conceptual Captions: A Cleaned, Hypernymed, Image Alt-text Dataset For Automatic Image Captioning''. In: Proceedings of ACL. 2018.",
            "[2] Marc Brysbaert et al. “Concreteness ratings for 40 thousand generally known English word lemmas”. In: Behavior research methods 46.3 (2014), pp. 904-911."
        ]
        citations = VGroup(*[Tex(r"\mbox{" + ct + "}", font_size=28) for ct in citations_texts])
        citations.arrange(DOWN, aligned_edge=LEFT, buff=0.25)

        # citations = Tex(r"\mbox{" + citations_text + "}", font_size=36)
        screen_width = config["frame_width"] - 2
        if citations.width > screen_width:
            citations.scale_to_fit_width(screen_width)
        # citations.to_corner(DOWN + LEFT, buff=0.5)
        citations.to_edge(DOWN, buff=0.5)
        citations.to_edge(LEFT, buff=0.5)
        
        
        # wrapped_main_text = textwrap.fill(main_text, width=90)
        # wrapped_main_text = wrapped_main_text.replace("\n", r"\\")
        # print(wrapped_main_text)
        # text = Tex(wrapped_main_text, font_size=20)
        tex_string = r"\begin{minipage}{13cm} " + main_text + r" \end{minipage}"
        text = Tex(tex_string, font_size=28)
        text.scale_to_fit_width(config["frame_width"] - 1)
        text.to_edge(UP, buff=1)
        self.p.play(Write(text), Write(citations))

        plot = SVGMobject("figures_dark/concreteness_vs_gap.svg").scale_to_fit_width(6)
        plot.next_to(text, DOWN, buff=0.5)
        self.p.play(Write(plot), run_time=1.5)
        # self.p.wait(1)
        self.p.next_slide()

        self.p.play(Unwrite(text), Unwrite(citations), Unwrite(plot),Unwrite(rq1), run_time=0.7)

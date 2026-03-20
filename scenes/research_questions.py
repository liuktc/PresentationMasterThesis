# Add .. to the path to import from the parent directory
import sys
import textwrap
sys.path.append("..")

from templates import MySlide


from manim import *

def get_research_questions(title, text, color=BLUE):
    box_width = 10
    header_height = 0.6
    inner_width = box_width - 1.0
    top_padding = 0.2
    bottom_padding = 0.2
    min_body_height = 0.5
    wrap_width = max(18, int(inner_width * 7.5))
    wrapped_text = textwrap.fill(text, width=wrap_width)

    body_text = Paragraph(
        *wrapped_text.split("\n"),
        alignment="left",
        font_size=24,
        line_spacing=0.6,
    )
    body_text.scale_to_fit_width(inner_width)
    body_height = max(body_text.height, min_body_height)
    box_height = header_height + top_padding + body_height + bottom_padding

    background = RoundedRectangle(
        width=box_width,
        height=box_height,
        corner_radius=0.12,
        stroke_color=color,
        stroke_width=2,
        fill_color=color,
        fill_opacity=0.1,
    )

    header = Rectangle(
        width=box_width - 0.04,
        height=header_height,
        stroke_width=0,
        fill_color=color,
        fill_opacity=0.8,
    )
    header.move_to(background.get_top() + DOWN * (header_height / 2 + 0.02))

    separator = Line(
        start=background.get_top() + DOWN * (header_height + 0.02) + LEFT * (box_width / 2 - 0.02),
        end=background.get_top() + DOWN * (header_height + 0.02) + RIGHT * (box_width / 2 - 0.02),
        color=BLUE_E,
        stroke_width=2,
    )

    title_text = Text(title, font_size=26, weight=BOLD)
    title_text.move_to(header.get_center())
    title_text.align_to(background, LEFT)
    title_text.shift(RIGHT * 0.35)

    body_text.next_to(separator, DOWN, buff=top_padding)
    body_text.align_to(title_text, LEFT)

    return VGroup(background, header, separator, title_text, body_text)


class RQScene(MySlide):
    def construct(self):
        # Create a colored block
        rq1 = get_research_questions(
            "RQ1",
            r"Is the modality gap uniform across different semantic concepts?",
            color=BLUE,
        )

        rq2 = get_research_questions(
            "RQ2",
            r"Can SAEs decomposition help us understand the geometry of the modality gap?",
            color=GREEN,
        )

        rq3 = get_research_questions(
            "RQ3",
            r"Can concept-specific gap corrections improve downstream task performance compared to a single global correction?",
            color=RED,
        )

        rq_group = VGroup(rq1, rq2, rq3)
        rq_group.arrange(DOWN, buff=0.5)

        self.p.play(Write(rq1))
        # self.p.wait(1)
        self.p.next_slide()
        self.p.play(Write(rq2))
        # self.p.wait(1)
        self.p.next_slide()
        self.p.play(Write(rq3))
        self.p.next_slide()

        content_to_clear = [rq_group]
        self.p.play(*[FadeOut(mob) for mob in content_to_clear], run_time=0.6)


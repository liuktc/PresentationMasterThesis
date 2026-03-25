from manim import *
from manim_slides import Slide, ThreeDSlide
import numpy as np

from settings import *


class MySlide(Slide):
    def __init__(self, parent_object: Slide = None, **kwargs):
        super().__init__(**kwargs)
        self.DEFAULT_TOP = 3.2
        self.DEFAULT_BOTTOM = -3.5
        if parent_object is None:
            self.p: Slide = self
        else:
            self.p: Slide = parent_object

class MyThreeDSlide(ThreeDSlide):
    def __init__(self, parent_object: ThreeDSlide = None, **kwargs):
        super().__init__(**kwargs)
        self.DEFAULT_TOP = 3.2
        self.DEFAULT_BOTTOM = -3.5
        if parent_object is None:
            self.p: ThreeDSlide = self
        else:
            self.p: ThreeDSlide = parent_object


class SlideTemplate(MySlide):
    def __init__(
        self,
        title_str="Title",
        name="Name",
        subtitle="Subtitle",
        date_text="01/01/1970",
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.content = None
        self.title = None
        self.title_str = title_str
        self.name = name
        self.subtitle = subtitle
        self.date_text = date_text
        self.page_number = 1
        self.page_number_mobject = None

    def add_slide_template(self):
        screen_width = config.frame_width
        # Define the slide title
        self.title = Tex(f"\\textbf{{{self.title_str}}}", font_size=24)
        self.title.to_edge(UP, buff=0.3)
        self.title.to_edge(LEFT, buff=0.5)

        self.title_line = Line(start=screen_width * 2 * LEFT, end=screen_width * 2 * RIGHT)
        # self.title_line.next_to(self.title, DOWN, buff=0.2)
        self.title_line.set_y(self.DEFAULT_TOP)


        DOWN_BUFF = 0.15
        # Define the subtitle
        subtitle = Tex(f"\\textit{{{self.subtitle}}}", font_size=24)
        subtitle.to_edge(DOWN, buff=DOWN_BUFF)

        self.page_number_mobject = Tex(self.page_number, font_size=24)
        self.page_number_mobject.to_edge(DOWN, buff=DOWN_BUFF)
        self.page_number_mobject.to_edge(RIGHT, buff=0.5)

        # # Define the footer with the date
        date_text = Tex(self.date_text, font_size=24)
        # Put the date text at the bottom right of the screen
        # date_text.to_edge(DOWN)
        # date_text.to_edge(DOWN, buff=DOWN_BUFF)
        # date_text.to_edge(RIGHT, buff=4.5)
        date_text.next_to(self.page_number_mobject, LEFT, buff=0.5)

        # # Define the footer with the website URL
        name = Tex(f"\\textbf{{{self.name}}}", font_size=24)
        # url_text.next_to(date_text, UP, buff=0.2)
        name.to_edge(DOWN, buff=DOWN_BUFF)
        name.to_edge(LEFT, buff=0.5)

        self.line = Line(start=screen_width * 2 * LEFT, end=screen_width * 2 * RIGHT)
        # self.line.next_to(subtitle, UP, buff=0.1)
        self.line.set_y(self.DEFAULT_BOTTOM)
        self.line.set_stroke(width=2)

        # Play more animations at the same time
        self.play(
            Write(subtitle),  # Fade in the subtitle
            Write(date_text),  # Fade in the date text
            Write(name),  # Fade in the URL text
            Create(self.line),  # Fade in the line
            Write(self.title),  # Fade in the title
            Create(self.title_line),  # Fade in the title line
            Write(self.page_number_mobject),  # Fade in the page number
        )

    # def get_top(self):
    #     return self.title_line.get_y()
    
    # def get_bottom(self):
    #     return self.line.get_y()

    def add_content(self, content: Mobject):
        self.content = content
        if content.width > config.frame_width * 0.9:
            before_width = content.width
            content.scale_to_fit_width(config.frame_width * 0.9)
            after_width = content.width
            print(
                f"Before width: {before_width}, After width: {after_width}, Scale: {after_width / before_width}"
            )

        content.next_to(self.title, DOWN, buff=1)
        content.align_to(self.title, LEFT)
        self.play(Write(content))
        # self.wait(1)  # Wait for a moment to let the content be visible

    def remove_content(self):
        self.play(FadeOut(self.content))
        self.content = None

    def change_title(self, new_title: str):
        # Create a new title object with the new text
        new_title_obj = Tex(f"\\textbf{{{new_title}}}", font_size=24)
        new_title_obj.move_to(self.title.get_center())
        new_title_obj.align_to(self.title, LEFT)  # Align to the left of the old title

        # Animate the replacement of the old title with the new one
        self.play(ReplacementTransform(self.title, new_title_obj))
        self.title = new_title_obj

    def add_page_number(self):
        self.page_number += 1

        if self.page_number_mobject:
            new_page_number_mobject = Tex(self.page_number, font_size=24)
            new_page_number_mobject.move_to(self.page_number_mobject.get_center())
            self.play(
                ReplacementTransform(self.page_number_mobject, new_page_number_mobject)
            )
            self.page_number_mobject = new_page_number_mobject

    def change_title_and_add_page_number(self, new_title: str, **kwargs):
        # Create a new title object with the new text
        new_title_obj = Tex(f"\\textbf{{{new_title}}}", font_size=24, **kwargs)
        new_title_obj.move_to(self.title.get_center())
        new_title_obj.align_to(self.title, LEFT)  # Align to the left of the old title

        # Animate the replacement of the old title with the new one

        self.page_number += 1

        new_page_number_mobject = Tex(self.page_number, font_size=24)
        new_page_number_mobject.move_to(self.page_number_mobject.get_center())

        self.play(
            [
                ReplacementTransform(self.title, new_title_obj),
                ReplacementTransform(self.page_number_mobject, new_page_number_mobject),
            ]
        )

        self.title = new_title_obj
        self.page_number_mobject = new_page_number_mobject




class TitleSlide(MySlide):
    def construct(
        self,
        title_str="Title of the Slide",
        name="Luca Domeniconi",
        date_text="2025-04-24",
        run_time=1.0,
    ):
        # Build the title imitating the beamer style
        title = Tex(title_str, font_size=48)
        title.to_edge(UP, buff=1)

        title_rect = SurroundingRectangle(
            title,
            color=WHITE,
            buff=0.5,
            stroke_width=2,
            fill_opacity=0.5,
            corner_radius=0.2,
        )

        title_group = VGroup(title, title_rect)

        # Add the author
        author = Tex(name, font_size=30)
        author.next_to(title_group, DOWN, buff=0.5)

        supervisor_title = Tex("Supervisor:", font_size=24)
        cosupervisors_title = Tex(r"Co-supervisors$^\dagger$:", font_size=24)
        
        titles = VGroup(supervisor_title, cosupervisors_title).arrange(RIGHT, buff=2)
        titles.next_to(author, DOWN, buff=0.5)

        supervisor = Tex(r"Prof. Samuele Salti", font_size=28)
        cosupervisors = VGroup(
            Tex(r"Prof. Andrea Cavallaro", font_size=28),
            Tex(r"Dr. Darya Baranouskaya", font_size=28),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)

        supervisor.next_to(supervisor_title, DOWN, buff=0.2)
        cosupervisors.next_to(cosupervisors_title, DOWN, buff=0.2)

        # Center things relative to their titles
        supervisor.match_x(supervisor_title)
        cosupervisors.match_x(cosupervisors_title)

        supervisors_group = VGroup(supervisor, cosupervisors, titles)

        # Add footnote with EPFL logo
        epfl_logo = SVGMobject("epfl_logo.svg")
        epfl_logo.scale_to_fit_height(0.3)
        
        footnote = VGroup(
            Tex(r"$\dagger$ {\textit{École polytechnique fédérale de Lausanne}}", font_size=20),
            epfl_logo
        ).arrange(RIGHT, buff=0.2)
        footnote.to_edge(DOWN, buff=0.2).to_edge(LEFT, buff=0.5)

        # Add the university
        university = Tex(
            r"Department of Computer Science and Engineering\\University of Bologna",
            font_size=24,
        )
        university.next_to(supervisors_group, DOWN, buff=0.8)

        # Add the date
        date = Tex(date_text, font_size=30)
        date.next_to(university, DOWN, buff=0.5)

        self.p.play(Write(title_group), run_time=run_time)
        self.p.play(
            Write(author),
            Write(university),
            Write(date),
            Write(supervisor),
            Write(cosupervisors),
            Write(supervisor_title),
            Write(cosupervisors_title),
            Write(footnote),
            run_time=run_time,
        )
        self.p.next_slide()
        # Unwrite everythin
        self.p.play(
            Unwrite(title_group),
            Unwrite(author),
            Unwrite(university),
            Unwrite(date),
            Unwrite(supervisor),
            Unwrite(cosupervisors),
            Unwrite(supervisor_title),
            Unwrite(cosupervisors_title),
            Unwrite(footnote),
        )

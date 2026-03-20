# Add .. to the path to import from the parent directory
import sys
sys.path.append("..")

from templates import MySlide


from manim import *


class CustomTypeWithCursor(TypeWithCursor):
    def __init__(self, text, **kwargs):
        target = text[0] if len(text) > 0 else text
        cursor_width = max(target.width * 0.9, 0.08)
        cursor_height = max(target.height * 1.05, 0.2)

        self.cursor = Rectangle(
            color = GREY_A,
            fill_color = GREY_A,
            fill_opacity = 0.6,
            height = cursor_height,
            width = cursor_width,
        ).move_to(target)
        super().__init__(text, self.cursor, **kwargs)


class VLMSScene(MySlide):
    def construct(self):
        # The slide will be divided into two columns
        # First column for LLM only
        # Second column for VLMs

        llm = Rectangle(width=3, height=2, color=GRAY, fill_opacity=0.5)
        llm.to_edge(LEFT, buff=2)
        llm_text = Tex(r"Large\\Language\\Model", font_size=24).scale_to_fit_width(llm.width * 0.6)
        llm_text.move_to(llm.get_center())

        self.p.play(Create(llm), Write(llm_text))

        input_text = Text(r"What is the capital of France?", font_size=24, font="Monospace")
        input_text_background = SurroundingRectangle(input_text, color=BLUE, buff=0.2)
        input_text_group = VGroup(input_text, input_text_background)
        input_text_group.next_to(llm, DOWN, buff=1)
        arrow = Arrow(start=input_text_group.get_top(), end=llm.get_bottom(), buff=0.1)
        
        anim = CustomTypeWithCursor(input_text)
        
        self.p.play(anim, Create(arrow), Create(input_text_background), run_time=1)
        self.p.remove(anim.cursor)  # Remove the cursor after typing animation is done
        # self.p.play(FadeOut(anim.cursor), run_time=0.1)
        # return
        answer = Text(r"The capital of France is Paris.", font_size=24, font="Monospace")
        answer_background = SurroundingRectangle(answer, color=BLUE, buff=0.2)
        answer_group = VGroup(answer, answer_background)
        answer_group.next_to(llm, UP, buff=1)
        arrow2 = Arrow(start=llm.get_top(), end=answer_group.get_bottom(), buff=0.1)
        
        anim = CustomTypeWithCursor(answer)

        self.p.play(Create(arrow2), anim, Create(answer_background), run_time=1)
        self.p.remove(anim.cursor)  # Remove the cursor after typing animation is done

        self.p.next_slide()
        # Draw a line to separate the two columns
        line = Line(start=ORIGIN + UP * self.DEFAULT_TOP, end=ORIGIN + UP * self.DEFAULT_BOTTOM)
        # line.set_length(config.frame_height * 2)
        line.set_stroke(width=2)
        # line.move_to(ORIGIN)
        self.p.play(Create(line))


        vlm = Rectangle(width=5, height=2, color=PURPLE, fill_opacity=0.5)
        vlm.to_edge(RIGHT, buff=1)
        vlm_text = Tex(r"Vision\\Language\\Model", font_size=24).scale_to_fit_width(3 * 0.6)
        vlm_text.move_to(vlm.get_center())

        self.p.play(Create(vlm), Write(vlm_text))
        text_input = Text("What is in this image?", font_size=20, font="Monospace")
        text_input_background = SurroundingRectangle(text_input, color=BLUE, buff=0.2)
        text_input_group = VGroup(text_input, text_input_background)

        image_input = ImageMobject("eiffel_tower.jpg").scale_to_fit_width(1.3)
        image_input_background = SurroundingRectangle(image_input, color=GREEN, buff=0.1)
        image_input = Group(image_input, image_input_background)
        
        input_group = Group(text_input_group, image_input)
        input_group.arrange(RIGHT, buff=0.5)
        input_group.next_to(vlm, DOWN, buff=0.8)

        arrow1_start = text_input_group.get_top()
        arrow1_end = vlm.get_bottom()
        arrow1_end[0] = arrow1_start[0]  # Align the x-coordinates

        arrow2_start = image_input.get_top()
        arrow2_end = vlm.get_bottom()
        arrow2_end[0] = arrow2_start[0]  # Align the x-coordinates


        arrow11 = Arrow(start=arrow1_start, end=arrow1_end, buff=0.1)
        arrow12 = Arrow(start=arrow2_start, end=arrow2_end, buff=0.1)
        
        anim = CustomTypeWithCursor(text_input)
        self.p.play(anim, FadeIn(image_input), Create(arrow11), Create(arrow12), Create(text_input_background), Create(image_input_background), run_time=1)
        self.p.remove(anim.cursor)  # Remove the cursor after typing animation is done
        self.p.wait(1)
        self.p.play(Circumscribe(image_input, color=YELLOW, buff=0.1))


        answer2 = Tex(r"\texttt{This is a picture of\\the Eiffel Tower.}", font_size=32)
        answer2_background = SurroundingRectangle(answer2, color=BLUE, buff=0.2)
        answer2 = VGroup(answer2, answer2_background)
        answer2.next_to(vlm, UP, buff=1)
        arrow3 = Arrow(start=vlm.get_top(), end=answer2.get_bottom(), buff=0.1)
        self.p.play(Create(arrow3), Write(answer2))

        self.p.next_slide()

        # Remove everything
        self.p.play(
            Uncreate(llm), Unwrite(llm_text), Uncreate(arrow), Uncreate(arrow2), Unwrite(input_text), Unwrite(answer),
            Uncreate(line),
            Uncreate(vlm), Unwrite(vlm_text), Uncreate(arrow11), Uncreate(arrow12), Unwrite(text_input), FadeOut(image_input), Unwrite(answer2), Uncreate(arrow3),
            Uncreate(text_input_background), Uncreate(image_input_background), Uncreate(answer2_background), Uncreate(input_text_background), Uncreate(answer_background)
        )
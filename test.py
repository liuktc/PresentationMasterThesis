from manim import *

class TestScene(Scene):
    def construct(self):
        text = Text("Hello, Manim!")
        formula = MathTex(r"E=mc^2")
        formula.next_to(text, DOWN, buff=0.5)
        self.play(Write(text))
        self.play(Write(formula))
        self.wait(2)
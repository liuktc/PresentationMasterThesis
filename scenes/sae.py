# Add .. to the path to import from the parent directory
import sys
sys.path.append("..")

from templates import MySlide


from manim import *
from .nn import NN


class SAEScene(MySlide):
    def construct(self):
        # Sparse autoencoders
        # 1. Configuration
        nn = NN(
            layers=[2, 6, 2],
            scene=self.p,
            labels=[r"\mathbf{x}", r"\mathbf{z}", r"\mathbf{\hat{x}}"],
            ellipsis_layers=[0,1,2],
            # layer_spacing=3,
            rotate=False
        )  # Input, Hidden (Sparse), Output
        nn.get_all_mobjects().scale(0.9)
        nn.display()

        # test_activations = [
        #     [0.1, 0.9],  # Input layer activations
        #     [0.05, 0.95, 0.1, 0.9, 0.2, 0.8],  # Hidden layer (sparse) activations
        #     [0.1, 0.9]   # Output layer activations
        # ]
        # nn.set_activations(test_activations)

        # Draw an arrow between the firts and last layer by doing square corners
        points = [nn.neurons[0].get_top() + UP * 0.1,
                    nn.neurons[0].get_top() + UP * 1.7,
                    nn.neurons[-1].get_top() + UP * 1.7,
                    nn.neurons[-1].get_top() + UP * 0.1]
        
        lines = VGroup(*[Line(points[i], points[i+1], color=YELLOW) for i in range(len(points)-1)])

        text_on_lines = MathTex(r"\mathcal{L}_{\text{reconstruction}}(\mathbf{x}, \mathbf{\hat{x}}) = \|\mathbf{x} - \mathbf{\hat{x}}\|^2", font_size=36)
        text_on_lines.next_to(lines, UP)
        self.p.play(Create(lines), Write(text_on_lines))
        self.p.next_slide()
        # self.p.play(Create(line))

        central_rectangle = SurroundingRectangle(nn.neurons[1], color=YELLOW, buff=0.2, corner_radius=0.1)
        text_on_rectangle = MathTex(r"\mathcal{L}_{\text{sparsity}} (\mathbf{z}) = \|\mathbf{z} \|_1", font_size=36)
        text_on_rectangle.next_to(central_rectangle, DOWN, buff=0.8)

        self.p.play(Create(central_rectangle), Write(text_on_rectangle))
        self.p.next_slide()

        all_elements = VGroup(*nn.get_all_mobjects(), lines, text_on_lines, central_rectangle, text_on_rectangle)
        self.p.play(all_elements.animate.scale(0.8).to_edge(LEFT))

        full_formula = MathTex(
            r"\mathcal{L} = \mathcal{L}_{\text{reconstruction}}(\mathbf{x}, \mathbf{\hat{x}}) + \lambda \mathcal{L}_{\text{sparsity}}(\mathbf{z})",
            substrings_to_isolate=[r"\lambda"],
            font_size=48
        )
        # full_formula.set_color_by_tex(r"\lambda", RED)
        # Play indicate animation on lambda
        full_formula.next_to(all_elements, RIGHT, buff=0.5)
        self.p.play(Write(full_formula))
        self.p.play(Indicate(full_formula.get_part_by_tex(r"\lambda")))

        self.p.next_slide()
        self.p.play(Unwrite(full_formula), Unwrite(all_elements))
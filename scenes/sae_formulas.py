# Add .. to the path to import from the parent directory
import sys
sys.path.append("..")

from manim_slides import ThreeDSlide
from templates import MySlide

from manim import *
from .nn import NN


class SAEFormulasScene(MySlide):
    def construct(self):
        # Sparse autoencoders
        # 1. Configuration
        rotate = False
        nn = NN(
            layers=[2, 6, 2],
            scene=self.p,
            labels=[r"\mathbf{x}", r"\mathbf{z}", r"\mathbf{\hat{x}}"],
            ellipsis_layers=[0,1,2],
            rotate=rotate
        )  # Input, Hidden (Sparse), Output
        # nn.get_all_mobjects().shift(UP)
        # nn.get_all_mobjects().to_edge(UP, buff=1)
        nn.get_all_mobjects().move_to(ORIGIN)
        nn.display()

        # Add the fact that the input x comes from CLIP embeddings
        input_label = Tex("CLIP Embeddings", font_size=24)
        input_background = SurroundingRectangle(input_label, fill_opacity=0.1, buff=0.2, corner_radius=0.1)
        input_background.set_stroke(color=[BLUE, GREEN], width=3)
        input_background.set_fill(color=[BLUE, GREEN], opacity=0.1)
        input_group = VGroup(input_background, input_label)
        
        if not rotate:
            input_group.rotate(-PI / 2)
        input_group.next_to(nn.neurons, DOWN if rotate else LEFT, buff=1)

        arrow = Arrow(start=input_group.get_top() if rotate else input_group.get_right(), end=nn.neurons.get_bottom() if rotate else nn.neurons.get_left(), buff=0.1, color=WHITE)
        input_group.add(arrow)

        # Draw a bracket below the input group to indicate the dimensionality of CLIP embeddings
        bracket = Brace(input_group, direction=DOWN if rotate else LEFT, buff=0.2)
        dim_text = Tex("D-dimensional", font_size=24)
        dim_text.next_to(bracket, DOWN if rotate else LEFT, buff=0.1)
        bracket.add(dim_text)

        input_group.add(bracket)
        self.p.play(Write(input_group), run_time=0.8)
        self.p.next_slide()

        self.p.play(Unwrite(input_group), run_time=0.5)
        self.p.play(nn.get_all_mobjects().animate.move_to(ORIGIN).to_edge(LEFT, buff=0.5).to_edge(DOWN, buff=1).scale(0.8), run_time=1)
        
        # Add text on top
        text_str = "To quantify the modality-specific information in the sparse hidden layer of the SAE, we define the Modality-Specific Index (MSI) for each neuron k."
        text = Tex(text_str).scale_to_fit_width(config["frame_width"] - 1)
        text.to_edge(UP, buff=1)
        text.to_edge(LEFT, buff=0.5)


        self.p.play(Write(text), run_time=0.8)
        self.p.next_slide()
        # test_activations = [
        #     [0.1, 0.9],  # Input layer activations
        #     [0.05, 0.95, 0.1, 0.9, 0.2, 0.8],  # Hidden layer (sparse) activations
        #     [0.1, 0.9]   # Output layer activations
        # ]
        # nn.set_activations(test_activations)
        # return 
        formulas = [
            MathTex(
                r"\bar{a}_k^{\text{img}} = \frac{1}{N}\sum_{i=1}^{N}",
                r"z_k(\mathbf{v}_i)",
                r"\quad",
                r"\bar{a}_k^{\text{txt}} = \frac{1}{N}\sum_{i=1}^{N}",
                r"z_k(\mathbf{t}_i)",
                font_size=36,
                substrings_to_isolate=[r"\mathbf{v}_i", r"\mathbf{t}_i", r"\bar{a}_k^{\text{img}}", r"\bar{a}_k^{\text{txt}}"]
            ),
            MathTex(r"\text{MSI}_k = \frac{|\bar{a}_k^{\text{img}} - \bar{a}_k^{\text{txt}}|}{\bar{a}_k^{\text{img}} + \bar{a}_k^{\text{txt}}} \quad \text{MSI}_k \in [0, 1]", font_size=36,
                    substrings_to_isolate=[r"\bar{a}_k^{\text{img}}", r"\bar{a}_k^{\text{txt}}"]),
            MathTex(
                r"\text{MSI}^{(c)} = \frac{\sum_{k=1}^{D} ",
                r"\bar{a}_k^{(c)}",
                r"\cdot \text{MSI}_k}{\sum_{k=1}^{D} ",
                r"\bar{a}_k^{(c)}",
                r"}",
                font_size=36,
            )
        ]

        # Color v_i in green and t_i in blue
        # Color img stuff in green and txt stuff in blue
        formulas[0].set_color_by_tex(r"\mathbf{v}_i",GREEN)
        formulas[0].set_color_by_tex(r"\mathbf{t}_i",BLUE)
        formulas[0].set_color_by_tex(r"\bar{a}_k^{\text{img}}",GREEN)
        formulas[0].set_color_by_tex(r"\bar{a}_k^{\text{txt}}",BLUE)
        formulas[1].set_color_by_tex(r"\bar{a}_k^{\text{img}}",GREEN)
        formulas[1].set_color_by_tex(r"\bar{a}_k^{\text{txt}}",BLUE)

        formulas[2][1].set_color_by_gradient(GREEN, BLUE)
        formulas[2][3].set_color_by_gradient(GREEN, BLUE)

        formulas_group = VGroup(*formulas)
        formulas_group.arrange(DOWN, buff=0.5)
        formulas_group.next_to(nn.get_all_mobjects(), RIGHT, buff=0 if rotate else 1)
        # formulas_group.to_edge(RIGHT, buff=1)
        # formulas_group.to_edge(UP, buff=1.5)

        self.p.play(Write(formulas[0]), Write(formulas[1]), Write(formulas[2]), run_time=1)

        hidden_layer = nn.neurons[1]
        z_layer_label = nn.labels_mobjects[1]
        # z_formula_terms = VGroup(formulas[0][1], formulas[0][3])



        # self.p.play(
        #     Indicate(hidden_layer, color=YELLOW, scale_factor=1.05),
        #     Indicate(z_layer_label, color=YELLOW, scale_factor=1.1),
        #     Indicate(z_formula_terms, color=YELLOW, scale_factor=1.1),
        #     run_time=1.2,
        # )

        highlight_hidden = SurroundingRectangle(hidden_layer, color=YELLOW, buff=0.15)
        highlight_z_img = SurroundingRectangle(formulas[0][1], color=YELLOW, buff=0.15)
        highlight_z_txt = SurroundingRectangle(formulas[0][4], color=YELLOW, buff=0.15)

        self.p.play(
            Create(highlight_hidden),
            # Create(SurroundingRectangle(z_layer_label, color=YELLOW, buff=0.1)),
            Create(highlight_z_img),
            Create(highlight_z_txt),
        )
        self.p.next_slide()

        to_remove = formulas[0]
        formulas_group.remove(formulas[0])

        self.p.play(Unwrite(to_remove), formulas_group.animate.shift(UP * 1.5), Uncreate(highlight_z_img), Uncreate(highlight_z_txt), Uncreate(highlight_hidden))

        gap_energy_formula = MathTex(r"E_k^{(c)} = \left( \frac{1}{N^{(c)}} \sum_{i=1}^{N^{(c)}} \left( z_k(\mathbf{v}_i^{(c)}) -  z_k(\mathbf{t}_i^{(c)}) \right) \right)^2",
                                     font_size=36,
                                     substrings_to_isolate=[r"\mathbf{v}_i^{(c)}", r"\mathbf{t}_i^{(c)}"])
        gap_energy_formula.set_color_by_tex(r"\mathbf{v}_i^{(c)}", GREEN)
        gap_energy_formula.set_color_by_tex(r"\mathbf{t}_i^{(c)}", BLUE)
        gap_energy_formula.next_to(formulas_group, DOWN, buff=0.5)
        self.p.play(Write(gap_energy_formula))



        self.p.next_slide()
        self.p.play(
            Uncreate(highlight_hidden),
            Uncreate(highlight_z_img),
            Uncreate(highlight_z_txt),
            Unwrite(formulas[0]),
            Unwrite(formulas[1]),
            Unwrite(formulas[2]),
            Unwrite(gap_energy_formula),    
            # Unwrite(formulas[3]),
            Uncreate(nn.get_all_mobjects()),
            Unwrite(text),
        )

        # self.p.play(formulas[2].animate.move_to(ORIGIN).to_edge(LEFT, buff=1), run_time=0.5)

        # self.add_fixed_in_frame_mobjects(
        #     nn.get_all_mobjects(),
        #     formulas_group,
        #     highlight_hidden,
        #     highlight_z_img,
        #     highlight_z_txt,
        # )


        # # Now create a 3D plot showing the plot of MSI for every value of a_img and a_txt
        # a_img_values = np.linspace(0.01, 1, 30)
        # a_txt_values = np.linspace(0.01, 1, 30)
        # a_img_grid, a_txt_grid = np.meshgrid(a_img_values, a_txt_values)
        # msi_grid = np.abs(a_img_grid - a_txt_grid) / (a_img_grid + a_txt_grid)  

        # axes = ThreeDAxes(x_range=[0, 1, 0.2], y_range=[0, 1, 0.2], z_range=[0, 1, 0.2], x_length=4, y_length=4, z_length=4)
        # axes.scale(0.9)
        # axes.to_edge(RIGHT, buff=0.5)
        # surface = Surface(
        #     lambda u, v: axes.c2p(u, v, np.abs(u - v) / (u + v)),
        #     u_range=[0.01, 1],
        #     v_range=[0.01, 1],
        #     resolution=(30, 30),
        #     fill_opacity=0.8,
        #     checkerboard_colors=[BLUE_D, BLUE_E],
        # )

        # rotation_center = axes.c2p(0.5, 0.5, 0.25)
        # right_side_offset = LEFT * 1.8

        # self.move_camera(
        #     phi=65 * DEGREES,
        #     theta=-45 * DEGREES,
        #     frame_center=rotation_center + right_side_offset,
        #     run_time=1,
        # )
        # self.begin_ambient_camera_rotation(rate=0.2)
        # self.p.play(Create(axes), Create(surface), run_time=2)
        # self.p.wait(1)
        # self.stop_ambient_camera_rotation()
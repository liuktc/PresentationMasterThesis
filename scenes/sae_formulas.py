# Add .. to the path to import from the parent directory
import sys
sys.path.append("..")

from manim_slides import ThreeDSlide
from templates import MySlide, MyThreeDSlide
from settings import IMAGE_COLOR, TEXT_COLOR

from manim import *
from .nn import NN
import math


class SAEFormulasScene(MyThreeDSlide):
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
        input_background.set_stroke(color=[TEXT_COLOR, IMAGE_COLOR], width=3)
        input_background.set_fill(color=[TEXT_COLOR, IMAGE_COLOR], opacity=0.1)
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
            MathTex(r"\text{MSI}_k = \frac{|\bar{a}_k^{\text{img}} - \bar{a}_k^{\text{txt}}|}{\bar{a}_k^{\text{img}} + \bar{a}_k^{\text{txt}}}", font_size=36,
                    substrings_to_isolate=[r"\bar{a}_k^{\text{img}}", r"\bar{a}_k^{\text{txt}}"]),
            MathTex(r"\text{MSI}_k \in [0, 1]", font_size=36),
            # MathTex(
            #     r"\text{MSI}^{(c)} = \frac{\sum_{k=1}^{D} ",
            #     r"\bar{a}_k^{(c)}",
            #     r"\cdot \text{MSI}_k}{\sum_{k=1}^{D} ",
            #     r"\bar{a}_k^{(c)}",
            #     r"}",
            #     font_size=36,
            # )
        ]

        # Color v_i in green and t_i in blue
        # Color img stuff in green and txt stuff in blue
        formulas[0].set_color_by_tex(r"\mathbf{v}_i", IMAGE_COLOR)
        formulas[0].set_color_by_tex(r"\mathbf{t}_i", TEXT_COLOR)
        formulas[0].set_color_by_tex(r"\bar{a}_k^{\text{img}}", IMAGE_COLOR)
        formulas[0].set_color_by_tex(r"\bar{a}_k^{\text{txt}}", TEXT_COLOR)
        formulas[1].set_color_by_tex(r"\bar{a}_k^{\text{img}}", IMAGE_COLOR)
        formulas[1].set_color_by_tex(r"\bar{a}_k^{\text{txt}}", TEXT_COLOR)

        # formulas[2][1].set_color_by_gradient(IMAGE_COLOR, TEXT_COLOR)
        # formulas[2][3].set_color_by_gradient(IMAGE_COLOR, TEXT_COLOR)

        bottom_group = VGroup(formulas[1], formulas[2])
        bottom_group.arrange(RIGHT, buff=0.5)

        formulas_group = VGroup(formulas[0], bottom_group)
        formulas_group.arrange(DOWN, buff=1)
        formulas_group.next_to(nn.get_all_mobjects(), RIGHT, buff=0 if rotate else 1)
        # formulas_group.to_edge(RIGHT, buff=1)
        # formulas_group.to_edge(UP, buff=1.5)

        self.p.play(Write(formulas_group), run_time=1)

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

        # self.p.play(Unwrite(to_remove), formulas_group.animate.shift(UP * 1.5), Uncreate(highlight_z_img), Uncreate(highlight_z_txt), Uncreate(highlight_hidden))

        # Moved to appendix
        # gap_energy_formula = MathTex(r"E_k^{(c)} = \left( \frac{1}{N^{(c)}} \sum_{i=1}^{N^{(c)}} \left( z_k(\mathbf{v}_i^{(c)}) -  z_k(\mathbf{t}_i^{(c)}) \right) \right)^2",
        #                              font_size=36,
        #                              substrings_to_isolate=[r"\mathbf{v}_i^{(c)}", r"\mathbf{t}_i^{(c)}"])
        # gap_energy_formula.set_color_by_tex(r"\mathbf{v}_i^{(c)}", IMAGE_COLOR)
        # gap_energy_formula.set_color_by_tex(r"\mathbf{t}_i^{(c)}", TEXT_COLOR)
        # gap_energy_formula.next_to(formulas_group, DOWN, buff=0.5)
        # self.p.play(Write(gap_energy_formula))



        self.p.next_slide()
        self.p.play(
            Uncreate(highlight_hidden),
            Uncreate(highlight_z_img),
            Uncreate(highlight_z_txt),
            Unwrite(formulas_group[:-1]),
            # Unwrite(formulas[0]),
            # Unwrite(formulas[1]),
            # Unwrite(formulas[2]),
            # Unwrite(formulas[3]),
            Uncreate(nn.get_all_mobjects()),
            Unwrite(text),
            bottom_group.animate.arrange(DOWN, buff=0.5).to_edge(LEFT, buff=0.5)
        )

        # self.p.play(formulas[2].animate.move_to(ORIGIN).to_edge(LEFT, buff=1), run_time=0.5)

        # self.add_fixed_in_frame_mobjects(
        #     nn.get_all_mobjects(),
        #     formulas_group,
        #     highlight_hidden,
        #     highlight_z_img,
        #     highlight_z_txt,
        # )

        self.add_fixed_in_frame_mobjects(
            formulas_group,
        )
        RESOLUTION = 200  # higher = smoother
        u = np.linspace(0.01, 2, RESOLUTION)
        v = np.linspace(0.01, 2, RESOLUTION)
        U, V = np.meshgrid(u, v)

        # Define your MSI function (2D)
        eps = 1e-3
        Z = np.abs(U - V) / (U + V + eps)

        # Normalize values to 0..1
        Z_norm = (Z - Z.min()) / (Z.max() - Z.min())

        # Map values to a colormap (viridis)
        import matplotlib.cm
        #cmap = matplotlib.cm.viridis
        cmap = matplotlib.cm.magma
        colors = (cmap(Z_norm)[:, :, :3] * 255).astype(np.uint8)  # drop alpha channel

        # Manim wants height x width
        img_array = np.flipud(colors)  # flip so origin is bottom-left

        from PIL import Image
        heatmap_img = Image.fromarray(img_array)
        heatmap_mob = ImageMobject(heatmap_img)

        axes_2d = Axes(
            x_range=[0, 2, 0.4],
            y_range=[0, 2, 0.4],
            x_length=4.5,
            y_length=4.5,
            tips=False,
            axis_config={"include_numbers": True, "font_size": 20},
        )

        heatmap_mob.stretch_to_fit_width(axes_2d.x_length)
        heatmap_mob.stretch_to_fit_height(axes_2d.y_length)
        heatmap_mob.move_to(axes_2d.c2p(2/2, 2/2))

        axes_2d_labels = axes_2d.get_axis_labels(
            MathTex(r"\bar{a}_{img}").set_color(IMAGE_COLOR),
            MathTex(r"\bar{a}_{txt}").set_color(TEXT_COLOR),
        )

        colorbar_resolution = 256
        colorbar_width_px = 24
        colorbar_values = np.linspace(1, 0, colorbar_resolution)[:, None]
        colorbar_rgb = (cmap(colorbar_values)[:, :, :3] * 255).astype(np.uint8)
        colorbar_rgb = np.repeat(colorbar_rgb, colorbar_width_px, axis=1)

        colorbar_img = Image.fromarray(colorbar_rgb)
        colorbar_mob = ImageMobject(colorbar_img)
        colorbar_mob.stretch_to_fit_height(axes_2d.y_length)
        colorbar_mob.stretch_to_fit_width(0.25)
        colorbar_mob.next_to(axes_2d_labels, RIGHT, buff=0.25)
        colorbar_mob.set_y(heatmap_mob.get_y())  # Align vertically with heatmap

        colorbar_frame = SurroundingRectangle(colorbar_mob, buff=0, stroke_width=1)
        colorbar_top = MathTex("1").scale(0.45).next_to(colorbar_mob, RIGHT, buff=0.12).align_to(colorbar_mob, UP)
        colorbar_bottom = MathTex("0").scale(0.45).next_to(colorbar_mob, RIGHT, buff=0.12).align_to(colorbar_mob, DOWN)
        colorbar_label = Tex("MSI").scale(0.5).next_to(colorbar_mob, RIGHT, buff=0.35)

        heatmap_group = Group(
            heatmap_mob,
            axes_2d,
            axes_2d_labels,
            colorbar_mob,
            colorbar_frame,
            colorbar_top,
            colorbar_bottom,
            colorbar_label,
        )
        # heatmap_group.to_edge(DOWN, buff=0.2).to_edge(LEFT, buff=0.6)
        heatmap_group.next_to(bottom_group, RIGHT, buff=1)

        # self.add(heatmap_group)
        self.p.play(FadeIn(heatmap_group))
        # self.wait(2)
        self.p.next_slide()
        self.p.play(FadeOut(heatmap_group), Unwrite(bottom_group), run_time=0.7)
        


        return 
        # Now create a 3D plot showing the plot of MSI for every value of a_img and a_txt
        RESOLUTION = 48  # smoother surface

        # def msi(u, v):
        #     eps = 0.02
        #     diff = u - v
        #     smooth_abs = abs(diff) if abs(diff) > eps else (diff**2) / (2 * eps) + eps / 2
        #     return smooth_abs / (u + v + 1e-6)

        def msi(u, v):
            eps = 1e-3
            return abs(u - v) / (u + v + eps)

        # Axes
        axes = ThreeDAxes(
            x_range=[0.01, 1, 0.2],
            y_range=[0.01, 1, 0.2],
            z_range=[0, 1, 0.2],
            x_length=5,
            y_length=5,
            z_length=3,
        )

        labels = axes.get_axis_labels(
            MathTex(r"\bar{a}_{img}").set_color(IMAGE_COLOR),
            MathTex(r"\bar{a}_{txt}").set_color(TEXT_COLOR),
            MathTex(r"MSI")
        )

        z_min_label = MathTex("0").scale(0.5)
        z_max_label = MathTex("1").scale(0.5)
        z_min_label.next_to(axes.c2p(0.01, 0.01, 0), LEFT, buff=0.08)
        z_max_label.next_to(axes.c2p(0.01, 0.01, 1), LEFT, buff=0.08)
        # Rotate so they points upwards
        z_min_label.rotate(PI / 2, axis=RIGHT)
        z_max_label.rotate(PI / 2, axis=RIGHT)

        z_endpoint_labels = VGroup(z_min_label, z_max_label)

        axes_group = VGroup(axes, labels)
        # axes_group.scale(0.9).to_edge(RIGHT, buff=0.2)

        # Surface with smooth coloring
        surface = Surface(
            lambda u, v: axes.c2p(u, v, msi(u, v)),
            u_range=[0.05, 1],
            v_range=[0.05, 1],
            resolution=(RESOLUTION, RESOLUTION),
            stroke_width=0,
        )

        # Apply gradient based on height (z-value)
        surface.set_style(fill_opacity=0.9, stroke_width=0.2)
        surface.set_fill_by_value(
            axes=axes,
            colors=[
                (BLUE, 0),
                (GREEN, 0.3),
                (YELLOW, 0.6),
                (RED, 1),
            ],
            axis=2,
        )

        # Lighting improves depth perception
        self.renderer.camera.light_source.move_to(3 * OUT + 2 * LEFT)

        

        plot_group = VGroup(axes, surface, labels, z_endpoint_labels).scale(0.9)


        rotation_center = axes_group.get_center()
        frame_center = rotation_center

        # # Set initial camera position
        self.set_camera_orientation(
            phi=65 * DEGREES,
            theta=0 * DEGREES,
            frame_center=frame_center,
        )

        # Move the plot group
        plot_group.move_to(ORIGIN + UP * 3 + 2 * LEFT)
        # z_endpoint_labels.shift(UP * 3)

        # plot_group.rotate(PI / 4, axis=OUT, about_point=plot_group.get_center())

        self.play(Create(axes), Create(surface), Write(labels), Write(z_endpoint_labels), run_time=1)
        # Rotate the object instead of the camera
        # self.play(
        #     Rotate(
        #         plot_group,
        #         angle=2 * PI,
        #         axis=OUT,  # rotate around vertical axis
        #         about_point=plot_group.get_center(),
        #     ),
        #     run_time=1,
        #     rate_func=linear,
        # )

        # self.wait()

        # # Move the whole 3D plot to the right
        # shift_vec = RIGHT * 20
        # axes_group.shift(shift_vec)
        # surface.shift(shift_vec)

        # # rotation_center = axes.c2p(0.5, 0.5, 0.25) + shift_vec
        

        # self.play(Create(axes), Create(surface), run_time=2)

        # # Smooth circular motion (full 360°)
        # self.move_camera(
        #     theta=2 * PI,
        #     frame_center=frame_center,
        #     run_time=2,
        #     rate_func=linear,
        # )

        # self.wait()
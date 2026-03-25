# Add .. to the path to import from the parent directory
import sys
sys.path.append("..")

from templates import MySlide
from settings import IMAGE_COLOR, TEXT_COLOR


from manim import *


class MGFormulasScene(MySlide):
    def construct(self):
        # Begin by defining an axis and the plotting to cluster of points
        axes = Axes(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            x_length=6,
            y_length=6,
            axis_config={"color": GREY},
        )
        # axes.to_edge(LEFT, buff=1.5)
        np.random.seed(42)
        cluster1 = np.random.multivariate_normal(mean=[-2, 0.2], cov=[[1, 1], [0.5, 1]], size=100)
        cluster2 = np.random.multivariate_normal(mean=[2, -0.2], cov=[[1, -1], [-0.5, 1]], size=100)

        dots1 = VGroup(*[
            Dot(axes.c2p(x, y), radius=0.05, color=TEXT_COLOR, fill_opacity=0.5)
            for x, y in cluster1
        ])
        dots2 = VGroup(*[
            Dot(axes.c2p(x, y), radius=0.05, color=IMAGE_COLOR, fill_opacity=0.5)
            for x, y in cluster2
        ])

        self.p.play(Create(axes), run_time=1)
        self.p.play(LaggedStartMap(Create, dots1), LaggedStartMap(Create, dots2), run_time=2)
        self.p.next_slide()

        axes_group = VGroup(axes, dots1, dots2)
        self.p.play(axes_group.animate.to_edge(LEFT, buff=1.5), run_time=1)

        mean_1 = np.mean(cluster1, axis=0)
        mean_1_label = MathTex(r"\bar{\mathbf{t}}")
        mean_1_label.next_to(axes.c2p(*mean_1), UP)
        mean_2 = np.mean(cluster2, axis=0)
        mean_2_label = MathTex(r"\bar{\mathbf{v}}")
        mean_2_label.next_to(axes.c2p(*mean_2), UP)
        mean_dot_1 = Dot(axes.c2p(*mean_1), radius=0.15, color=TEXT_COLOR, fill_opacity=1)
        mean_dot_2 = Dot(axes.c2p(*mean_2), radius=0.15, color=IMAGE_COLOR, fill_opacity=1)

        gap = Line(
            start=axes.c2p(*mean_1),
            end=axes.c2p(*mean_2),
            color=YELLOW,
            buff=0,
        ).set_z_index(-1)
        gap_label = MathTex(r"\vec{\Delta}")
        gap_label.next_to(gap, DOWN)




        # Right column with formulas
        formula_1 = MathTex(r"\bar{\mathbf{t}} = \frac{1}{N} \sum_{i=1}^{N} \mathbf{t}_i",
                            substrings_to_isolate=[r"\bar{\mathbf{t}}", r"\mathbf{t}_i"])
        formula_2 = MathTex(r"\bar{\mathbf{v}} = \frac{1}{N} \sum_{i=1}^{N} \mathbf{v}_i",
                            substrings_to_isolate=[r"\bar{\mathbf{v}}", r"\mathbf{v}_i"])
        formula_3 = MathTex(r"\vec{\Delta} = \bar{\mathbf{t}} - \bar{\mathbf{v}}",
                            substrings_to_isolate=[r"\vec{\Delta}", r"\bar{\mathbf{t}}", r"\bar{\mathbf{v}}"])
        
        formula_1.set_color_by_tex(r"\bar{\mathbf{t}}", TEXT_COLOR)
        formula_1.set_color_by_tex(r"\mathbf{t}_i", TEXT_COLOR)
        formula_2.set_color_by_tex(r"\bar{\mathbf{v}}", IMAGE_COLOR)
        formula_2.set_color_by_tex(r"\mathbf{v}_i", IMAGE_COLOR)
        # formula_3.set_color_by_tex(r"\vec{\Delta}", YELLOW)
        formula_3.set_color_by_tex(r"\bar{\mathbf{t}}", TEXT_COLOR)
        formula_3.set_color_by_tex(r"\bar{\mathbf{v}}", IMAGE_COLOR)


        formulas = VGroup(formula_1, formula_2, formula_3)
        formulas.arrange(DOWN, buff=0.5)
        formulas.to_edge(RIGHT, buff=2)
        formulas.to_edge(UP, buff=1.5)

        self.p.play(Create(mean_dot_1),
                    Create(mean_dot_2),
                    Write(mean_1_label),
                    Write(mean_2_label),
                    Write(formula_1),
                    Write(formula_2))
        # self.p.wait(1)
        self.p.next_slide()
        self.p.play(Create(gap), Write(gap_label), Write(formula_3))
        self.p.next_slide()

        # Remove all the formulas and labels to prepare for the next part
        self.p.play(Uncreate(gap), Uncreate(mean_dot_1), Uncreate(mean_dot_2),
                    Unwrite(mean_1_label), Unwrite(mean_2_label),
                    Unwrite(gap_label),
                    Unwrite(formula_1), Unwrite(formula_2), Unwrite(formula_3))

        # Subdivide the two clusters into 3 subclusters each based on the y-coordinate
        # Random thresholds for varied grouping
        t1_low = -0.5 + np.random.rand() * 0.3
        t1_high = 0.5 + np.random.rand() * 0.3
        t2_low = -0.5 + np.random.rand() * 0.3
        t2_high = 0.5 + np.random.rand() * 0.3
        
        cluster1_subclusters = [cluster1[cluster1[:, 1] < t1_low],
                                cluster1[(cluster1[:, 1] >= t1_low) & (cluster1[:, 1] < t1_high)],
                                cluster1[cluster1[:, 1] >= t1_high]]
        cluster2_subclusters = [cluster2[cluster2[:, 1] < t2_low],
                                cluster2[(cluster2[:, 1] >= t2_low) & (cluster2[:, 1] < t2_high)],
                                cluster2[cluster2[:, 1] >= t2_high]]
        
        # Color the subclusters with clearly separated shades
        # colors1 = [BLUE_E, BLUE_C, BLUE_A]
        # colors2 = [GREEN_E, GREEN_C, GREEN_A]
        colors1 = [TEXT_COLOR, YELLOW, PINK]
        colors2 = [IMAGE_COLOR, ORANGE, PURPLE]
        animations = []
        animations_per_subcluster = [[] for _ in range(3)]
        for (i, (subcluster, color)) in enumerate(zip(cluster1_subclusters, colors1)):
            for x, y in subcluster:
                dot = dots1[cluster1.tolist().index([x, y])]
                animations.append(dot.animate.set_color(color).set_fill(color, opacity=0.3).set_stroke(color, width=1))
                animations_per_subcluster[i].append(Indicate(dot, scale_factor=1.8))

        for (i, (subcluster, color)) in enumerate(zip(cluster2_subclusters, colors2)):
            for x, y in subcluster:
                dot = dots2[cluster2.tolist().index([x, y])]
                animations.append(dot.animate.set_color(color).set_fill(color, opacity=0.3).set_stroke(color, width=1))
                animations_per_subcluster[i].append(Indicate(dot, scale_factor=1.8))

        
        self.p.play(*animations, run_time=1)
        # self.p.wait(1)
        self.p.next_slide()
        # for i in range(3):
        #     self.p.play(*animations_per_subcluster[i], run_time=1)
        #     self.p.wait(0.5)

        # Repeat the same as before (centroid, label and gap) for each pair of the 3 subclusters, but with smaller dots and labels to avoid clutter
        to_be_removed = VGroup()
        gap_lines = VGroup()
        mean_dots_1_sub = VGroup()
        mean_dots_2_sub = VGroup()
        gap_labels_sub = VGroup()
        for i in range(3):
            mean_1_sub = np.mean(cluster1_subclusters[i], axis=0)
            mean_2_sub = np.mean(cluster2_subclusters[i], axis=0)
            mean_dot_1_sub = Dot(axes.c2p(*mean_1_sub), radius=0.1, color=colors1[i], fill_opacity=1, stroke_color=YELLOW, stroke_width=2)
            mean_dot_2_sub = Dot(axes.c2p(*mean_2_sub), radius=0.1, color=colors2[i], fill_opacity=1, stroke_color=YELLOW, stroke_width=2)
            mean_dots_1_sub.add(mean_dot_1_sub)
            mean_dots_2_sub.add(mean_dot_2_sub)

            gap_sub = always_redraw(
                lambda dot1=mean_dot_1_sub, dot2=mean_dot_2_sub: Line(
                    start=dot1.get_center(),
                    end=dot2.get_center(),
                    color=YELLOW,
                    buff=0,
                ).set_z_index(-1)
            )
            gap_label_sub = MathTex(r"\vec{\Delta}_{" + str(i+1) + r"}")
            gap_label_sub.next_to(gap_sub, UP if i == 2 else DOWN, buff=0.1)
            gap_labels_sub.add(gap_label_sub)

            to_be_removed.add(gap_sub, gap_label_sub, mean_dot_1_sub, mean_dot_2_sub)
            gap_lines.add(gap_sub)

            self.p.play(*animations_per_subcluster[i], run_time=1)
            self.p.play(Create(mean_dot_1_sub), Create(mean_dot_2_sub), Create(gap_sub), Write(gap_label_sub))
            self.p.wait(0.5)

        # Write the new formulas for the subclusters
        formula_1_sub = MathTex(r"\bar{\mathbf{t}}^{(c)} = \frac{1}{N^{(c)}} \sum_{j=1}^{N^{(c)}} \mathbf{t}_{i}^{(c)}",
                                substrings_to_isolate=[r"\bar{\mathbf{t}}^{(c)}", r"\mathbf{t}_{i}^{(c)}"])
        formula_2_sub = MathTex(r"\bar{\mathbf{v}}^{(c)} = \frac{1}{N^{(c)}} \sum_{j=1}^{N^{(c)}} \mathbf{v}_{i}^{(c)}",
                                substrings_to_isolate=[r"\bar{\mathbf{v}}^{(c)}", r"\mathbf{v}_{i}^{(c)}"])
        formula_3_sub = MathTex(r"\vec{\Delta}^{(c)} = \bar{\mathbf{t}}^{(c)} - \bar{\mathbf{v}}^{(c)}",
                                substrings_to_isolate=[r"\vec{\Delta}^{(c)}", r"\bar{\mathbf{t}}^{(c)}", r"\bar{\mathbf{v}}^{(c)}"])
        
        formula_1_sub.set_color_by_tex(r"\bar{\mathbf{t}}^{(c)}", TEXT_COLOR)
        formula_1_sub.set_color_by_tex(r"\mathbf{t}_{i}^{(c)}", TEXT_COLOR)
        formula_2_sub.set_color_by_tex(r"\bar{\mathbf{v}}^{(c)}", IMAGE_COLOR)
        formula_2_sub.set_color_by_tex(r"\mathbf{v}_{i}^{(c)}", IMAGE_COLOR)
        # formula_3_sub.set_color_by_tex(r"\vec{\Delta}^{(c)}", YELLOW)
        formula_3_sub.set_color_by_tex(r"\bar{\mathbf{t}}^{(c)}", TEXT_COLOR)
        formula_3_sub.set_color_by_tex(r"\bar{\mathbf{v}}^{(c)}", IMAGE_COLOR)

        formulas_sub = VGroup(formula_1_sub, formula_2_sub, formula_3_sub)
        formulas_sub.arrange(DOWN, buff=0.5)
        formulas_sub.to_edge(RIGHT, buff=1)
        formulas_sub.to_edge(UP, buff=1.5)

        self.p.play(Write(formula_1_sub), Write(formula_2_sub), Write(formula_3_sub))
        self.p.next_slide()

        # Explain what does it mean to apply the gap delta
        self.p.play(Unwrite(formula_1_sub),
                    Unwrite(formula_2_sub),
                    Unwrite(formula_3_sub),
                    gap_lines.animate.set_stroke(color=YELLOW, opacity=0.4),
                    # Uncreate(axes_group),
                    # Uncreate(dots1),
                    # Uncreate(dots2),
                    # Unwrite(to_be_removed),
                    run_time=1)
        # you basically apply alpha/2 delta to the image and -alpha/2 delta to the text, so you move the two clusters closer by a factor of alpha, without changing their internal structure

        shift_formula_1 = MathTex(r"\mathbf{t}_{i}^{(c)} \rightarrow \mathbf{t}_{i}^{(c)} - \frac{\alpha}{2} \vec{\Delta}^{(c)}",
                        substrings_to_isolate=[r"\mathbf{t}_{i}^{(c)}", r"\frac{\alpha}{2} \vec{\Delta}^{(c)}"])
        shift_formula_2 = MathTex(r"\mathbf{v}_{i}^{(c)} \rightarrow \mathbf{v}_{i}^{(c)} + \frac{\alpha}{2} \vec{\Delta}^{(c)}",
                        substrings_to_isolate=[r"\mathbf{v}_{i}^{(c)}", r"\frac{\alpha}{2} \vec{\Delta}^{(c)}"])
        
        shift_formula_1.set_color_by_tex(r"\mathbf{t}_{i}^{(c)}", TEXT_COLOR)
        # shift_formula_1.set_color_by_tex(r"\vec{\Delta}^{(c)}", YELLOW)
        shift_formula_2.set_color_by_tex(r"\mathbf{v}_{i}^{(c)}", IMAGE_COLOR)
        # shift_formula_2.set_color_by_tex(r"\vec{\Delta}^{(c)}", YELLOW)

        shift_formulas = VGroup(shift_formula_2, shift_formula_1)
        shift_formulas.arrange(DOWN, buff=0.5)
        shift_formulas.move_to(ORIGIN)
        shift_formulas.to_edge(RIGHT, buff=1)

        # shift_formulas.to_edge(UP, buff=1.5)
        self.p.play(Write(shift_formula_1), Write(shift_formula_2))
        self.p.next_slide()


        # Do the following:
        # Show, for each subcluster, a small arrow from the center showing the direction of the shift
        # Apply the shift to the subclusters by animating the dots moving according to the formulas, so the text cluster moves towards the image cluster and the image cluster moves towards the text cluster, effectively reducing the gap by a factor of alpha

        gap_arrows_1 = VGroup()
        gap_arrows_2 = VGroup()
        rectangles_arrows = VGroup()
        for i in range(3):
            mean_1_sub = np.mean(cluster1_subclusters[i], axis=0)
            mean_2_sub = np.mean(cluster2_subclusters[i], axis=0)
            gap_arrow_1 = Arrow(
                start=axes.c2p(*np.mean(cluster1_subclusters[i], axis=0)),
                end=axes.c2p(*np.mean(cluster1_subclusters[i], axis=0) - 0.3 * (mean_1_sub - mean_2_sub)),
                color=YELLOW,
                buff=0,
            ).set_z_index(-1)
            gap_arrow_2 = Arrow(
                start=axes.c2p(*np.mean(cluster2_subclusters[i], axis=0)),
                end=axes.c2p(*np.mean(cluster2_subclusters[i], axis=0) + 0.3 * (mean_1_sub - mean_2_sub)),
                color=YELLOW,
                buff=0,
            ).set_z_index(-1)
            gap_arrows_1.add(gap_arrow_1)
            gap_arrows_2.add(gap_arrow_2)

            if i == 0:
                rectangle_arrow1 = SurroundingRectangle(gap_arrow_1, color=YELLOW, buff=0.1)
                rectangle_arrow2 = SurroundingRectangle(gap_arrow_2, color=PURPLE, buff=0.1)

                rectangles_arrows.add(rectangle_arrow1, rectangle_arrow2)

                rectangle_formula_1 = SurroundingRectangle(shift_formula_1.get_part_by_tex(r"\frac{\alpha}{2} \vec{\Delta}^{(c)}"), color=PURPLE, buff=0.1)
                rectangle_formula_2 = SurroundingRectangle(shift_formula_2.get_part_by_tex(r"\frac{\alpha}{2} \vec{\Delta}^{(c)}"), color=YELLOW, buff=0.1)

                self.p.play(Create(gap_arrow_1), Create(gap_arrow_2))
                self.p.play(Create(rectangle_arrow1), Create(rectangle_formula_2))
                self.p.play(Create(rectangle_arrow2), Create(rectangle_formula_1))
            else:
                rectangle_arrow1 = SurroundingRectangle(gap_arrow_1, color=YELLOW, buff=0.1)
                rectangle_arrow2 = SurroundingRectangle(gap_arrow_2, color=PURPLE, buff=0.1)

                rectangles_arrows.add(rectangle_arrow1, rectangle_arrow2)

                self.p.play(Create(gap_arrow_1), Create(gap_arrow_2), Create(rectangle_arrow1), Create(rectangle_arrow2))

        # Animate the shift of the dots according to the formulas
        shift_animations = []
        alpha = 0.4
        for i in range(3):
            delta = np.mean(cluster1_subclusters[i], axis=0) - np.mean(cluster2_subclusters[i], axis=0)
            shift_vec = np.array([delta[0], delta[1], 0.0])
            for x, y in cluster1_subclusters[i]:
                dot = dots1[cluster1.tolist().index([x, y])]
                shift_animations.append(dot.animate.shift(-0.5 * alpha * shift_vec))
            for x, y in cluster2_subclusters[i]:
                dot = dots2[cluster2.tolist().index([x, y])]
                shift_animations.append(dot.animate.shift(0.5 * alpha * shift_vec))

            # Also animate the centroids
            shift_animations.append(mean_dots_1_sub[i].animate.shift(-0.5 * alpha * shift_vec))
            shift_animations.append(mean_dots_2_sub[i].animate.shift(0.5 * alpha * shift_vec))

            # if i == 0:
            #     rectangle_arrow1 = SurroundingRectangle(gap_arrows_1[0], color=YELLOW, buff=0.1)
            #     rectangle_arrow2 = SurroundingRectangle(gap_arrows_2[0], color=YELLOW, buff=0.1)

            #     rectangle_formula_1 = SurroundingRectangle(shift_formula_1.get_part_by_tex(r"\frac{\alpha}{2} \vec{\Delta}^{(c)}"), color=YELLOW, buff=0.1)
            #     rectangle_formula_2 = SurroundingRectangle(shift_formula_2.get_part_by_tex(r"\frac{\alpha}{2} \vec{\Delta}^{(c)}"), color=YELLOW, buff=0.1)


            #     self.p.play(*shift_animations, run_time=2)
            #     shift_animations = []

        # In the shift animations also add an animation to move the centroid dots
        # Remove the surrounding rectangles and remove the arrows

        shift_animations += [FadeOut(gap_arrows_1), FadeOut(gap_arrows_2)]
        shift_animations += [FadeOut(VGroup(rectangles_arrows, rectangle_formula_1, rectangle_formula_2))]
        shift_animations += [FadeOut(gap_labels_sub)]

        self.p.play(*shift_animations, run_time=2)

        self.p.next_slide()

        # Remove everything
        self.p.play(
            Uncreate(axes_group),
            Uncreate(dots1),
            Uncreate(dots2),
            Unwrite(to_be_removed),
            Unwrite(formulas_sub),
            Unwrite(shift_formulas),
        )
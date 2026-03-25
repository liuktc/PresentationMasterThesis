# Add .. to the path to import from the parent directory
import sys
sys.path.append("..")

from templates import MySlide
from settings import IMAGE_COLOR, TEXT_COLOR


from manim import *

from .clip import get_trapezoid


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

# def get_custom_table(data: list[list[VMobject]], **kwargs):
#     # Arrange items in grid and add just a line between header and body (horizontal line)
#     # and just a single line between columns (vertical line)
#     num_cols = len(data[0])
#     print(num_cols)

#     group = VGroup(*[cell for row in data for cell in row])
#     group.arrange_in_grid(cols=num_cols, buff=(.5, .3), **kwargs)

#     # return group

#     # Draw line between header and body
#     header_line = Line(
#         start=data[0][0].get_bottom() + DOWN * 0.1 + LEFT * 0.3,
#         end=data[0][1].get_bottom() + DOWN * 0.1 - RIGHT * 0.3,
#         color=WHITE,
#         stroke_width=2,
#     )

#     # Draw line between columns
#     # column_line = Line(
#     #     start=data[0][0].get_left() + RIGHT * 0.1 +

#     #     end=data[1][0].get_left() + RIGHT * 0.1,
#     #     color=WHITE,
#     #     stroke_width=2,
#     # )

#     for i in range(1, num_cols):
#         column_line = Line(
#             start=data[0][i].get_left() + RIGHT * 0.1,
#             end=data[-1][i].get_left() + RIGHT * 0.1,
#             color=WHITE,
#             stroke_width=2,
#         )
#         group.add(column_line)
#     return VGroup(group, header_line, column_line)


# def create_minimal_table(col1_data, col2_data, header=["Column A", "Column B"]):
#     # 1. Create the text elements
#     header_tex = VGroup(Tex(header[0], font_size=24), Tex(header[1], font_size=24))
#     col1 = VGroup(*[Tex(str(i), font_size=24) for i in col1_data])
#     col2 = VGroup(*[Tex(str(i), font_size=24) for i in col2_data])

#     # 2. Arrange the columns
#     col1.arrange(DOWN, buff=0.5)
#     col2.arrange(DOWN, buff=0.5)
    
#     # Position columns side-by-side
#     columns = VGroup(col1, col2).arrange(RIGHT, buff=1)
    
#     # Position headers above columns
#     header_tex[0].next_to(col1, UP, buff=0.6)
#     header_tex[1].next_to(col2, UP, buff=0.6)

#     # 3. Create the lines
#     # Horizontal line between header and body
#     h_line = Line(
#         start=header_tex.get_left() + LEFT*0, 
#         end=header_tex.get_right() + RIGHT*0
#     ).next_to(header_tex, DOWN, buff=0.3)

#     # Vertical line between columns
#     x_coord = (col1.get_right()[0] + col2.get_left()[0]) / 2
    
#     v_line = Line(
#         start=[x_coord, header_tex.get_top()[1] + 0, 0],
#         end=[x_coord, columns.get_bottom()[1] - 0, 0],
#         stroke_width=2
#     )

#     return VGroup(header_tex, columns, h_line, v_line)

class CustomTable(Table):
    def _add_horizontal_lines(self) -> Table:
        """Adds the horizontal lines to the table."""
        anchor_left = self.get_left()[0] - 0.5 * self.h_buff
        anchor_right = self.get_right()[0] + 0.5 * self.h_buff
        line_group = VGroup()
        if self.include_outer_lines:
            anchor = self.get_rows()[0].get_top()[1] + 0.5 * self.v_buff
            line = Line(
                [anchor_left, anchor, 0], [anchor_right, anchor, 0], **self.line_config
            )
            line_group.add(line)
            self.add(line)
            anchor = self.get_rows()[-1].get_bottom()[1] - 0.5 * self.v_buff
            line = Line(
                [anchor_left, anchor, 0], [anchor_right, anchor, 0], **self.line_config
            )
            line_group.add(line)
            self.add(line)
        for k in range(1):
            anchor = self.get_rows()[k + 1].get_top()[1] + 0.5 * (
                self.get_rows()[k].get_bottom()[1] - self.get_rows()[k + 1].get_top()[1]
            )
            line = Line(
                [anchor_left, anchor, 0], [anchor_right, anchor, 0], **self.line_config
            )
            line_group.add(line)
            self.add(line)
        self.horizontal_lines = line_group
        return self


def get_L_shaped_arrow(start_point, end_point, color=WHITE, **kwargs):
    mid_point = np.array([start_point[0], end_point[1], 0])
    return VGroup(
        Line(start_point, mid_point, color=color, **kwargs),
        Arrow(mid_point, end_point, color=color, **kwargs)
    )

class EncodersScene(MySlide):
    def construct(self):
        # Classical image classification networks (like ResNets or VGG) are designed to classify images
        # into a fixed set of categories
        # Take a complex image example for example a dog on a beach with a ball, and show how it would be classified by a ResNet
        # (e.g. as "dog" or "ball" or "beach") -> By just using a single label, we are missing important information
        # about the image, such as the presence of multiple objects, their relationships, and the overall context.
        np.random.seed(0)

        input_image = ImageMobject("cat.png").scale_to_fit_height(1.5)
        input_image.to_edge(LEFT, buff=0.3)
        input_image_background = SurroundingRectangle(input_image, color=IMAGE_COLOR, buff=0.1)

        input_label = Tex(r"Class: \texttt{cat}", font_size=36)
        input_label.next_to(input_image, DOWN, buff=0.5)

        self.p.play(Create(input_image_background), FadeIn(input_image), Write(input_label))


        image_encoder = get_trapezoid(r"Image\\Encoder", color=IMAGE_COLOR)
        image_encoder.next_to(input_image, RIGHT, buff=0.7)

        arrow_input_to_encoder = Arrow(start=input_image.get_right(), end=image_encoder.get_left(), buff=0.1, color=WHITE)

        image_embedding = MathTex(r"[0.25, -0.1, \dots, 0.04]", font_size=24)
        image_embedding.next_to(image_encoder, RIGHT, buff=0.7)
        image_embedding_bracket = Brace(image_embedding,UP)
        image_embedding_bracket_label = MathTex(r"\mathbf{v}_i", r"\in \mathbb{R}^d", font_size=36)
        image_embedding_bracket_label.set_color_by_tex(r"\mathbf{v}_i", IMAGE_COLOR)
        image_embedding_bracket_label.next_to(image_embedding_bracket, UP, buff=0.1)

        arrow_encoder_output = Arrow(start=image_encoder.get_right(), end=image_embedding.get_left(), buff=0.1, color=WHITE)
        image_embedding_group = VGroup(image_embedding, image_embedding_bracket, image_embedding_bracket_label)
        # clip_image_output_group = VGroup(image_embedding, arrow_encoder_output, image_embedding_bracket, image_embedding_bracket_label)

        # self.p.play(Write(image_encoder), Write(arrow_input_to_encoder), Write(image_embedding), Create(arrow_encoder_output))
        

        linear_classifier = Tex(r"Linear Classifier\\$y = W\mathbf{v}_i + b$", font_size=24, color=WHITE)
        linear_classifier_background = SurroundingRectangle(linear_classifier, color=BLUE, buff=0.2, fill_color=BLUE, fill_opacity=0.1)
        linear_classifier = VGroup(linear_classifier, linear_classifier_background)

        linear_classifier.next_to(image_embedding, RIGHT, buff=0.7)
        arrow_embedding_to_classifier = Arrow(start=image_embedding.get_right(), end=linear_classifier.get_left(), buff=0.1, color=WHITE)


        image_classifier = SurroundingRectangle(Group(image_encoder, linear_classifier), buff=0.4, corner_radius=0.3, fill_opacity=0.1, color=GRAY)
        # Make sure that image_classifier is behind the other elements
        image_classifier.set_z_index(-1)
        image_classifier_label = Tex(r"Image Classifier", font_size=36, color=WHITE)
        image_classifier_label.next_to(image_classifier, UP, buff=0.2)

        image_classifier_group = VGroup(image_classifier, image_classifier_label, image_encoder, arrow_embedding_to_classifier, linear_classifier, arrow_encoder_output, image_embedding_group)

        self.p.play(Write(image_classifier), Write(image_classifier_label))
        self.p.play(Write(image_encoder), Write(arrow_input_to_encoder))
        self.p.play(Write(image_embedding_group), Create(arrow_encoder_output))
        self.p.play(Write(linear_classifier), Write(arrow_embedding_to_classifier))

        output = CustomTable(
            [
                [r"\textbf{Class}", r"\textbf{Probability}"],
                [r"\texttt{cat}", "$0.65$"],
                [r"\texttt{dinosaur}", "$0.18$"],
                [r"\texttt{chair}", "$0.07$"],
                [r"\texttt{sunglasses}", "$0.05$"],
                [r"\texttt{sunrise}", "$0.05$"],
                [r"$\vdots$", r"$\vdots$"],
            ],
            include_outer_lines=False,
            h_buff=0.5,
            v_buff=0.3,
            element_to_mobject=lambda x: Tex(x, font_size=24)
        )

        output.get_rows()[0][0].set_y(output.get_rows()[0][1].get_y())
        # Make the header row bold and bigger
        for cell in output.get_rows()[0]:
            cell.set_font_size(28)

        output.next_to(linear_classifier, RIGHT, buff=0.7)
        arrow_classifier_to_output = Arrow(start=linear_classifier.get_right(), end=output.get_left(), buff=0.1, color=WHITE)
        self.p.play(Write(output), Write(arrow_classifier_to_output))

        self.p.next_slide()

        self.p.play(image_classifier_group.animate.scale(0.7).to_edge(LEFT, buff=0.3).to_edge(UP, buff=1),
                    FadeOut(input_label),
                    FadeOut(input_image),
                    FadeOut(input_image_background),
                    FadeOut(arrow_input_to_encoder),
                    FadeOut(arrow_classifier_to_output),
                    FadeOut(output))
        # The image classifier is trained as you can see
        # For this reason, images of the same class (e.g. "dog") will tend to cluster together in the embedding space
        # This is very useful for other task, such as retrieval, where we want to find images that are similar to a query image

        # What if we want to find an image given a text query?
        # To perform this, CLIP has been introduced.


        embedding_space = Axes(
            x_range=[-1, 1, 0.5],
            y_range=[-1, 1, 0.5],
            x_length=4,
            y_length=4,
            tips=False,
                )
        
        # Create 3 different clusters
        COLORS = [RED, GREEN, BLUE]
        cluster_1 = np.random.randn(50, 2) * 0.2 + np.array([0, 0.5])
        cluster_2 = np.random.randn(50, 2) * 0.2 + np.array([-0.5, -0.5])
        cluster_3 = np.random.randn(50, 2) * 0.2 + np.array([0.5, -0.5])


        cluster_1_points = [Dot(point=[embedding_space.c2p(x,y)], color=COLORS[0], fill_opacity=0.7) for x, y in cluster_1]
        cluster_2_points = [Dot(point=[embedding_space.c2p(x,y)], color=COLORS[1], fill_opacity=0.7) for x, y in cluster_2]
        cluster_3_points = [Dot(point=[embedding_space.c2p(x,y)], color=COLORS[2], fill_opacity=0.7) for x, y in cluster_3]

        line_from_embedding_to_space = get_L_shaped_arrow(image_embedding_group.get_bottom() + 0.2 * DOWN, embedding_space.get_left() + 0.2 * LEFT, buff=0)

        self.p.play(Create(embedding_space), Create(line_from_embedding_to_space))
        # return
        self.p.play(LaggedStartMap(Create, VGroup(*cluster_1_points), lag_ratio=0.05),
                    LaggedStartMap(Create, VGroup(*cluster_2_points), lag_ratio=0.05),
                    LaggedStartMap(Create, VGroup(*cluster_3_points), lag_ratio=0.05))


        cluster_1_example_image = ImageMobject("cat.png").scale_to_fit_height(1.5)
        cluster_1_example_image.next_to(cluster_1_points[0], UP, buff=0.5)
        # cluster_1_arrow = Arrow(start=cluster_1_points[0], end=cluster_1_example_image.get_bottom(), buff=0.1, color=WHITE)
        # self.p.play(FadeIn(cluster_1_example_image), Write(cluster_1_arrow))

        cluster_2_example_image = ImageMobject("concept_cow.png").scale_to_fit_height(1.5)
        cluster_2_example_image.next_to(cluster_2_points[0], LEFT, buff=0.5)
        # cluster_2_arrow = Arrow(start=cluster_2_points[0], end=cluster_2_example_image.get_right(), buff=0.1, color=WHITE)

        INDEX = 10
        cluster_3_example_image = ImageMobject("dog.png").scale_to_fit_height(1.5)
        cluster_3_example_image.next_to(cluster_3_points[INDEX], RIGHT, buff=0.5)
        # cluster_3_arrow = Arrow(start=cluster_3_points[0], end=cluster_3_example_image.get_left(), buff=0.1, color=WHITE)

        # cluster_1_points[0]

        selected_points = [cluster_1_points[0], cluster_2_points[0], cluster_3_points[INDEX]]
        for point in selected_points:
            point.set_z_index(10)
        self.p.bring_to_front(*selected_points)

        self.p.play(FadeIn(cluster_1_example_image), 
                    FadeIn(cluster_2_example_image),
                    FadeIn(cluster_3_example_image),
                    cluster_1_points[0].animate.set_stroke(WHITE, width=0.1).set_fill(YELLOW, opacity=1.0).scale(1.5),
                    cluster_2_points[0].animate.set_stroke(WHITE, width=0.1).set_fill(YELLOW, opacity=1.0).scale(1.5),
                    cluster_3_points[INDEX].animate.set_stroke(WHITE, width=0.1).set_fill(YELLOW, opacity=1.0).scale(1.5))

        self.p.next_slide()

        self.p.play(FadeOut(cluster_1_example_image),
                    FadeOut(cluster_2_example_image),
                    FadeOut(cluster_3_example_image),
                    cluster_1_points[0].animate.set_stroke(None).set_fill(COLORS[0], opacity=0.7).scale(1/1.5),
                    cluster_2_points[0].animate.set_stroke(None).set_fill(COLORS[1], opacity=0.7).scale(1/1.5),
                    cluster_3_points[INDEX].animate.set_stroke(None).set_fill(COLORS[2], opacity=0.7).scale(1/1.5))
        

        example_point = cluster_3_points[INDEX]
        top_3_closest_points = sorted(
            [point for i, point in enumerate(cluster_3_points) if i != INDEX],
            key=lambda point: np.linalg.norm(point.get_center() - example_point.get_center()),
        )[:3]

        example_image = ImageMobject("dog.png").scale_to_fit_height(1.5)
        example_image.next_to(example_point, UP + LEFT, buff=0.5)

        example_point.set_z_index(10)
        self.p.bring_to_front(example_point)
        self.p.play(FadeIn(example_image),
                    example_point.animate.set_stroke(WHITE, width=0.1).set_fill(YELLOW, opacity=1.0).scale(1.5))
        
        for point in top_3_closest_points:
            point.set_z_index(10)
        self.p.bring_to_front(*top_3_closest_points)
        self.p.play(*[p.animate.set_stroke(WHITE, width=0.1).set_fill(YELLOW, opacity=1.0).scale(1.5) for p in top_3_closest_points])
                    


        example_images = Group(*[
                        # Tex("Retrieved Images"),
                        ImageMobject("dog_1.jpg").scale_to_fit_height(1.5),
                        ImageMobject("dog_2.jpg").scale_to_fit_height(1.5),
                        ImageMobject("dog_3.jpg").scale_to_fit_height(1.5)])
        
        example_images.arrange(DOWN, buff=0.3)
        example_images.next_to(embedding_space, RIGHT, buff=0.5)
        # example_images.shift(DOWN)
        example_images.to_edge(DOWN, buff=1)

        example_images_label = Tex("Retrieved Images", font_size=28)
        example_images_label.next_to(example_images, UP, buff=0.3)
        arrows = [Arrow(start=p.get_center(), end=example_images[i].get_left(), buff=0.1, color=WHITE) for i, p in enumerate(top_3_closest_points)]

        self.p.play(
            LaggedStart(*[FadeIn(image) for image in example_images], lag_ratio=0.2),
            LaggedStart(*[Create(arrow) for arrow in arrows], lag_ratio=0.2),
            Write(example_images_label)
        )

        self.p.next_slide()

        # Remove everything
        self.p.play(
            Uncreate(embedding_space),
            Uncreate(line_from_embedding_to_space),
            *[Uncreate(point) for point in cluster_1_points],
            *[Uncreate(point) for point in cluster_2_points],
            *[Uncreate(point) for point in cluster_3_points],
            FadeOut(example_image),
            FadeOut(example_images),
            FadeOut(example_images_label),
            *[Uncreate(arrow) for arrow in arrows],
            *[Unwrite(mob) for mob in image_classifier_group]
        )

        
        
        
        













        # Classical image classifiers works as follows: they take as input an image and a label (in our case ....),
        # The image is passed to an image encoder (usually a convolutional neural network) that produces a 
        # fixed lenght vector representation of the image (called embedding). 
        # This embedding is then passed to a linear classifier that produces a probability distribution over the possible classes (e.g. "dog", "ball", "cat", etc.)
        # However, this approach has a major limitation: it can only assign a single label to the image,
        # which means that it cannot capture the rich and complex information contained in the image, such as
        # the presence of multiple objects, their relationships, and the overall context.
        # To fix this problem, researchers have developed 


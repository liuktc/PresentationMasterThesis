# Add .. to the path to import from the parent directory
import sys
sys.path.append("..")

from templates import MySlide


from manim import *

# my_tex_template = TexTemplate()
# my_tex_template.add_to_preamble(r"\usepackage{ragged2e}")

TRAPEZOID_WIDTH = 1
TRAPEZOID_HEIGHT = 1
TRAPEZOID_SKEW = .25

def get_trapezoid(text="Image Encoder", color=BLUE):
    points = [
        [-TRAPEZOID_WIDTH / 2, -TRAPEZOID_HEIGHT / 2, 0],
        [TRAPEZOID_WIDTH / 2, -TRAPEZOID_HEIGHT / 2, 0],
        [TRAPEZOID_WIDTH / 2 + TRAPEZOID_SKEW, TRAPEZOID_HEIGHT / 2, 0],
        [-TRAPEZOID_WIDTH / 2 - TRAPEZOID_SKEW, TRAPEZOID_HEIGHT / 2, 0],
    ]
    polygon = Polygon(*points)
    # Rotate the trapezoid by 90 degrees to make it vertical
    polygon.rotate(PI / 2, axis=OUT)
    polygon.set_fill(color, opacity=0.5)
    polygon.set_stroke(color, width=2)

    text_mobject = Tex(text, font_size=24)
    text_mobject.move_to(polygon.get_center())
    text_mobject.scale_to_fit_width(TRAPEZOID_WIDTH * 0.8)
    # Give the trapezoid a reference to the text for simpler animations later
    polygon.text = text_mobject
    polygon.add(text_mobject)
    return polygon


def fed_pair_to_encoders(scene,
                         image_encoder,
                         text_encoder,
                         input_pair:InputPair,
                         axes,
                         ):
    image_mobject = ImageMobject(input_pair.image_path)
    text_mobject = Tex(input_pair.text, font_size=24)

    image_mobject.scale_to_fit_width(1.5)
    text_mobject.scale_to_fit_width(1.5)
    # Add a colored border to the image and text mobjects to indicate which encoder they belong to
    image_border = SurroundingRectangle(image_mobject, color=GREEN, buff=0.1)
    text_border = SurroundingRectangle(text_mobject, color=BLUE, buff=0.1)

    # Group the image and text mobjects with their respective borders
    image_group = Group(image_mobject, image_border)
    text_group = VGroup(text_mobject, text_border)

    image_group.next_to(image_encoder, LEFT, buff=1)
    text_group.next_to(text_encoder, LEFT, buff=1)

    # scene.add(image_group, text_group)
    scene.play(FadeIn(image_group), Create(text_group), run_time=0.3)
    scene.wait(0.3)

    # Animate moving into the encoders with a "swallow" effect
    scene.play(
        image_group.animate.move_to(image_encoder.get_center()).scale(0.2),
        text_group.animate.move_to(text_encoder.get_center()).scale(0.2),
        # Visual feedback on encoders
        image_encoder.animate.scale(1.1).set_fill(opacity=0.8),
        text_encoder.animate.scale(1.1).set_fill(opacity=0.8),
        run_time=0.5,
    )

    # image_group[0].remove()
    # Remove the image from the image group
    # image_group.remove(image_mobject)
    # Pulse back
    scene.play(
        image_encoder.animate.scale(1/1.1).set_fill(opacity=0.5),
        text_encoder.animate.scale(1/1.1).set_fill(opacity=0.5),
        run_time=0.5
    )

    # Morph the image and text groups into points in the shared embedding space
    image_embedding_point = Dot(axes.c2p(input_pair.image_embedding[0], input_pair.image_embedding[1]), color=GREEN)
    text_embedding_point = Dot(axes.c2p(input_pair.text_embedding[0], input_pair.text_embedding[1]), color=BLUE)
    line_connecting_points = Line(image_embedding_point.get_center(), text_embedding_point.get_center(), color=YELLOW)

    scene.play(
        image_group.animate.next_to(image_embedding_point, input_pair.image_direction, buff=0.5).scale(3),
        text_group.animate.next_to(text_embedding_point, input_pair.text_direction, buff=0.5).scale(3),
        Create(image_embedding_point), Create(text_embedding_point),
        Create(line_connecting_points),
        run_time=0.5,
    )

    # Return all the created objects
    to_return = [image_group, text_group, image_embedding_point, text_embedding_point, line_connecting_points]
    return to_return

    # image_embedding_point.add(image_group)
    # text_embedding_point.add(text_group)

    
    # scene.play(
    #     ReplacementTransform(image_group, image_embedding_point),
    #     ReplacementTransform(text_group, text_embedding_point),
    #     run_time=1.0,
    # )

class InputPair():
    def __init__(self, image_path, text, image_embedding, text_embedding, image_direction=UP, text_direction=UP):
        self.image_path = image_path
        self.text = text
        self.image_embedding = image_embedding
        self.text_embedding = text_embedding
        self.image_direction = image_direction
        self.text_direction = text_direction


class ClipScene(MySlide):
    def construct(self):
        image_encoder = get_trapezoid(text=r"Image\\Encoder", color=GREEN)
        text_encoder = get_trapezoid(text=r"Text\\Encoder", color=BLUE)
        text_encoder.next_to(image_encoder, DOWN, buff=.5)


        encoders = VGroup(image_encoder, text_encoder)
        encoders_background = SurroundingRectangle(encoders, color=GREY, fill_opacity=0.1, buff=0.3, corner_radius=0.5)
        encoders_background_label = Tex("CLIP")
        encoders_background_label.next_to(encoders_background, UP)
        encoders = VGroup(encoders_background, encoders_background_label, encoders)
        encoders.move_to(ORIGIN).scale(1)
        # encoders.to_edge(LEFT, buff=3)

        # clip_formula = MathTex(r"\mathcal{L} = - \frac{1}{N} \sum_{i=1}^{N} \log \frac{\exp(\mathrm{sim}(\mathbf{v}_i, \mathbf{t}_i)/\tau)}{\sum_{j=1}^{N} \exp(\mathrm{sim}(\mathbf{v}_i, \mathbf{t}_j)/\tau)}",
        #                        font_size=24,
        #                        substrings_to_isolate=[r"\mathbf{v}_i", r"\mathbf{t}_i", r"\mathbf{t}_j"])
        
        # clip_formula.set_color_by_tex(r"\mathbf{v}_i", GREEN)
        # clip_formula.set_color_by_tex(r"\mathbf{t}_i", BLUE)
        # clip_formula.set_color_by_tex(r"\mathbf{t}_j", BLUE)

        clip_image = ImageMobject("cat.png").scale_to_fit_width(1.5)
        clip_image_background = SurroundingRectangle(clip_image, color=GREEN, buff=0.1)
        clip_image_input_group = Group(clip_image, clip_image_background)
        clip_image_input_group.next_to(image_encoder, LEFT, buff=1)

        clip_text = Tex(r"\texttt{A cute cat}", font_size=24)
        clip_text_background = SurroundingRectangle(clip_text, color=BLUE, buff=0.1)
        clip_text_input_group = VGroup(clip_text, clip_text_background)
        clip_text_input_group.next_to(text_encoder, LEFT, buff=1)

        clip_text_arrow = Arrow(start=clip_text_input_group.get_right(), end=text_encoder.get_left(), buff=0.1, color=WHITE)
        clip_text_input_group.add(clip_text_arrow)
        clip_image_arrow = Arrow(start=clip_image_input_group.get_right(), end=image_encoder.get_left(), buff=0.1, color=WHITE)
        clip_image_input_group.add(clip_image_arrow)

        clip_image_output = MathTex(r"[0.25, -0.1, \dots, 0.04]", font_size=36)
        clip_image_output.next_to(image_encoder, RIGHT, buff=1)
        clip_image_output_bracket = Brace(clip_image_output,UP)
        clip_image_output_bracket_label = MathTex(r"\mathbf{v}_i", r"\in \mathbb{R}^d")
        clip_image_output_bracket_label.set_color_by_tex(r"\mathbf{v}_i", GREEN)
        clip_image_output_bracket_label.next_to(clip_image_output_bracket, UP, buff=0.1)
        clip_image_arrow_output = Arrow(start=image_encoder.get_right(), end=clip_image_output.get_left(), buff=0.1, color=WHITE)
        clip_image_output_group = VGroup(clip_image_output, clip_image_arrow_output, clip_image_output_bracket, clip_image_output_bracket_label)

        clip_text_output = MathTex(r"[0.21, -0.12, \dots, 0.05]", font_size=36)
        clip_text_output.next_to(text_encoder, RIGHT, buff=1)
        clip_text_output_bracket = Brace(clip_text_output,UP)
        clip_text_output_bracket_label = MathTex(r"\mathbf{t}_i", r"\in \mathbb{R}^d")
        clip_text_output_bracket_label.set_color_by_tex(r"\mathbf{t}_i", BLUE)
        clip_text_output_bracket_label.next_to(clip_text_output_bracket, UP, buff=0.1)
        clip_text_arrow_output = Arrow(start=text_encoder.get_right(), end=clip_text_output.get_left(), buff=0.1, color=WHITE)
        clip_text_output_group = VGroup(clip_text_output, clip_text_arrow_output, clip_text_output_bracket, clip_text_output_bracket_label)

        # clip_formula.next_to(encoders, DOWN, buff=0.2)
        #clip_formula.to_edge(DOWN, buff=0.15)
        # self.p.play(Write(image_encoder))
        # self.p.play(Write(text_encoder))
        self.p.play(Write(encoders), FadeIn(clip_image_input_group), Write(clip_text_input_group))
        self.p.next_slide()
        self.p.play(Write(clip_image_output_group), Write(clip_text_output_group))
        self.p.next_slide()
        # self.p.play(Write(clip_formula))
        # self.p.next_slide()
        

        self.p.play(encoders.animate.to_edge(LEFT, buff=3).scale(1/1),
                    FadeOut(clip_image_input_group), Unwrite(clip_text_input_group),
                    Unwrite(clip_image_output_group), Unwrite(clip_text_output_group))
        

        # Add an axis to represent the shared embedding space
        embedding_space = Axes(x_range=[-1, 1, .25], y_range=[-1, 1, .25], x_length=4, y_length=4)
        # embedding_space.add_coordinates()
        embedding_space.to_edge(RIGHT, buff=3)
        self.p.play(Create(embedding_space))

        # return




        # Load example image and text
        TO_SPAWN = [
            InputPair("cat.png", r"\texttt{A cute cat}", (0.6, 0.5), (0.65, 0.48), image_direction=UP, text_direction=RIGHT),
            InputPair("dog.png", r"\texttt{A funny dog}", (-0.2, 0.4), (-0.3, 0.42), image_direction=UP, text_direction=LEFT),
            InputPair("adamo.jpg", r"\texttt{Consciousness}", (0.5, -0.4), (0.55, -0.42), image_direction=DOWN, text_direction=RIGHT),
            InputPair("falling-apple.jpg", r"\texttt{Discovery}", (-0.5, -0.5), (-0.55, -0.48), image_direction=DOWN, text_direction=LEFT),
        ]


        spawned = Group()
        for pair in TO_SPAWN:
            res = fed_pair_to_encoders(self.p, image_encoder, text_encoder, pair, embedding_space)
            spawned.add(*res)
            # lines.add(res[-1])
        # return 
        self.p.next_slide()

        # Draw a cross on top of the axis to indicate that this is not what happens
        cross = Cross(embedding_space, color=RED, stroke_width=10)
        spawned.add(cross)
        self.p.play(Create(cross))

        # Unfade both cross and points in embedding space
        self.p.play(FadeOut(spawned))

        TO_SPAWN_GAP = [
            InputPair("cat.png", r"\texttt{A cute cat}", (-0.6, 0.5), (0.45, 0.55), image_direction=UP + LEFT * 0.5, text_direction=RIGHT + UP * 0.5),
            InputPair("dog.png", r"\texttt{A funny dog}", (-0.63, 0.2), (0.6, 0.3), image_direction=LEFT, text_direction=RIGHT),
            InputPair("adamo.jpg", r"\texttt{Consciousness}", (-0.5, -0.2), (0.4, -0.3), image_direction=LEFT, text_direction=RIGHT),
            InputPair("falling-apple.jpg", r"\texttt{Discovery}", (-0.55, -0.5), (0.35, -0.45), image_direction=DOWN + LEFT * 0.5, text_direction=RIGHT + DOWN* 0.5),
        ]

        lines = Group()
        spawned_pairs = []
        for pair in TO_SPAWN_GAP:
            res = fed_pair_to_encoders(self.p, image_encoder, text_encoder, pair, embedding_space)
            spawned.add(*res)
            lines.add(res[-1])
            spawned_pairs.append(res)

        self.p.next_slide()

        # Play a loop animation highlighting the lines connecting the image and text embeddings
        self.p.play(
            Wiggle(lines)
        )

        text = Tex("Modality Gap", color=YELLOW)
        text.next_to(embedding_space, UP, buff=0.5)

        lines_copy = lines.copy()

        # Clone the lines and merge them to create the text "Modality Gap" with the lines as the strokes of the letters
        self.p.play(ReplacementTransform(lines_copy, text), run_time=1.5)
        self.p.next_slide()


        movement_animations = []
        line_animations = []
        to_delete = []
        for idx, pair_objects in enumerate(spawned_pairs):
            image_group = pair_objects[0]
            text_group = pair_objects[1]
            image_point = pair_objects[2]
            text_point = pair_objects[3]
            line = pair_objects[4]


            image_center = image_point.get_center()
            text_center = text_point.get_center()
            pair_vector = text_center - image_center
            midpoint = (image_center + text_center) / 2

            distance_factor = 0.4 if idx < 2 else 1.45
            new_pair_vector = pair_vector * distance_factor
            new_image_center = midpoint - new_pair_vector / 2
            new_text_center = midpoint + new_pair_vector / 2

            delta_image = new_image_center - image_center
            delta_text = new_text_center - text_center

            movement_animations.append(image_point.animate.shift(delta_image))
            movement_animations.append(image_group.animate.shift(delta_image))
            movement_animations.append(text_point.animate.shift(delta_text))
            movement_animations.append(text_group.animate.shift(delta_text))

            target_line = line.copy().put_start_and_end_on(new_image_center, new_text_center)
            target_line.set_color(PURPLE)
            line_animations.append(Transform(line, target_line))
            to_delete.append(line)
            to_delete.append(image_group)
            to_delete.append(text_group)
            to_delete.append(target_line)
            to_delete.append(image_point)
            to_delete.append(text_point)

        concept_specific_text = Tex("Concept-specific Modality Gap", color=PURPLE)
        concept_specific_text.next_to(embedding_space, UP, buff=0.5)

        self.p.play(*movement_animations, *line_animations, run_time=1.3)
        self.p.play(ReplacementTransform(text, concept_specific_text), run_time=0.8)
        self.p.next_slide()

        # Clear only scene content, preserving persistent header/footer elements
        content_to_clear = [encoders, embedding_space, concept_specific_text, *to_delete]
        # visible_content = []
        # for mob in content_to_clear:
        #     if mob in self.p.mobjects and mob not in visible_content:
        #         visible_content.append(mob)
        # if visible_content:
        self.p.play(*[FadeOut(mob) for mob in content_to_clear
                          ], run_time=0.6)
# Add .. to the path to import from the parent directory
import sys
import textwrap
sys.path.append("..")

from templates import MySlide


from manim import *


class DatasetScene(MySlide):
    def construct(self):
        text = "To compare concepts across modalities, we collect a subset of CC3M[1] of $200$ different concepts (spanning the whole concrete-abstract spectrum[2]) with $N=100$ pairs of text and image samples each."

        screen_width = config["frame_width"] - 2
        wrapped_text = textwrap.fill(text, width=60)
        paragraph = Tex(wrapped_text, font_size=28)

        paragraph.scale_to_fit_width(screen_width)
        paragraph.to_edge(UP, buff=1.5)

        # Add examples of text and image pairs (using placeholders)
        samples = [("concept_book.png", "Book"), ("concept_cow.png", "Cow"), ("concept_development.png", "Development"), ("concept_equality.png", "Equality")]

        images = Group()
        to_delete= []
        for img_file, label in samples:
            # Placeholder for image (in practice, load actual images)
            # img_placeholder = Rectangle(width=2, height=2, color=GREY, fill_opacity=0.5)
            img = ImageMobject(img_file).scale_to_fit_height(2)
            img_label = Tex(f"\\texttt{{{label}}}", font_size=32)
            img_group = Group(img, img_label)
            img_group.arrange(DOWN, buff=0.1)
            to_delete.append(img_group)
            images.add(img_group)

        images.arrange(RIGHT, buff=0.5)
        images.next_to(paragraph, DOWN, buff=1)

        # citations_text = r"[1] Piyush Sharma et al. ``Conceptual Captions: A Cleaned, Hypernymed, Image Alt-text Dataset For Automatic Image Captioning''. In: Proceedings of ACL. 2018.\newline[2] Marc Brysbaert, Amy Beth Warriner, and Victor Kuperman. “Concreteness ratings for 40 thousand generally known English word lemmas”. In: Behavior research methods 46.3 (2014), pp. 904-911."

        citations_texts = [
            "[1] Piyush Sharma et al. ``Conceptual Captions: A Cleaned, Hypernymed, Image Alt-text Dataset For Automatic Image Captioning''. In: Proceedings of ACL. 2018.",
            "[2] Marc Brysbaert et al. “Concreteness ratings for 40 thousand generally known English word lemmas”. In: Behavior research methods 46.3 (2014), pp. 904-911."
        ]
        citations = VGroup(*[Tex(r"\mbox{" + ct + "}", font_size=28) for ct in citations_texts])
        citations.arrange(DOWN, aligned_edge=LEFT, buff=0.25)

        # citations = Tex(r"\mbox{" + citations_text + "}", font_size=36)
        if citations.width > screen_width:
            citations.scale_to_fit_width(screen_width)
        # citations.to_corner(DOWN + LEFT, buff=0.5)
        citations.to_edge(DOWN, buff=1)
        citations.to_edge(LEFT, buff=0.5)


        self.p.play(Write(paragraph), Write(citations))
        self.p.play(LaggedStartMap(FadeIn, images), run_time=2)

        self.p.next_slide()

        content_to_clear = [paragraph, citations, *to_delete]
        
        self.p.play(*[FadeOut(mob) for mob in content_to_clear], run_time=0.6)
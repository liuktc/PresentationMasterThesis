from templates import SlideTemplate, TitleSlide
# from title import TitleSlide
# import light_theme
from manim import *

from scenes import ClipScene, DatasetScene, MGFormulasScene, RQScene, SAEFormulasScene, SAEScene, EncodersScene, RQ1Scene, RQ2Scene, RQ3Scene, ConclusionsScene, AppendixScene, AppendixGapEnergyAndSparsityScene, MSIConceptScene

class MainScene(SlideTemplate):
    def __init__(self, **kwargs):
        super().__init__(
            title_str="Image Embeddings",
            name="Luca Domeniconi",
            subtitle="Concept Dependent Modality Gap",
            date_text="March 26, 2026",
            **kwargs,
        )

    def construct(self):
        self.wait_time_between_slides = 0.1
        title = TitleSlide(self)
        title.construct(
            title_str=r"Using Sparse Features to Characterize\\and Mitigate Concept-Dependent Modality Gap\\ in Vision-Language Models",
            name="Luca Domeniconi",
            date_text="March 26, 2026",
            run_time=3.0,
        )

        self.wait_time_between_slides = 0.1
        self.add_slide_template()

        # self.change_title_and_add_page_number("Vision-Language Models (VLMs)")
        vlms_scene = EncodersScene(self)
        vlms_scene.construct()

        self.change_title_and_add_page_number("CLIP (Contrastive Language-Image Pretraining)")
        clip_scene = ClipScene(self)
        clip_scene.construct()

        self.change_title_and_add_page_number("Modality Gap")
        mg_formulas_scene = MGFormulasScene(self)
        mg_formulas_scene.construct()
        
        self.change_title_and_add_page_number("Sparse Autoencoders (SAE)")
        sae_scene = SAEScene(self)
        sae_scene.construct()

        self.change_title_and_add_page_number("SAE Formulas")
        sae_formulas_scene = SAEFormulasScene(self)
        sae_formulas_scene.construct()

        self.change_title_and_add_page_number("Dataset")
        dataset_scene = DatasetScene(self)
        dataset_scene.construct()

        self.change_title_and_add_page_number("Research Questions")
        rq_scene = RQScene(self)
        rq_scene.construct()

        self.change_title_and_add_page_number(r"a", color=BLACK)  # Add a blank page with page number 1
        rq1_scene = RQ1Scene(self)
        rq1_scene.construct()

        self.add_page_number()
        rq2_scene = RQ2Scene(self)
        rq2_scene.construct()

        self.add_page_number()
        rq3_scene = RQ3Scene(self)
        rq3_scene.construct()

        self.change_title_and_add_page_number("Conclusions", color=WHITE)
        conclusions_scene = ConclusionsScene(self)
        conclusions_scene.construct()

        self.change_title_and_add_page_number(r"a", color=BLACK)

        thanks = Tex("Thank you!", font_size=48)
        self.p.play(Write(thanks), run_time=2.0)


        return
        self.change_title_and_add_page_number("Appendix", color=WHITE)
        appendix_scene = AppendixScene(self)
        appendix_scene.construct()

        self.add_page_number()
        appendix_gap_energy_and_sparsity_scene = AppendixGapEnergyAndSparsityScene(self)
        appendix_gap_energy_and_sparsity_scene.construct()

        self.add_page_number()
        msi_concept_scene = MSIConceptScene(self)
        msi_concept_scene.construct()



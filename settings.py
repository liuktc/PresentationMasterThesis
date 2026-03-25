from manim import *

TEXT_COLOR = BLUE
IMAGE_COLOR = RED

default_run_times = {
    Write: 1,
    FadeOut: 1,
    FadeIn: 1,
    Unwrite: 1,
}

for obj, run_time in default_run_times.items():
    obj.set_default(**{"run_time": run_time})

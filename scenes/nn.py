from manim import *


class NN:
    def __init__(
        self,
        layers,
        scene,
        labels,
        ellipsis_layers=None,
        rotate=True,
        extra_middle_gap=0.5,
        layer_spacing=2,
    ):
        self.scene = scene
        self.neurons = VGroup()
        self.connections = VGroup()
        self.ellipsis = VGroup()
        self.labels = labels
        self.labels_mobjects = VGroup()
        self.ellipsis_layers = set(ellipsis_layers or [])

        for i, num_neurons in enumerate(layers):
            layer = VGroup(
                *[
                    Circle(radius=0.2, color=WHITE, fill_opacity=1, fill_color=BLACK).set_z_index(10)
                    for _ in range(num_neurons)
                ]
            )
            layer.arrange(DOWN, buff=0.3)

            if i in self.ellipsis_layers and num_neurons >= 2:
                split = num_neurons // 2
                if num_neurons % 2 == 0:
                    for idx, neuron in enumerate(layer):
                        if idx < split:
                            neuron.shift(UP * (extra_middle_gap / 2))
                        else:
                            neuron.shift(DOWN * (extra_middle_gap / 2))
                else:
                    for idx, neuron in enumerate(layer):
                        if idx < split:
                            neuron.shift(UP * (extra_middle_gap / 2))
                        elif idx > split:
                            neuron.shift(DOWN * (extra_middle_gap / 2))

            layer.shift(RIGHT * (i - 1) * layer_spacing)
            self.neurons.add(layer)

            if i in self.ellipsis_layers:
                dots = VGroup(
                    *[
                        Dot(radius=0.035, color=WHITE, fill_opacity=1).set_z_index(20)
                        for _ in range(3)
                    ]
                )
                dots.arrange(DOWN, buff=0.12)
                dots.move_to(layer.get_center())
                self.ellipsis.add(dots)

        for i in range(len(layers) - 1):
            for n1 in self.neurons[i]:
                for n2 in self.neurons[i + 1]:
                    line = Line(
                        n1.get_center(),
                        n2.get_center(),
                        stroke_width=1,
                        stroke_opacity=0.5,
                        color=WHITE,
                    )
                    self.connections.add(line)

        if rotate:
            self.neurons.rotate(PI / 2)
            self.connections.rotate(PI / 2)
            self.ellipsis.rotate(PI / 2)

        for i, label in enumerate(self.labels):
            label_mobject = MathTex(label)
            label_mobject.next_to(self.neurons[i], RIGHT if rotate else DOWN, buff=0.5)
            self.labels_mobjects.add(label_mobject)

    def get_all_mobjects(self):
        return VGroup(self.neurons, self.connections, self.ellipsis, self.labels_mobjects)

    def display(self):
        self.scene.play(Write(self.neurons), run_time=1)
        if len(self.ellipsis) > 0:
            self.scene.play(FadeIn(self.ellipsis), run_time=0.4)
        self.scene.play(Write(self.connections), run_time=1)
        self.scene.play(Write(self.labels_mobjects), run_time=1)

    def set_activations(self, activations):
        animations = []
        for layer, layer_activations in zip(self.neurons, activations):
            for neuron, activation in zip(layer, layer_activations):
                color = interpolate_color(BLACK, YELLOW, activation)
                animations.append(neuron.animate.set_fill(color))

        if animations:
            self.scene.play(*animations, run_time=0.5)

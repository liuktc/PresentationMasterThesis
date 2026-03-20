from manim import *
import numpy as np
from sklearn.decomposition import PCA

class SparseAutoencoderScene(Scene):
    def construct(self):
        # -----------------------
        # Load weights
        # -----------------------
        data = np.load("sae_weights.npz")
        W_enc = data["W_enc"]
        b_enc = data["b_enc"]
        W_dec = data["W_dec"]
        X = data["X"]

        # PCA projection
        pca = PCA(n_components=2)
        X_proj = pca.fit_transform(X)
        scale = 3
        x_proj_max = max(np.max(np.abs(X_proj)), 1e-8)
        X_proj_scaled = X_proj / x_proj_max * scale

        # Background points
        # dots = VGroup(*[
        #     Dot([x, y, 0], radius=0.02, color=BLUE, fill_opacity=0.3)
        #     for x, y in X_proj_scaled[::10]
        # ])
        # self.add(dots)

        # Moving point and reconstruction

        # -----------------------
        # Helper functions
        # -----------------------
        def encode(x):
            return np.maximum(0, x @ W_enc.T + b_enc)

        def get_top_vectors(x, k=5):
            h = encode(x)
            topk = np.argsort(h)[-k:][::-1]
            vectors = []
            for i in topk:
                vec = h[i] * W_dec[:, i]
                vec_proj = pca.transform([vec])[0]
                vec_proj = vec_proj / x_proj_max * scale
                vectors.append(vec_proj)
            return vectors

        # -----------------------
        # ValueTracker to move through dataset
        # -----------------------
        t = ValueTracker(0)
        self.add(t)

        def state_from_t(t_value):
            idx = int(t_value) % len(X)
            next_idx = (idx + 1) % len(X)
            alpha = t_value % 1.0

            # Linear interpolation between points for smooth motion
            x = (1 - alpha) * X[idx] + alpha * X[next_idx]

            x_proj = pca.transform([x])[0]
            x_proj = x_proj / x_proj_max * scale

            vectors = get_top_vectors(x, k=3)

            current = np.array([0.0, 0.0])
            arrow_specs = []
            for v in vectors:
                start = np.array([current[0], current[1]])
                current += v
                end = np.array([current[0], current[1]])
                arrow_specs.append((start, end))

            return x_proj, current, arrow_specs

        def make_point():
            x_proj, _, _ = state_from_t(t.get_value())
            return Dot([x_proj[0], x_proj[1], 0], color=YELLOW)

        def make_recon_point():
            _, current, _ = state_from_t(t.get_value())
            return Dot([current[0], current[1], 0], color=RED)

        def make_arrows_group():
            _, _, arrow_specs = state_from_t(t.get_value())
            arrows = VGroup()
            for start, end in arrow_specs:
                arrows.add(
                    Arrow(
                        start=[start[0], start[1], 0],
                        end=[end[0], end[1], 0],
                        buff=0,
                        color=GREEN,
                        max_stroke_width_to_length_ratio=10
                    )
                )
            return arrows

        point = always_redraw(make_point)
        recon_point = always_redraw(make_recon_point)
        arrows_group = always_redraw(make_arrows_group)
        self.add(arrows_group, point, recon_point)

        # Animate t to trigger updater
        self.play(t.animate.set_value(1), run_time=2, rate_func=rate_functions.ease_out_cubic)

        self.play(t.animate.set_value(2), run_time=2, rate_func=rate_functions.ease_out_cubic)

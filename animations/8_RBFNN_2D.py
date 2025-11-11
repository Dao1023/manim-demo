from manim import *
import numpy as np

class RBF2DAnimation(ThreeDScene):
    def construct(self):
        # === 参数设置 ===
        centers = np.array([
            [-1, -1],
            [0, 0],
            [1, 1],
            [-1, 1],
            [1, -1]
        ])  # shape: (5, 2)
        b = 0.8  # 共享宽度
        weights = np.array([1.2, -0.8, 1.0, 0.6, -0.5])

        # === 创建 3D 坐标轴 ===
        axes = ThreeDAxes(
            x_range=[-2, 2, 1],
            y_range=[-2, 2, 1],
            z_range=[-1.5, 2, 0.5],
            axis_config={"color": BLUE},
            x_length=6,
            y_length=6,
            z_length=4,
        )
        x_label = axes.get_x_axis_label("x_1")
        y_label = axes.get_y_axis_label("x_2")
        z_label = axes.get_z_axis_label("f")

        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)
        self.add(axes, x_label, y_label, z_label)
        self.wait(1)

        # === 步骤1：显示中心点（在 xy 平面上）===
        center_dots = VGroup()
        for c in centers:
            dot = Dot3D(point=axes.c2p(c[0], c[1], 0), color=RED, radius=0.08)
            center_dots.add(dot)
        self.play(LaggedStart(*[Create(dot) for dot in center_dots], lag_ratio=0.2))
        self.wait(1)

        # === 步骤2：绘制每个 RBF 高斯基函数（未加权）===
        def rbf_func(x, y, center, sigma):
            dx = x - center[0]
            dy = y - center[1]
            return np.exp(-(dx**2 + dy**2) / (2 * sigma**2))

        rbf_surfaces = VGroup()
        for c in centers:
            surface = Surface(
                lambda u, v: axes.c2p(
                    u, v,
                    rbf_func(u, v, c, b)
                ),
                u_range=[-2, 2],
                v_range=[-2, 2],
                resolution=(20, 20),
                fill_opacity=0.6,
                stroke_width=0.5,
                stroke_color=TEAL
            )
            rbf_surfaces.add(surface)

        self.begin_ambient_camera_rotation(rate=0.1)
        self.play(LaggedStart(*[Create(surf) for surf in rbf_surfaces], lag_ratio=0.3))
        self.wait(2)

        # === 步骤3：应用权重（改变高度）===
        weighted_surfaces = VGroup()
        for c, w in zip(centers, weights):
            surface = Surface(
                lambda u, v, c=c, w=w: axes.c2p(
                    u, v,
                    w * rbf_func(u, v, c, b)
                ),
                u_range=[-2, 2],
                v_range=[-2, 2],
                resolution=(20, 20),
                fill_opacity=0.6,
                stroke_width=0.5,
                stroke_color=GREEN
            )
            weighted_surfaces.add(surface)

        self.play(Transform(rbf_surfaces, weighted_surfaces))
        self.wait(2)

        # === 步骤4：叠加形成最终输出曲面 ===
        def final_func(x, y):
            total = 0.0
            for c, w in zip(centers, weights):
                total += w * np.exp(-((x - c[0])**2 + (y - c[1])**2) / (2 * b**2))
            return total

        final_surface = Surface(
            lambda u, v: axes.c2p(u, v, final_func(u, v)),
            u_range=[-2, 2],
            v_range=[-2, 2],
            resolution=(30, 30),
            fill_opacity=0.8,
            stroke_width=0,
            color=YELLOW
        )

        self.play(Transform(rbf_surfaces, final_surface))
        self.wait(3)

        self.stop_ambient_camera_rotation()
        self.wait(1)
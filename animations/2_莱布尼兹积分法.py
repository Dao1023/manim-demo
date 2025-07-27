from manim import *
import numpy as np

class Leibniz3DProof(ThreeDScene):
    def construct(self):
        # 定义函数和坐标系
        def f(x, y):
            return np.sin(x) + 0.5 * np.cos(y) + 1
        
        axes = ThreeDAxes(
            x_range=[0, 3], y_range=[0, 3], z_range=[0, 3],
            x_length=6, y_length=6, z_length=4
        )
        
        # 绘制曲面 z = f(x,y)
        surface = Surface(
            lambda x, y: axes.c2p(x, y, f(x, y)),
            u_range=[0, 3], v_range=[0, 3],
            resolution=30,
            fill_opacity=0.7,
            checkerboard_colors=[BLUE_D, GREEN_D],
        )
        
        # 设置摄像机
        self.set_camera_orientation(phi=70*DEGREES, theta=-30*DEGREES, distance=6)
        self.play(Create(axes), Create(surface))
        
        # 动态展示积分过程 T(x) = ∫f dy
        x_tracker = ValueTracker(0.1)
        integral_slice = always_redraw(lambda:
            Surface(
                lambda x, y: axes.c2p(x, y, f(x, y)),
                u_range=[0, x_tracker.get_value()],
                v_range=[0, x_tracker.get_value()],
                resolution=20,
                fill_opacity=0.5,
                color=GREEN,
            )
        )
        self.play(Create(integral_slice))
        self.play(x_tracker.animate.set_value(2.5), run_time=3)
        
        # 高亮边界项 f(x,x)（红色曲线）
        boundary_curve = ParametricFunction(
            lambda t: axes.c2p(t, t, f(t, t)),
            t_range=[0, 3],
            color=RED,
            stroke_width=4
        )
        self.play(Create(boundary_curve))
        
        # 显示边界贡献 f(x,x)Δx
        dx = 0.2
        boundary_strip = Polygon(
            axes.c2p(2.5, 2.5, 0),
            axes.c2p(2.5 + dx, 2.5 + dx, 0),
            axes.c2p(2.5 + dx, 2.5 + dx, f(2.5, 2.5)),
            axes.c2p(2.5, 2.5, f(2.5, 2.5)),
            color=RED, fill_opacity=0.5
        )
        self.play(FadeIn(boundary_strip))
        
        # 显示内部演化 ∫f_x dy
        def f_x(x, y):
            return np.cos(x)  # f的偏导数
        
        internal_change = Rectangle(
            width=2.5 * axes.x_axis.unit_size,
            height=dx * axes.y_axis.unit_size,
            color=YELLOW,
            fill_opacity=0.3,
            stroke_width=0
        ).move_to(axes.c2p(1.25, 1.25, 0))
        self.play(FadeIn(internal_change))
        
        # 显示公式
        formula = MathTex(
            r"\frac{d}{dx}\int_{0}^{x} f(x,y) dy =",
            r"f(x,x)",
            r"+",
            r"\int_{0}^{x} f_x(x,y) dy"
        ).to_edge(UP)
        formula[1].set_color(RED)
        formula[3].set_color(YELLOW)
        self.add_fixed_in_frame_mobjects(formula)
        self.play(Write(formula))
        self.wait(3)
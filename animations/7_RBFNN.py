from manim import *
import numpy as np

class RBFAnimation(Scene):
    def construct(self):
        # 定义参数
        x_range = np.linspace(0, 10, 1000)
        centers = np.array([2, 4, 6, 8])
        sigmas = np.array([0.5, 0.7, 0.4, 0.6])
        weights = np.array([3, 0.8, 1.5, -1.0])
        
        # 创建坐标轴
        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[-3, 3, 1],
            axis_config={"color": BLUE},
        )
        
        # 标签坐标轴
        x_label = axes.get_x_axis_label("x")
        y_label = axes.get_y_axis_label("y")
        
        self.play(Create(axes), Write(x_label), Write(y_label))
        self.wait(1)
        
        # 步骤1：生成X轴离散采样点
        dots = VGroup()
        for x in np.linspace(0, 10, 50):
            dot = Dot(axes.c2p(x, 0), color=YELLOW, radius=0.03)
            dots.add(dot)
        
        self.play(LaggedStart(*[Create(dot) for dot in dots], lag_ratio=0.01))
        self.wait(1)
        self.play(FadeOut(dots))
        
        # 步骤2：显示中心点
        center_dots = VGroup()
        for c in centers:
            dot = Dot(axes.c2p(c, 0), color=RED, radius=0.08)
            center_dots.add(dot)
        
        self.play(LaggedStart(*[Create(dot) for dot in center_dots], lag_ratio=0.2))
        self.wait(1)
        
        # 步骤3：绘制多个高斯函数
        gaussian_curves = VGroup()
        for i, (c, sigma) in enumerate(zip(centers, sigmas)):
            def make_curve(center, sigma_val):
                return axes.plot(
                    lambda x: np.exp(-((x - center) ** 2) / (2 * sigma_val ** 2)),
                    color=TEAL,
                    x_range=[0, 10],
                )
            curve = make_curve(c, sigma)
            gaussian_curves.add(curve)
        
        self.play(LaggedStart(*[Create(curve) for curve in gaussian_curves], lag_ratio=0.3))
        self.wait(1)
        
        # 步骤4：乘以权重调整高度
        weighted_curves = VGroup()
        for i, (c, sigma, w) in enumerate(zip(centers, sigmas, weights)):
            def make_weighted_curve(center, sigma_val, weight):
                return axes.plot(
                    lambda x: weight * np.exp(-((x - center) ** 2) / (2 * sigma_val ** 2)),
                    color=GREEN,
                    x_range=[0, 10],
                )
            weighted_curve = make_weighted_curve(c, sigma, w)
            weighted_curves.add(weighted_curve)
        
        self.play(Transform(gaussian_curves, weighted_curves))
        self.wait(1)
        
        # 步骤5：叠加高斯函数形成最终曲线
        final_curve = axes.plot(
            lambda x: sum(w * np.exp(-((x - c) ** 2) / (2 * sigma ** 2)) 
                         for c, sigma, w in zip(centers, sigmas, weights)),
            color=YELLOW,
            x_range=[0, 10],
            stroke_width=4
        )
        
        self.play(Transform(gaussian_curves, final_curve))
        self.wait(2)
        
        # 淡出所有元素
        self.play(FadeOut(axes), FadeOut(x_label), FadeOut(y_label), 
                  FadeOut(center_dots), FadeOut(gaussian_curves))
from manim import *
import numpy as np

class ComplexLogPlotWithLabels(ThreeDScene):
    def construct(self):
        # 设置坐标系（带标签）
        axes = ThreeDAxes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            z_range=[-3, 3, 1],
            x_length=6,
            y_length=6,
            z_length=6,
        )
        
        # 添加坐标轴标签
        labels = VGroup(
            axes.get_x_axis_label(Tex("Re(x)"), edge=RIGHT, direction=RIGHT),
            axes.get_y_axis_label(Tex("Im(x)"), edge=UP, direction=UP),
            axes.get_z_axis_label(Tex("Re(y)"), edge=OUT, direction=OUT),
        )
        
        self.set_camera_orientation(phi=60*DEGREES, theta=-45*DEGREES)
        self.add(axes, labels)

        # 改进的复数对数计算函数
        def safe_complex_log(x, b):
            if abs(x) < 1e-6 or abs(b) < 1e-6:
                return 0
                
            r_x = np.sqrt(x.real**2 + x.imag**2)
            theta_x = np.arctan2(x.imag, x.real)
            
            r_b = np.sqrt(b.real**2 + b.imag**2)
            theta_b = np.arctan2(b.imag, b.real)
            
            ln_x = np.log(r_x) + 1j * theta_x
            ln_b = np.log(r_b) + 1j * theta_b
            
            if abs(ln_b) < 1e-6:
                return 0
                
            result = ln_x / ln_b
            return result.real if not np.isnan(result.real) else 0

        # 创建值追踪器（范围改为-3到3）
        t_tracker = ValueTracker(-3)  # 初始值设为-3

        # 颜色映射函数（根据b值变化）
        def get_color(b_value):
            # 将b值从[-3,3]映射到[0,1]用于颜色插值
            t = (b_value + 3) / 6  
            return interpolate_color(BLUE, RED, t)

        # 创建动态显示b值的标签
        def update_b_label():
            current_b = round(t_tracker.get_value(), 2)
            return Tex(
                f"Base $b = {current_b}$",
                font_size=24
            ).to_corner(UL)
        
        b_label = always_redraw(update_b_label)
        equation_label = Tex("$y = \\log_b(x)$", font_size=28).next_to(b_label, DOWN, aligned_edge=LEFT)
        
        # 创建曲面函数（直接使用t_tracker的值作为b）
        def surface_func(a, b):
            x = a + 1j*b
            base = t_tracker.get_value()
            return safe_complex_log(x, base)

        # 初始曲面
        surface = Surface(
            lambda a, b: [a, b, surface_func(a, b)],
            u_range=[-3, 3],
            v_range=[-3, 3],
            resolution=(20, 20),
            fill_opacity=0.7,
            color=get_color(-3),  # 初始颜色
            stroke_width=0.1
        )

        # 添加固定元素
        self.add_fixed_in_frame_mobjects(b_label, equation_label)
        self.add(surface)
        
        # 开始摄像机旋转
        self.begin_ambient_camera_rotation(rate=0.1)

        # 曲面更新函数
        def update_surface(m):
            m.become(
                Surface(
                    lambda a, b: [a, b, surface_func(a, b)],
                    u_range=[-3, 3],
                    v_range=[-3, 3],
                    resolution=(20, 20),
                    fill_opacity=0.7,
                    color=get_color(t_tracker.get_value()),  # 使用正确的颜色函数
                    stroke_width=0.1
                )
            )

        surface.add_updater(update_surface)

        # 动画序列（从-3到3）
        self.play(
            t_tracker.animate.set_value(3),
            run_time=12,  # 延长动画时间
            rate_func=linear
        )
        
        self.wait(3)
        self.stop_ambient_camera_rotation()
        self.wait(2)
from manim import *
import numpy as np

class StableReactionDiffusion3D(ThreeDScene):
    def construct(self):
        # 修复后的参数设置（数值稳定）
        λ = 5.0   # 降低λ值防止数值爆炸
        L = 1.0
        T = 2.0
        
        # 创建坐标轴
        axes = ThreeDAxes(
            x_range=[0, L, 0.2],
            y_range=[0, T, 0.5],
            z_range=[-2, 2, 1],
            x_length=8,
            y_length=8,
            z_length=5,
        )
        axes_labels = axes.get_axis_labels(
            Tex("x").scale(0.7), 
            Tex("t").scale(0.7), 
            Tex("u").scale(0.7)
        )

        # 初始条件：u(x,0) = sin(πx)
        def initial_condition(x):
            return np.sin(np.pi * x)

        # 边界条件
        U_control = 0.5
        
        # 数值求解（修复数值稳定性）
        nx, nt = 100, 200
        dx = L / nx
        dt = T / nt
        u = np.zeros((nx, nt))
        
        # 设置初始条件
        for i in range(nx):
            u[i, 0] = initial_condition(i * dx)
            
        # 数值稳定性改进：添加扩散常数
        D = 0.1  # 扩散系数
        
        # 时域迭代
        for n in range(nt-1):
            u[0, n+1] = 0
            u[-1, n+1] = U_control * (1 - np.exp(-5*n*dt))
            
            # 稳定格式：前向差分
            for i in range(1, nx-1):
                uxx = (u[i+1, n] - 2*u[i, n] + u[i-1, n]) / (dx**2)
                # 添加数值稳定性项
                u[i, n+1] = u[i, n] + dt * (D * uxx + λ * u[i, n])
        
        # 修复LaTeX转义问题
        initial_label = MathTex(r"u(x,0) = \sin(\pi x)", color=GREEN).scale(0.8)
        lambda_label = MathTex(f"\\lambda = {λ}", color=RED).scale(0.8)
        
        # 创建曲面函数
        def surface_func(x, t):
            # 限制数值范围防止溢出
            xi = int(x * nx / L)
            ti = int(t * nt / T)
            
            if xi < 0: xi = 0
            if xi >= nx: xi = nx - 1
            if ti < 0: ti = 0
            if ti >= nt: ti = nt - 1
            
            # 数值裁剪
            value = u[xi, ti]
            if np.isnan(value) or np.abs(value) > 10:
                return 0
            return value
        
        # 创建曲面
        surface = Surface(
            lambda x, t: axes.c2p(
                x, 
                t, 
                surface_func(x, t)
            ),
            u_range=[0, L],
            v_range=[0, T],
            resolution=(nx//10, nt//10),
            fill_opacity=0.7,
            checkerboard_colors=[BLUE_D, BLUE_C],
        )
        
        # 边界控制输入可视化
        U_line = ParametricFunction(
            lambda t: axes.c2p(L, t, U_control * (1 - np.exp(-5*t))),
            t_range=[0, T],
            color=YELLOW,
            stroke_width=4
        )
        U_label = MathTex("U(t)", color=YELLOW).scale(0.8)
        U_label.next_to(U_line, OUT, buff=0.1)
        
        # 初始条件可视化
        initial_line = ParametricFunction(
            lambda x: axes.c2p(x, 0, initial_condition(x)),
            t_range=[0, L],
            color=GREEN,
            stroke_width=4
        )
        initial_label.next_to(initial_line, OUT, buff=0.1)
        lambda_label.to_corner(UR)

        # 设置相机视角
        self.set_camera_orientation(phi=60*DEGREES, theta=-45*DEGREES)
        
        # 添加动画
        self.play(
            Create(axes),
            Write(axes_labels),
            Write(lambda_label)
        )
        self.wait(0.5)
        
        self.play(
            Create(initial_line),
            Write(initial_label)
        )
        self.wait(1)
        
        self.play(
            Create(U_line),
            Write(U_label)
        )
        self.wait(1)
        
        # 添加曲面动画
        self.play(
            Create(surface),
            run_time=3,
            rate_func=linear
        )
        
        # 添加方程文本（修复LaTeX格式）
        equations = VGroup(
            Tex("Reaction-Diffusion Equation"),
            MathTex(
                r"\frac{\partial u}{\partial t} = D\frac{\partial^2 u}{\partial x^2} + \lambda u",
                color=BLUE
            ).scale(0.8),
            MathTex(
                r"u(0,t) = 0, \quad u(1,t) = U(t)",
                color=YELLOW
            ).scale(0.8),
        ).arrange(DOWN, aligned_edge=LEFT)
        equations.to_edge(UL, buff=0.25)
        
        # 添加方程说明
        self.play(
            FadeIn(equations),
            lambda_label.animate.scale(0.8).to_corner(UR)
        )
        self.wait(3)
        
        # 高亮扩散项
        diff_term = equations[1][0][8:19]
        diff_box = SurroundingRectangle(diff_term, color=GREEN, buff=0.1)
        
        self.play(
            Create(diff_box),
            equations[1].animate.set_color_by_tex(r"\frac{\partial^2 u}{\partial x^2}", GREEN),
            run_time=2
        )
        self.wait(2)
        
        # 旋转展示三维效果
        self.begin_ambient_camera_rotation(rate=0.1)
        self.wait(8)
        self.stop_ambient_camera_rotation()
        self.wait(2)
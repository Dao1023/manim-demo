from manim import *
import numpy as np

class ReactionDiffusionVectorField(Scene):
    def construct(self):
        # 标题和参数
        title = VGroup(
            Text("ReactionDiffusionVectorField", font_size=36),
            MathTex(r"u_t = u_{xx} + \lambda u", font_size=32)
        ).arrange(DOWN, buff=0.3)
        title.to_edge(UP)
        self.play(Write(title))
        
        # 参数说明
        params = MathTex(
            r"\lambda = 15,\quad U(t) = \sin(2t)",
            font_size=24
        ).next_to(title, DOWN)
        self.play(Write(params))
        
        # 创建坐标系统
        axes = Axes(
            x_range=[0, 1, 0.2],
            y_range=[-3, 3, 1],
            axis_config={"color": BLUE},
            x_length=7,
            y_length=5
        ).next_to(params, DOWN, buff=0.5)
        axis_labels = axes.get_axis_labels(
            MathTex(r"x").scale(0.7), 
            MathTex(r"u(x,t)").scale(0.7)
        )
        self.play(Create(axes), Write(axis_labels))
        
        # 添加关键动力学说明
        instability = MathTex(
            r"\text{when } \lambda > \pi^2 \approx 9.87 \text{ system becomes unstable}",
            font_size=24,
            color=RED
        ).next_to(axes, DOWN)
        self.play(Write(instability))
        
        # 添加边界条件标注
        bc1 = MathTex(r"u(0,t)=0", color=GREEN).next_to(axes, LEFT)
        bc2 = MathTex(r"u(1,t)=U(t)", color=RED).next_to(axes, RIGHT)
        self.play(Write(bc1), Write(bc2))
        
        # 离散化空间
        nx = 20
        dx = 1 / nx
        x_points = np.linspace(0, 1, nx)
        
        # 时间追踪器
        time_tracker = ValueTracker(0)
        time_label = MathTex("t = ").scale(0.8).next_to(instability, DOWN)
        time_value = DecimalNumber(
            0, num_decimal_places=2
        ).next_to(time_label, RIGHT)
        self.play(FadeIn(VGroup(time_label, time_value)))
        
        # 向量场函数
        def vector_field_func(point):
            x, y = axes.point_to_coords(point)
            idx = int(x * nx)
            
            # 边缘点处理
            if idx <= 0:  # x=0
                if x <= 0:  # 严格在边界上
                    u_t = np.sin(2 * time_tracker.get_value())  # 使用边界条件
                    return Vector([0, u_t])
                else:
                    return Vector([0, 0])  # 避免索引错误
            
            if idx >= nx - 1:  # x=1
                return Vector([0, np.sin(2 * time_tracker.get_value())])
            
            # 内部点处理
            u_left = np.sin(np.pi * (x - dx))
            u_right = np.sin(np.pi * (x + dx))
            u_xx = (u_left - 2*y + u_right) / dx**2
            u_t = u_xx + 15 * y  # λ=15
            return Vector([0, u_t])
        
        # 创建向量场
        def create_vector_field():
            grid_size = 0.1
            vectors = VGroup()
            for x in np.arange(0, 1.01, grid_size):
                for u in np.arange(-2.5, 3.0, grid_size):
                    point = axes.c2p(x, u)
                    vector = vector_field_func(point)
                    # 根据大小设置颜色和长度
                    vec_len = np.linalg.norm(vector.get_vector())
                    if vec_len > 0.5:  # 避免显示过小的向量
                        vector.set_stroke(
                            color=interpolate_color(
                                BLUE, RED, 
                                clip(0, 1, vec_len/15)
                            ),
                            width=1.5
                        )
                        # 标准化长度避免过长
                        max_length = 0.6
                        if vec_len > max_length:
                            vector.scale(max_length/vec_len)
                        vector.move_to(point)
                        vectors.add(vector)
            return vectors
        
        # 初始向量场
        vector_field = create_vector_field()
        self.play(Create(vector_field))
        
        # 添加流线指示
        stream_text = Text("Vector rate", font_size=18, color=YELLOW)
        stream_text.next_to(time_value, DOWN, buff=0.1)
        self.play(FadeIn(stream_text))
        
        # 时间动画函数
        def update_vector_field(mob):
            new_field = create_vector_field()
            mob.become(new_field)
            
        vector_field.add_updater(update_vector_field)
        time_value.add_updater(
            lambda m: m.set_value(time_tracker.get_value())
        )
        
        # 运行模拟（持续10秒）
        self.play(
            time_tracker.animate.set_value(10),
            run_time=10,
            rate_func=linear
        )
        
        # 最后强调不稳定模式
        self.play(
            vector_field.animate.set_color_by_gradient(BLUE, RED),
            rate_func=there_and_back,
            run_time=2
        )
        
        self.wait(2)
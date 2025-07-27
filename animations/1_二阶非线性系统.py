from manim import *
import numpy as np
import math
import random

class NonlinearSystem(Scene):
    def construct(self):
        # 系统参数 - 使用更清晰的排版
        system_eqs = VGroup(
            MathTex(r"\dot{x}_1 = x_2 + x_1^2", color=BLUE),
            MathTex(r"\dot{x}_2 = u", color=GREEN)
        ).arrange(DOWN, aligned_edge=LEFT)
        
        # 将方程移到左上角，留出更多空间
        system_eqs.to_corner(UL, buff=0.5)
        
        # 添加标题
        title = Tex("Second-order nonlinear system", font_size=36).to_edge(UP)
        
        self.play(Write(title), Write(system_eqs))
        self.wait(1)
        
        # 创建更大的坐标轴
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            x_length=7,
            y_length=7,
            axis_config={"color": WHITE, "font_size": 24},
        ).shift(DOWN*0.5)
        
        # 更大的坐标轴标签
        axes_labels = axes.get_axis_labels(
            Tex("$x_1$", font_size=28).set_color(BLUE), 
            Tex("$x_2$", font_size=28).set_color(GREEN)
        )
        
        self.play(Create(axes), Write(axes_labels))
        self.wait(1)
        
        # 定义向量场函数
        def vector_field_func(point):
            x, y = axes.point_to_coords(point)
            u = -x - y - 0.5*x**2  # 改进的控制输入
            dx = y + x**2
            dy = u
            # 限制向量长度防止过大
            norm = np.sqrt(dx**2 + dy**2)
            if norm > 3:
                dx, dy = dx/norm*3, dy/norm*3
            return axes.c2p(dx, dy) - axes.c2p(0, 0)
        
        # 创建向量场
        vector_field = ArrowVectorField(
            vector_field_func,
            x_range=[-2.5, 2.5, 0.5],
            y_range=[-2.5, 2.5, 0.5],
            length_func=lambda norm: 0.3 * sigmoid(norm),
            colors=[BLUE, GREEN],
        )
        
        self.play(Create(vector_field))
        self.wait(1)
        

        def generate_spiral_points(num_points=48, max_radius=3.0):
            points = []
            golden_angle = math.pi * (3 - math.sqrt(5))  # 黄金角度，用于均匀分布
            
            for i in range(1, num_points + 1):
                # 使用平方根使点在半径上分布更均匀
                radius = max_radius * math.sqrt(i / num_points)
                
                # 黄金角度产生螺旋效果
                angle = golden_angle * i
                
                # 添加一些随机扰动使点不那么完美排列
                radius_jitter = radius * (1 + (random.random() - 0.5) * 0.1)
                angle_jitter = angle + (random.random() - 0.5) * 0.2
                
                x = radius_jitter * math.cos(angle_jitter)
                y = radius_jitter * math.sin(angle_jitter)
                
                points.append([round(x, 2), round(y, 2)])
            
            return points

        spiral_points = generate_spiral_points()


        trajectories = VGroup()
        for x0, y0 in spiral_points:
            # 数值积分模拟轨迹
            dt = 0.05
            t_max = 5  # 减少模拟时间
            points = [axes.c2p(x0, y0)]
            x, y = x0, y0
            for _ in range(int(t_max/dt)):
                u = -x - y - 0.5*x**2  # 改进的控制输入
                dx = y + x**2
                dy = u
                x += dx * dt
                y += dy * dt
                
                # 如果超出范围则停止
                if abs(x) > 10 or abs(y) > 10:
                    break
                
                points.append(axes.c2p(x, y))
            
            trajectory = VMobject()
            trajectory.set_points_smoothly(points)
            trajectory.set_stroke(width=2, color=YELLOW)
            trajectories.add(trajectory)
        
        self.play(Create(trajectories), run_time=30)
        self.wait(2)
        

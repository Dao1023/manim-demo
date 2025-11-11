from manim import *

class MovingPointsOnNumberLine(Scene):
    def construct(self):
        # 数轴
        number_line = NumberLine(
            x_range=[-30, 15, 2],
            length=12,
            include_numbers=True,
            label_direction=DOWN,
        )
        self.play(Create(number_line))

        # 固定点 A, B, C
        A = -24
        B = -10
        C = 10

        dot_A = Dot(number_line.n2p(A), color=RED)
        dot_B = Dot(number_line.n2p(B), color=GREEN)
        dot_C = Dot(number_line.n2p(C), color=BLUE)
        label_A = Text("A", font_size=24).next_to(dot_A, UP)
        label_B = Text("B", font_size=24).next_to(dot_B, UP)
        label_C = Text("C", font_size=24).next_to(dot_C, UP)

        self.play(
            Create(VGroup(dot_A, dot_B, dot_C)),
            Write(VGroup(label_A, label_B, label_C))
        )

        # 动点 P
        dot_P = Dot(number_line.n2p(A), color=YELLOW)
        label_P = Text("P", font_size=24, color=YELLOW).next_to(dot_P, UP)
        self.play(Create(dot_P), Write(label_P))

        # P 移动到 B（0 到 14 秒）
        self.play(
            dot_P.animate.move_to(number_line.n2p(B)),
            label_P.animate.next_to(number_line.n2p(B), UP),
            run_time=14,
            rate_func=linear
        )

        # 此时创建 Q
        dot_Q = Dot(number_line.n2p(A), color=PURPLE)
        label_Q = Text("Q", font_size=24, color=PURPLE).next_to(dot_Q, UP)
        self.play(Create(dot_Q), Write(label_Q))

        # 同步移动 P 和 Q
        # 总时间从 t=14 开始，模拟到 t=37（足够覆盖所有解）
        total_sim_time = 23  # 从 t=14 到 t=37

        # 定义 updater
        p_start_time = 14  # P 已经走了14秒
        q_start_time = 0   # Q 的局部时间

        def p_updater(mob, dt):
            nonlocal p_start_time
            p_start_time += dt
            pos = -24 + p_start_time
            mob.move_to(number_line.n2p(pos))
            label_P.next_to(mob, UP)

        def q_updater(mob, dt):
            nonlocal q_start_time
            q_start_time += dt
            tau = q_start_time
            if tau <= 34 / 3:
                pos = -24 + 3 * tau
            elif tau <= 68 / 3:
                pos = 86 - 3 * (tau + 14) + 3 * 14  # 简化为 86 - 3*(tau + 14 - 14) = 86 - 3*tau
                # 实际：Q(t) = 86 - 3t, t = 14 + tau → Q = 86 - 3(14 + tau) = 44 - 3*tau
                # 但这里 tau 是 Q 的局部时间，所以 Q = -24 + 3*tau (去程), 或 10 - 3*(tau - 34/3) (返程)
                # 更清晰写法：
                if tau <= 34 / 3:
                    pos = -24 + 3 * tau
                else:
                    pos = 10 - 3 * (tau - 34 / 3)
            else:
                pos = -24  # 停止
            mob.move_to(number_line.n2p(pos))
            label_Q.next_to(mob, UP)

        dot_P.add_updater(p_updater)
        dot_Q.add_updater(q_updater)

        self.add(dot_P, label_P, dot_Q, label_Q)

        # 运行动画
        self.wait(total_sim_time)

        # 移除 updater
        dot_P.clear_updaters()
        dot_Q.clear_updaters()

        # 显示答案
        solutions = [20, 22, 27, 28]
        ans_text = VGroup(*[
            MathTex(f"t = {s}") for s in solutions
        ]).arrange(DOWN).to_edge(UP)
        self.play(Write(ans_text))
        self.wait(2)
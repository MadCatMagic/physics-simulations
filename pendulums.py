g = 9.81

from simulation import Sim
from context import Context
from math import sin, cos, tan, pi
from vector import v2

# q = (x, theta)
class pendulum(Sim):
    def setParams(self):
        self.m = 1
        self.M = 2
        self.l = 0.5

    def setd2s(self):
        theta = self.q[1]
        d_theta = self.d_q[1]
        tdd = (self.m * self.l * d_theta ** 2 * sin(theta) * cos(theta) + (self.m + self.M) * g * sin(theta)) / (self.m * self.l * cos(theta) ** 2 - (self.m + self.M) * self.l)
        self.d2_q = (
            -g * tan(theta) - self.l * tdd / cos(theta),
            tdd
        )

    def guiEditables(self) -> bool:
        dsedited = self.defaultSliders(["x_0", "v_0", "theta_0", "omega_0"], [(-2.0, 2.0), (-1.0, 1.0), (-pi, pi), (-2.0 * pi, 2.0 * pi)])
        m = self.autoslider("m", 0.0, 10.0)
        M = self.autoslider("M", 0.0, 10.0)
        l = self.autoslider("l", 0.01, 2.0)
        return any((dsedited, m, M, l))

    def displayFrame(self, ctx: Context, q, d_q, d2_q):
        ctx.col = (200, 200, 200)
        ctx.line(v2(-5, 0), v2(5, 0))
        ctx.col = (255, 255, 255)
        ctx.rect(v2(q[0], 0.1), v2(0.1, 0.1))
        ctx.line(v2(q[0], 0), v2(q[0] + self.l * sin(q[1]), -self.l * cos(q[1])))
        ctx.circle(v2(q[0] + self.l * sin(q[1]), -self.l * cos(q[1])), 0.1)

# q = (theta1, theta2)
class pendulum2(Sim):
    def setParams(self):
        self.m1 = 1
        self.m2 = 2
        self.l1 = 0.5
        self.l2 = 0.9

    def setd2s(self):
        the1, the2 = self.q
        dthe1, dthe2 = self.d_q
        sd = sin(the1 - the2)
        cd = cos(the1 - the2)
        mm = self.m1 + self.m2
        a = self.m2 * self.l1 * cd
        b = self.m2 * self.l2
        c = self.m2 * self.l1 * dthe1 ** 2 * sd - g * self.m2 * sin(the2)
        d = self.l1 * mm
        e = self.m2 * self.l2 * cd
        f = - self.m2 * self.l2 * dthe2 ** 2 * sd - g * mm * sin(the1)
        self.d2_q = (
            (c * e - b * f) / (a * e - b * d),
            (a * f - c * d) / (a * e - b * d)
        )
        #if self.d2_q[0] > 1e5 or self.d2_q[1] > 1e5:
        #    raise ValueError()

    def guiEditables(self) -> bool:
        dsedited = self.defaultSliders(["theta_1,0", "omega_1,0", "theta_2,0", "omega_2,0"], [(-pi, pi), (-2.0 * pi, 2.0 * pi), (-pi, pi), (-2.0 * pi, 2.0 * pi)])
        m1 = self.autoslider("m1", 0.0, 10.0)
        m2 = self.autoslider("m2", 0.0, 10.0)
        l1 = self.autoslider("l1", 0.01, 2.0)
        l2 = self.autoslider("l2", 0.01, 2.0)
        return any((dsedited, m1, m2, l1, l2))

    def displayFrame(self, ctx: Context, q, d_q, d2_q):
        ctx.col = (200, 200, 200)
        ctx.line(v2(-5, 0), v2(5, 0))
        ctx.col = (255, 255, 255)
        p1 = self.l1 * v2(sin(q[0]), -cos(q[0]))
        p2 = p1 + self.l2 * v2(sin(q[1]), -cos(q[1]))
        ctx.line(v2(), p1)
        ctx.line(p1, p2)
        ctx.circle(p1, 0.08)
        ctx.circle(p2, 0.08)

if __name__ == "__main__":
    import main
    options = ["pendulum with block", "double pendulum"]
    s = "\n".join(f"{i}: {option}" for i, option in enumerate(options))
    option = int(input(f"enter option:\n{s}\n"))
    if option == 0:
        main.simulate(pendulum(float, 0, (0, 0.6), (0, -0.1)), "Pendulums")
    elif option == 1:
        main.simulate(pendulum2(float, 0, (0.3, 0.6), (0, -0.1)), "Pendulums")
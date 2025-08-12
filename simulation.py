
from math import sin, cos, tan, pi
from vector import v2, v3
from context import Context

from imgui.core import slider_float

simDataType = float | v2 | v3
class Sim:
    def __init__(self, t0: float, q0: tuple[simDataType, ...], d_q0: tuple, d2_q0: tuple):
        # current values
        self.t = t0
        self.q: tuple = q0
        self.d_q: tuple = d_q0
        self.d2_q: tuple = d2_q0
        # history variables
        self.h_T = [t0]
        self.h_Q = [q0]
        self.h_dQ = [d_q0]
        self.h_d2Q = [d2_q0]

    def resetSim(self):
        self.t = self.h_T[0]
        self.q = self.h_Q[0]
        self.d_q = self.h_dQ[0]
        self.d2_q = self.h_d2Q[0]
        self.h_T = [self.t]
        self.h_Q = [self.q]
        self.h_dQ = [self.d_q]
        self.h_d2Q = [self.d2_q]

    def setParams(self):
        raise NotImplementedError()

    def setd2s(self):
        raise NotImplementedError()
    
    def displayFrame(self, ctx: Context, q, d_q, d2_q):
        raise NotImplementedError()
    
    def autoslider(self, name: str, rmin: float, rmax: float) -> bool:
        c, v = slider_float(name, getattr(self, name), rmin, rmax)
        setattr(self, name, v)
        return c
    
    def defaultSliders(self, names: list[str], ranges: list[tuple[float, float]]) -> bool:
        n = len(self.q)
        changed = [False for _ in range(n * 2)]
        new_h_Q = [0 for _ in range(n)]
        new_h_dQ = [0 for _ in range(n)]
        for i in range(n):
            changed[i * 2], new_h_Q[i] = slider_float(names[i * 2], self.h_Q[0][i], ranges[i * 2][0], ranges[i * 2][1])
            changed[i * 2 + 1], new_h_dQ[i] = slider_float(names[i * 2 + 1], self.h_dQ[0][i], ranges[i * 2 + 1][0], ranges[i * 2 + 1][1])
        self.h_Q[0] = tuple(new_h_Q)
        self.h_dQ[0] = tuple(new_h_dQ)
        return any(changed)
        
    def guiEditables(self) -> bool:
        raise NotImplementedError()
    
    def update(self, dt):
        self.setd2s()
        self.d_q = tuple(map(lambda x: x[0] + x[1] * dt, zip(self.d_q, self.d2_q)))
        self.q = tuple(map(lambda x: x[0] + x[1] * dt, zip(self.q, self.d_q)))

        self.t += dt

        self.h_T.append(self.t)
        self.h_Q.append(self.q)
        self.h_dQ.append(self.d_q)
        self.h_d2Q.append(self.d2_q)

    def run(self, duration, dt):
        t0 = self.t
        while self.t - t0 < duration:
            self.update(dt)

g = 9.81
# q = (x, theta)
class pendulum(Sim):
    def setParams(self):
        self.m = 1
        self.M = 2
        self.l = 0.5

    def setd2s(self):
        theta = self.q[1]
        d_theta = self.d_q[1]
        tdd = (self.m * self.l * d_theta ** 2 * sin(theta) * cos(theta) - (self.m + self.M) * g * sin(theta)) / (self.m * self.l * cos(theta) ** 2 - (self.m + self.M) * self.l)
        self.d2_q = (
            g * tan(theta) - self.l * tdd / cos(theta),
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
        if self.d2_q[0] > 1e5 or self.d2_q[1] > 1e5:
            raise ValueError()

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
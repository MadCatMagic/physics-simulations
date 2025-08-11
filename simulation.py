
from math import sin, cos, tan
from vector import v2, v3
from context import Context

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

    def setd2s(self):
        raise NotImplementedError()
    
    def displayFrame(self, ctx: Context, q, d_q, d2_q):
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

# q = (x, theta)
class pendulum(Sim):
    def setParams(self):
        self.m = 1
        self.M = 2
        self.l = 0.5
        self.g = -9.81

    def setd2s(self):
        theta = self.q[1]
        d_theta = self.d_q[1]
        tdd = (self.m * self.l * d_theta ** 2 * sin(theta) * cos(theta) - (self.m + self.M) * self.g * sin(theta)) / (self.m * self.l * cos(theta) ** 2 - (self.m + self.M) * self.l)
        self.d2_q = (
            self.g * tan(theta) - self.l * tdd / cos(theta),
            tdd
        )

    def displayFrame(self, ctx: Context, q, d_q, d2_q):
        ctx.col = (200, 200, 200)
        ctx.line(v2(-5, 0), v2(5, 0))
        ctx.col = (255, 255, 255)
        ctx.rect(v2(q[0], 0.1), v2(0.1, 0.1))
        ctx.line(v2(q[0], 0), v2(q[0] + self.l * sin(q[1]), -self.l * cos(q[1])))
        ctx.circle(v2(q[0] + self.l * sin(q[1]), -self.l * cos(q[1])), 0.1)
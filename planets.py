from simulation import Sim
from context import Context
from math import sin, cos, tan, pi
from vector import v2

G = 1
au = 1
yr = 1

# q = (r, theta)
class planet(Sim):
    def setParams(self):
        self.M = 1

    def setd2s(self):
        self.d2_q = (
            self.d_q[1] * self.d_q[1] * self.q[0] - self.M * G / (self.q[0] * self.q[0]),
            -2 * self.d_q[1] * self.d_q[0] / self.q[0]
        )

    def guiEditables(self) -> bool:
        dsedited = self.defaultSliders(["r_0", "dr_0", "theta_0", "omega_0"], [(0.0, 2.0 * au), (-10.0, 10.0), (-pi, pi), (-20.0 / yr, 20.0 / yr)])
        M = self.autoslider("M", 0.0, 10.0)
        return any((dsedited, M))

    def displayFrame(self, ctx: Context, q, d_q, d2_q):
        ctx.col = (200, 200, 200)
        ctx.line(v2(0, 0), v2(-1.0 * au, 0))
        ctx.col = (255, 255, 255)
        ctx.circle(v2(), 0.01 * au)
        r = q[0]
        t = q[1]
        ctx.circle(v2(-r * cos(t), -r * sin(t)), 0.01 * au)

if __name__ == "__main__":
    import main
    main.simulate(planet(float, 0, (au, 0.0), (1, 0), (0, 0)), "Planet", v2(), 5 * au)
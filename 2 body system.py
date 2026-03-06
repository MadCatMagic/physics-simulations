from simulation import Sim
from context import Context
from vector import v2

G = 1

# q = (r, theta)
class planet(Sim):
    def setParams(self):
        self.M1 = 1
        self.M2 = 2
        self.followCOM = False
        self.showArrows = True

    def setd2s(self):
        f = G * self.M1 * self.M2 / (self.q[1] - self.q[0]).length() ** 2 * (self.q[1] - self.q[0]).normalise()
        self.d2_q = (
            f / self.M1,
            v2()-f / self.M2
        )

    def guiEditables(self) -> bool:
        #dsedited = self.defaultSliders(["r_0", "dr_0", "theta_0", "omega_0"], [(0.0, 2.0), (-10.0, 10.0), (-pi, pi), (-20.0 / yr, 20.0 / yr)])
        M1 = self.autoslider("M1", 0.0, 10.0)
        M2 = self.autoslider("M2", 0.0, 10.0)
        _ = self.autocheckbox("followCOM")
        _ = self.autocheckbox("showArrows")
        if self.button("EXPLODE"):
            self.M2 *= 0.5
        return any((M1, M2))

    def displayFrame(self, ctx: Context, q, d_q, d2_q):
        
        COM: v2 = (self.q[0] * self.M1 + self.q[1] * self.M2) / (self.M1 + self.M2)
        if not self.followCOM:
            ctx.col = (50, 50, 50)
            ctx.line(v2(0, 0), v2(-1.0, 0))
            COM = v2(0)

        ctx.col = (255, 255, 255)
        ctx.circle(q[0] - COM, 0.01)
        ctx.circle(q[1] - COM, 0.01)

        if self.showArrows:
            ctx.col = (200, 30, 30)
            ctx.line(q[0] - COM, q[0] - COM + d_q[0])
            ctx.line(q[1] - COM, q[1] - COM + d_q[1])

        first = max(len(self.h_Q) - 1 - 400, 0)
        if self.followCOM:
            ctx.col = (150, 150, 150)
            for i in range(first, len(self.h_Q) - 1):
                COMthen = (self.h_Q[i][0] * self.M1 + self.h_Q[i][1] * self.M2) / (self.M1 + self.M2)
                ctx.line(self.h_Q[i][0] - COMthen, self.h_Q[i+1][0] - COMthen)
                COMthen = (self.h_Q[i + 1][0] * self.M1 + self.h_Q[i + 1][1] * self.M2) / (self.M1 + self.M2)
                ctx.line(self.h_Q[i][1] - COMthen, self.h_Q[i+1][1] - COMthen)

            ctx.col = (50, 50, 50)
        else:
            ctx.col = (150, 150, 150)
        for i in range(first, len(self.h_Q) - 1):
            ctx.line(self.h_Q[i][0] - COM, self.h_Q[i+1][0] - COM)
            ctx.line(self.h_Q[i][1] - COM, self.h_Q[i+1][1] - COM)

if __name__ == "__main__": # v^2/r=GMm/r^2
    import main
    r0 = 0.3
    vel = 1 / (3 * r0 ** 0.5)
    main.simulate(planet(v2, 0, 
                         (v2(r0 * 2, 0), v2(-r0, 0)), 
                         (v2(0, vel * 2), v2(0, -vel))
        ), "2-body system", v2(), 8, 0.03, 6)
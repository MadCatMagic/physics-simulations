from simulation import Sim
from context import Context
from vector import v2
from math import sin, cos, pi

# q = (theta1, theta2)
class waveEquation(Sim):
    def setParams(self):
        self.c = 1
        self.gamma = 0.5

    def setd2s(self):
        N = len(self.q)
        q = lambda i: self.q[i] if 0 <= i < N else 0
        self.d2_q = (
            -self.c * N * (-q(i - 1) + 2 * q(i) - q(i + 1)) -self.gamma * self.d_q[i]
            for i in range(N)
        )

    def guiEditables(self) -> bool:
        #dsedited = self.defaultSliders(["c", "omega_1,0", "theta_2,0", "omega_2,0"], [(0.1, 5)])
        self.autoslider("c", 5, 50.0)
        self.autoslider("gamma", 0.01, 1)
        return self.button("Reset")

    def displayFrame(self, ctx: Context, q, d_q, d2_q):
        ctx.col = (200, 200, 200)
        ctx.line(v2(-2, 0), v2(2, 0))
        ctx.col = (255, 255, 255)
        
        scale = lambda x: x / len(q) * 4 - 2
        for i, y in enumerate(q):
            ctx.line(v2(scale(i), 0), v2(scale(i), y))
            #ctx.circle(v2(scale(i), y), 0.01)

    def onClick(self, pos: v2, button: int):
        if -2 < pos.x < 2:
            index = int((pos.x + 2) / 4 * len(self.q))
            summands = [0.0 for _ in self.q]
            for i in range(max(0, index - 10), min(len(self.q), index + 10)):
                summands[i] += cos((i - index) / 20 * pi) * (-(button * 2 - 1))

            self.q = tuple(q + s for q, s in zip(self.q, summands))

if __name__ == "__main__": # v^2/r=GMm/r^2
    import main
    N = 200
    initialQ = [(sin(i / 20 * pi) if 80 < i < 100 else 0) for i in range(200)]
    initialdQ = [0 for _ in range(200)]
    main.simulate(waveEquation(float, 0, 
            tuple(initialQ), 
            tuple(initialdQ)
        ), "Wave equation", v2(), 6, 1 / 60, 2)
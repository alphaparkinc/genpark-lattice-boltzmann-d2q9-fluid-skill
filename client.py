class LatticeBoltzmannD2Q9:
    """
    2D 9-velocity (D2Q9) Lattice Boltzmann Method (LBM).
    BGK single-relaxation-time collision and streaming step.
    """
    C = [(0,0), (1,0), (0,1), (-1,0), (0,-1), (1,1), (-1,1), (-1,-1), (1,-1)]
    W = [4/9, 1/9, 1/9, 1/9, 1/9, 1/36, 1/36, 1/36, 1/36]

    def __init__(self, nx=8, ny=8, tau=0.8):
        self.nx = nx
        self.ny = ny
        self.tau = tau
        self.f = [[[self.W[i] for i in range(9)] for _ in range(ny)] for _ in range(nx)]

    def step(self):
        rho = [[sum(self.f[x][y]) for y in range(self.ny)] for x in range(self.nx)]
        u_x = [[sum(self.f[x][y][i] * self.C[i][0] for i in range(9)) / rho[x][y] for y in range(self.ny)] for x in range(self.nx)]
        u_y = [[sum(self.f[x][y][i] * self.C[i][1] for i in range(9)) / rho[x][y] for y in range(self.ny)] for x in range(self.nx)]

        f_coll = [[[0.0]*9 for _ in range(self.ny)] for _ in range(self.nx)]
        for x in range(self.nx):
            for y in range(self.ny):
                r = rho[x][y]
                ux, uy = u_x[x][y], u_y[x][y]
                u_sq = ux*ux + uy*uy
                for i in range(9):
                    ci_u = self.C[i][0] * ux + self.C[i][1] * uy
                    feq = self.W[i] * r * (1.0 + 3.0*ci_u + 4.5*(ci_u**2) - 1.5*u_sq)
                    f_coll[x][y][i] = self.f[x][y][i] - (self.f[x][y][i] - feq) / self.tau

        for x in range(self.nx):
            for y in range(self.ny):
                for i in range(9):
                    prev_x = (x - self.C[i][0]) % self.nx
                    prev_y = (y - self.C[i][1]) % self.ny
                    self.f[x][y][i] = f_coll[prev_x][prev_y][i]

        return rho, u_x, u_y

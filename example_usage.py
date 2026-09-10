from client import LatticeBoltzmannD2Q9

def main():
    print("=== Testing Lattice Boltzmann D2Q9 Fluid Simulator ===")
    lbm = LatticeBoltzmannD2Q9(nx=8, ny=8, tau=0.8)

    rho, ux, uy = lbm.step()
    print("Macro density at center (4, 4):", round(rho[4][4], 4))
    print("Macro velocity (ux, uy) at center:", (round(ux[4][4], 4), round(uy[4][4], 4)))

    assert len(rho) == 8
    assert abs(rho[4][4] - 1.0) < 1e-3
    print("=== All tests passed successfully! ===")

if __name__ == "__main__":
    main()

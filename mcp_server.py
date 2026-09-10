import sys
import json
from client import LatticeBoltzmannD2Q9

lbm = LatticeBoltzmannD2Q9(16, 16)

def handle_call(name, arguments):
    if name == "step":
        rho, ux, uy = lbm.step()
        return {"avg_density": sum(sum(r) for r in rho) / (16 * 16)}
    return {"error": f"Unknown tool: {name}"}

def main():
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            res = handle_call(req.get("name"), req.get("arguments", {}))
            print(json.dumps({"id": req.get("id"), "result": res}))
            sys.stdout.flush()
        except Exception as e:
            print(json.dumps({"error": str(e)}))
            sys.stdout.flush()

if __name__ == "__main__":
    main()

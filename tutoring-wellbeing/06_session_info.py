"""Save seed, package versions and platform info (protocol §9)."""
import os
import platform
import sys
from importlib.metadata import version

HERE = os.path.dirname(os.path.abspath(__file__))
pkgs = ["numpy", "pandas", "scipy", "statsmodels", "pyreadstat", "pyarrow", "matplotlib"]
lines = [f"python {sys.version.split()[0]}", f"platform {platform.platform()}",
         "seed 20221 (+ system index, one stream per system)", "MI: PMM, M = 20, 20 iterations, k = 5 donors"]
lines += [f"{p} {version(p)}" for p in pkgs]
open(os.path.join(HERE, "results", "session_info.txt"), "w").write("\n".join(lines) + "\n")
print("\n".join(lines))

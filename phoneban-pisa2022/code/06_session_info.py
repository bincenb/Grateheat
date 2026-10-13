"""Record seed, package versions and machine info for reproducibility."""
import platform
import sys
from importlib.metadata import version

pk = ["numpy", "pandas", "scipy", "statsmodels", "patsy", "pyreadstat", "matplotlib"]
lines = [f"python {sys.version.split()[0]}", f"platform {platform.platform()}",
         "imputation seed 20221 (code/03_impute.py), M = 20, 15 iterations, PMM k = 5",
         "raw-data checksums: data_raw/SHA256SUMS"]
lines += [f"{p} {version(p)}" for p in pk]
open("output/session_info.txt", "w").write("\n".join(lines) + "\n")
print("\n".join(lines))

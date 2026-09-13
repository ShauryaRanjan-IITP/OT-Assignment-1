"""Small regression checks for the assignment implementations."""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def run_script(filename):
    result = subprocess.run(
        [sys.executable, str(ROOT / filename)],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        print(result.stdout)
        print(result.stderr)
        raise SystemExit(f"{filename} failed with exit code {result.returncode}")
    return result.stdout


def main():
    big_m = run_script("big_m_stigler.py")
    transportation = run_script("transportation_vam_modi_final.py")

    assert "Minimum daily cost  = $0.10866228" in big_m
    assert "Minimum annual cost = $39.6617" in big_m
    assert "Maximum artificial-variable value: 0.0" in big_m
    assert "Minimum transportation cost = 715" in transportation
    assert "Initial transportation cost = 725" in transportation

    print("Big-M implementation : PASS")
    print("VAM + MODI           : PASS")
    print("All regression tests : PASS")


if __name__ == "__main__":
    main()

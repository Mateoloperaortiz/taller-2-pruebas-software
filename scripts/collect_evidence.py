"""Ejecuta los pasos 6 a 10 y conserva salidas auténticas, incluso fallas esperadas."""

import json
import os
import platform
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "evidencias"


def main() -> None:
    OUTPUT.mkdir(exist_ok=True)
    runs = [
        ("paso06_unit_real", ["test_unit_real_api.py"], False, 0),
        ("paso06_integration_real", ["test_integration_real_api.py"], False, 0),
        ("paso07_unit_falla", ["test_unit_real_api.py"], True, 1),
        ("paso07_integration_falla", ["test_integration_real_api.py"], True, 1),
        ("paso09_stub", ["test_unit_with_stub.py"], True, 0),
        ("paso10_fake", ["test_integration_with_fake.py"], True, 0),
        ("suite_sin_red", ["-m", "not external"], True, 0),
    ]
    summary = {
        "executed_at_utc": datetime.now(timezone.utc).isoformat(),
        "python": platform.python_version(),
        "platform": platform.platform(),
        "runs": [],
    }
    for name, targets, broken, expected in runs:
        env = os.environ.copy()
        env["SIMULATE_USER_API_FAILURE"] = "1" if broken else "0"
        command = [sys.executable, "-m", "pytest", *targets, "-v", "--color=no"]
        result = subprocess.run(
            command, cwd=ROOT, env=env, text=True, capture_output=True, timeout=90
        )
        transcript = (
            f"Fecha UTC: {summary['executed_at_utc']}\n"
            f"Comando: python -m pytest {' '.join(targets)} -v --color=no\n"
            f"SIMULATE_USER_API_FAILURE={env['SIMULATE_USER_API_FAILURE']}\n"
            f"Código de salida: {result.returncode}; esperado: {expected}\n\n"
            + result.stdout + result.stderr
        )
        (OUTPUT / f"{name}.txt").write_text(
            "\n".join(line.rstrip() for line in transcript.splitlines()) + "\n",
            encoding="utf-8",
        )
        summary["runs"].append({
            "name": name, "exit_code": result.returncode, "expected_exit_code": expected
        })
        print(f"{name}: exit={result.returncode}, esperado={expected}", flush=True)
    (OUTPUT / "resumen.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    if any(run["exit_code"] != run["expected_exit_code"] for run in summary["runs"]):
        raise SystemExit("Al menos una ejecución difiere del resultado esperado")


if __name__ == "__main__":
    main()

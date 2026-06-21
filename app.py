from flask import Flask, render_template_string
import subprocess, sys
from pathlib import Path

app = Flask(__name__)

PAGE = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <title>tidex — Smoke Test</title>
  <style>body{font-family:system-ui,Segoe UI,Roboto,Arial;margin:2rem;} pre{background:#f6f8fa;padding:1rem;border-radius:6px;overflow:auto}</style>
</head>
<body>
  <h1>tidex — Smoke Test</h1>
  <p>Status: <strong>{{ status }}</strong></p>
  <pre>{{ output }}</pre>
</body>
</html>
"""

ROOT = Path(__file__).resolve().parents[0]
SCRIPT = ROOT / "scripts" / "run_mvp_smoke_test.py"


def run_smoke():
    # Run the existing script and capture stdout/stderr
    if not SCRIPT.exists():
        return "ERROR", f"Smoke test script not found: {SCRIPT}\nRun the app from the repository root."

    try:
        proc = subprocess.run([sys.executable, str(SCRIPT)],
                              capture_output=True, text=True, check=True)
        return "PASS", proc.stdout
    except subprocess.CalledProcessError as e:
        out = (e.stdout or "") + ("\n--- STDERR ---\n" + (e.stderr or ""))
        return "FAIL", out


@app.route("/")
def index():
    status, output = run_smoke()
    return render_template_string(PAGE, status=status, output=output)


if __name__ == "__main__":
    # Listen only on localhost for development
    app.run(host="127.0.0.1", port=5000, debug=False)

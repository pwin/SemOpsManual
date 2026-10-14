"""Run a command with no Java runtime visible, so HermiT cannot start.

    python scripts/without_java.py ontology-quality-suite ontology --ontology ...

Removes every PATH entry holding a `java` executable and unsets JAVA_HOME, then
runs the command. Otherwise whether the DL reasoner runs depends on the hash seed (Chapter 14
§14.4); this takes Java away as well, to show that a missing Java gives a different message.
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path

env = dict(os.environ)
env.pop("JAVA_HOME", None)
exe = "java.exe" if os.name == "nt" else "java"
keep = [d for d in env.get("PATH", "").split(os.pathsep) if d and not (Path(d) / exe).is_file()]
env["PATH"] = os.pathsep.join(keep)
print(f"without_java: java on PATH now: {shutil.which('java', path=env['PATH']) or 'none'}", flush=True)
cmd = sys.argv[1:]
cmd[0] = shutil.which(cmd[0], path=env["PATH"]) or cmd[0]
sys.exit(subprocess.run(cmd, env=env).returncode)

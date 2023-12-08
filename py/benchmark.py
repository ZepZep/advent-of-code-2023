from glob import glob
from importlib.machinery import SourceFileLoader
from pathlib import Path
import sys

to_load = [
    (Path(path).with_suffix("").name, path)
    for path in sorted(glob("task*.py"))
    if not path.endswith("task.py")
]

tasks = [ SourceFileLoader(name, path).load_module() for name, path in to_load]

n = 50
if len(sys.argv) > 1:
    n = int(sys.argv[1])
tasks[0].task.benchmark(n, header=True)
for task_module in tasks[1:]:
    task_module.task.benchmark(n, header=False)

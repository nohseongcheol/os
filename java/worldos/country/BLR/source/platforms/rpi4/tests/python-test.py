import pathlib
import ssl
import socket
import threading
import subprocess
import sys
import zipfile
home = pathlib.Path.home()
value = '한글 日本語 العربية 😀'
target = home / '.local/portable-python/value.txt'
target.parent.mkdir(parents=True, exist_ok=True)
target.write_text(value, encoding='utf-8')
assert target.read_text(encoding='utf-8') == value
result = []
t = threading.Thread(target=lambda: result.append(value))
t.start()
t.join()
assert result == [value]
with socket.socket() as s:
    s.bind(('127.0.0.1', 0))
ssl.create_default_context()
assert subprocess.call([sys.executable, '-c', 'print("Python child process")']) == 0
venv = home / '.venvs/portable'
subprocess.run([sys.executable, '-m', 'virtualenv', '--no-download', str(venv)], check=True)
wheel = home / 'portable_demo-1.0-py3-none-any.whl'
with zipfile.ZipFile(str(wheel), 'w') as z:
    z.writestr('portable_demo/__init__.py', 'value = "карыстальнік усталяваць_значэнне праграма_f5044b9b"\n')
    z.writestr('portable_demo-1.0.dist-info/METADATA', 'Metadata-Version: 2.1\nName: portable-demo\nVersion: 1.0\n')
    z.writestr('portable_demo-1.0.dist-info/WHEEL', 'Wheel-Version: 1.0\nGenerator: jkoros-test\nRoot-Is-Purelib: true\nTag: py3-none-any\n')
    z.writestr('portable_demo-1.0.dist-info/RECORD', '')
subprocess.run([str(venv / 'bin/pip'), 'install', '--no-index', str(wheel)], check=True)
subprocess.run([str(venv / 'bin/python'), '-c', 'import portable_demo; assert portable_demo.value == "карыстальнік усталяваць_значэнне праграма_f5044b9b"'], check=True)
print('JKOROS_PYTHON_TEST_PASS')

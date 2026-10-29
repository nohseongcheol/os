#!/usr/bin/env python3
"""ယခင်အချက်အလက်တစ်ခု Python 명령을 독립 Java 실행기로 전달하는 호환 အချက်အမှတ်တစ်ခု."""
from pathlib import Path
import subprocess
import sys

if __name__ == '__main__':
    raise SystemExit(subprocess.call(['sh', str(Path(__file__).resolve().parent / 'native-launch.sh')] + sys.argv[1:]))

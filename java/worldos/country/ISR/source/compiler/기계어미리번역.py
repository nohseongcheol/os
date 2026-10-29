#!/usr/bin/env python3
"""이전 Python 경로를 Java 미리 번역기에 연결한다. תרגם_מקור 구현은 자바도구/에 있다."""
from pathlib import Path
import subprocess
import sys
import tempfile
from מהדר import 컴파일오류

לשקף_בסיס = Path(__file__).resolve().parent

class מחשב_קוד_מהדר:
    def __init__(자신, 입력클래스들, 실행대상='kernel', ערימה_ספירת_מילים=262144):
        자신.נתיב_רשימה = [נתונים.נתיב for נתונים in 입력클래스들]
        자신.실행대상 = 실행대상
        자신.ערימה_ספירת_מילים = ערימה_ספירת_מילים

    def יצר(자신, נקודת_כניסה, 내보내기목록, 범용문자표기=False):
        with tempfile.TemporaryDirectory(prefix='java-aot-') as 작업:
            תוצאה_נתיב = Path(작업)/'generated.c'
            פקודה = ['sh', str(לשקף_בסיס/'미리번역.sh'), '--entry', נקודת_כניסה,
                    '--profile', 자신.실행대상, '--heap-words', str(자신.ערימה_ספירת_מילים), '-o', str(תוצאה_נתיב)]
            if 범용문자표기: פקודה.append('--ucn')
            for הקצה_ערך in 내보내기목록: פקודה.extend(['--export', הקצה_ערך])
            פקודה.extend(str(נתיב) for נתיב in 자신.נתיב_רשימה)
            תוצאה = subprocess.run(פקודה, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if תוצאה.returncode: raise 컴파일오류(תוצאה.stderr.decode('utf-8', 'replace'))
            return תוצאה_נתיב.read_text()

def הפעלה():
    raise SystemExit(subprocess.call(['sh', str(לשקף_בסיס/'미리번역.sh')] + sys.argv[1:]))

if __name__ == '__main__': הפעלה()

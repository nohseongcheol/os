#!/usr/bin/env python3
"""이전 Python 경로를 Java 미리 번역기에 연결한다. Аудару_көз 구현은 자바도구/에 있다."""
from pathlib import Path
import subprocess
import sys
import tempfile
from 컴파일러 import құрастыру_қатесі

жоба_түбір = Path(__file__).resolve().parent

class 기계어번역기:
    def __init__(자신, 입력클래스들, 실행대상='kernel', 동적기억낱말수=262144):
        자신.жол_Тізім_4d1a5003 = [деректер.Жол_2 for деректер in 입력클래스들]
        자신.실행대상 = 실행대상
        자신.동적기억낱말수 = 동적기억낱말수

    def жасау(자신, енгізу_ұпай, 내보내기목록, 범용문자표기=False):
        with tempfile.TemporaryDirectory(prefix='java-aot-') as 작업:
            өлшем_жол = Path(작업)/'generated.c'
            Команда = ['sh', str(жоба_түбір/'미리번역.sh'), '--entry', енгізу_ұпай,
                    '--profile', 자신.실행대상, '--heap-words', str(자신.동적기억낱말수), '-o', str(өлшем_жол)]
            if 범용문자표기: Команда.append('--ucn')
            for белгілеу_мән in 내보내기목록: Команда.extend(['--export', белгілеу_мән])
            Команда.extend(str(Жол_2) for Жол_2 in 자신.жол_Тізім_4d1a5003)
            НӘТИЖЕ = subprocess.run(Команда, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if НӘТИЖЕ.returncode: raise құрастыру_қатесі(НӘТИЖЕ.stderr.decode('utf-8', 'replace'))
            return өлшем_жол.read_text()

def Орындау_2():
    raise SystemExit(subprocess.call(['sh', str(жоба_түбір/'미리번역.sh')] + sys.argv[1:]))

if __name__ == '__main__': Орындау_2()

#!/usr/bin/env python3
"""이전 Python 경로를 Java 미리 번역기에 연결한다. translēt_avots 구현은 자바도구/에 있다."""
from pathlib import Path
import subprocess
import sys
import tempfile
from kompilators import kompilēšanas_kļūda

Project_sakne = Path(__file__).resolve().parent

class mašīna_CODE_kompilators:
    def __init__(자신, 입력클래스들, 실행대상='kernel', kaudze_Word_COUNT=262144):
        자신.ceļš_Saraksts = [dati.CEĻŠ for dati in 입력클래스들]
        자신.실행대상 = 실행대상
        자신.kaudze_Word_COUNT = kaudze_Word_COUNT

    def ģenerēt(자신, ieejas_punkts, 내보내기목록, 범용문자표기=False):
        with tempfile.TemporaryDirectory(prefix='java-aot-') as 작업:
            mērs_ceļš = Path(작업)/'generated.c'
            Komanda = ['sh', str(Project_sakne/'미리번역.sh'), '--entry', ieejas_punkts,
                    '--profile', 자신.실행대상, '--heap-words', str(자신.kaudze_Word_COUNT), '-o', str(mērs_ceļš)]
            if 범용문자표기: Komanda.append('--ucn')
            for nodot_VALUE in 내보내기목록: Komanda.extend(['--export', nodot_VALUE])
            Komanda.extend(str(CEĻŠ) for CEĻŠ in 자신.ceļš_Saraksts)
            mērs = subprocess.run(Komanda, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if mērs.returncode: raise kompilēšanas_kļūda(mērs.stderr.decode('utf-8', 'replace'))
            return mērs_ceļš.read_text()

def Palaist():
    raise SystemExit(subprocess.call(['sh', str(Project_sakne/'미리번역.sh')] + sys.argv[1:]))

if __name__ == '__main__': Palaist()

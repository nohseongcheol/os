#!/usr/bin/env python3
"""Forrige_vare Python 경로를 Java 미리 번역기에 연결한다. OVERSETT_kilde 구현은 자바도구/에 있다."""
from pathlib import Path
import subprocess
import sys
import tempfile
from kompilator import 컴파일오류

speile_rot = Path(__file__).resolve().parent

class maskin_KODE_kompilator:
    def __init__(자신, 입력클래스들, kjøring_mål='kernel', heap_ord_ANTALL=262144):
        자신.bane_Liste = [data.Sti for data in 입력클래스들]
        자신.kjøring_mål = kjøring_mål
        자신.heap_ord_ANTALL = heap_ord_ANTALL

    def generere(자신, inngangspunkt, 내보내기목록, 범용문자표기=False):
        with tempfile.TemporaryDirectory(prefix='java-aot-') as 작업:
            KR_bane = Path(작업)/'generated.c'
            Kommando = ['sh', str(speile_rot/'미리번역.sh'), '--entry', inngangspunkt,
                    '--profile', 자신.kjøring_mål, '--heap-words', str(자신.heap_ord_ANTALL), '-o', str(KR_bane)]
            if 범용문자표기: Kommando.append('--ucn')
            for overdra_VERDI in 내보내기목록: Kommando.extend(['--export', overdra_VERDI])
            Kommando.extend(str(Sti) for Sti in 자신.bane_Liste)
            KR = subprocess.run(Kommando, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if KR.returncode: raise 컴파일오류(KR.stderr.decode('utf-8', 'replace'))
            return KR_bane.read_text()

def Kjør_2():
    raise SystemExit(subprocess.call(['sh', str(speile_rot/'미리번역.sh')] + sys.argv[1:]))

if __name__ == '__main__': Kjør_2()

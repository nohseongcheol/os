#!/usr/bin/env python3
"""이전 Python 경로를 Java 미리 번역기에 연결한다. TRANSLATE_sumber 구현은 자바도구/에 있다."""
from pathlib import Path
import subprocess
import sys
import tempfile
from 컴파일러 import kesalahan_kompilasi

Tugas_akar = Path(__file__).resolve().parent

class 기계어번역기:
    def __init__(자신, 입력클래스들, 실행대상='kernel', 동적기억낱말수=262144):
        자신.jalur_Daftar = [data.jalur for data in 입력클래스들]
        자신.실행대상 = 실행대상
        자신.동적기억낱말수 = 동적기억낱말수

    def buat(자신, entri_p, 내보내기목록, 범용문자표기=False):
        with tempfile.TemporaryDirectory(prefix='java-aot-') as 작업:
            KR_jalur = Path(작업)/'generated.c'
            perintah = ['sh', str(Tugas_akar/'미리번역.sh'), '--entry', entri_p,
                    '--profile', 자신.실행대상, '--heap-words', str(자신.동적기억낱말수), '-o', str(KR_jalur)]
            if 범용문자표기: perintah.append('--ucn')
            for Tugaskan_VALUE in 내보내기목록: perintah.extend(['--export', Tugaskan_VALUE])
            perintah.extend(str(jalur) for jalur in 자신.jalur_Daftar)
            hasil = subprocess.run(perintah, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if hasil.returncode: raise kesalahan_kompilasi(hasil.stderr.decode('utf-8', 'replace'))
            return KR_jalur.read_text()

def jalankan():
    raise SystemExit(subprocess.call(['sh', str(Tugas_akar/'미리번역.sh')] + sys.argv[1:]))

if __name__ == '__main__': jalankan()

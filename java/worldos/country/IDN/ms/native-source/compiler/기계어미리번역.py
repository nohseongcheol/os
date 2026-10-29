#!/usr/bin/env python3
"""이전 Python 경로를 Java 미리 번역기에 연결한다. Terjemah_sumber 구현은 자바도구/에 있다."""
from pathlib import Path
import subprocess
import sys
import tempfile
from 컴파일러 import ralat_kompilasi

projek_akar = Path(__file__).resolve().parent

class 기계어번역기:
    def __init__(자신, 입력클래스들, 실행대상='kernel', timbunan_Kiraan_Kata=262144):
        자신.laluan_Senarai = [data.LALUAN for data in 입력클래스들]
        자신.실행대상 = 실행대상
        자신.timbunan_Kiraan_Kata = timbunan_Kiraan_Kata

    def jana(자신, titik_permulaan, 내보내기목록, 범용문자표기=False):
        with tempfile.TemporaryDirectory(prefix='java-aot-') as 작업:
            ukuran_laluan = Path(작업)/'generated.c'
            Perintah = ['sh', str(projek_akar/'미리번역.sh'), '--entry', titik_permulaan,
                    '--profile', 자신.실행대상, '--heap-words', str(자신.timbunan_Kiraan_Kata), '-o', str(ukuran_laluan)]
            if 범용문자표기: Perintah.append('--ucn')
            for Tugaskan_VALUE in 내보내기목록: Perintah.extend(['--export', Tugaskan_VALUE])
            Perintah.extend(str(LALUAN) for LALUAN in 자신.laluan_Senarai)
            ukuran = subprocess.run(Perintah, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if ukuran.returncode: raise ralat_kompilasi(ukuran.stderr.decode('utf-8', 'replace'))
            return ukuran_laluan.read_text()

def Jalan():
    raise SystemExit(subprocess.call(['sh', str(projek_akar/'미리번역.sh')] + sys.argv[1:]))

if __name__ == '__main__': Jalan()

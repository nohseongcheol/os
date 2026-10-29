#!/usr/bin/env python3
"""tambah_entri Python 패키지 없이 Indonesia Java 메서드의 결과를 받는다."""
import argparse
import os
from pathlib import Path
import subprocess


def poin_kode_COUNT(Isi_VALUE, pustaka, Kelas_Direktori):
    hasil = subprocess.run(
        ['java', '-Dfile.encoding=UTF-8', '-cp',
         os.pathsep.join([str(pustaka), str(Kelas_Direktori)]), '문자명령', Isi_VALUE],
        check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        encoding='utf-8', timeout=60)
    return int(hasil.stdout.strip())


if __name__ == '__main__':
    인수해석 = argparse.ArgumentParser(description=__doc__)
    인수해석.add_argument('--jar', type=Path, default=Path('/opt/jkoros/lib/한국어자바.jar'))
    인수해석.add_argument('--classes', type=Path, default=Path(__file__).resolve().parent / 'classes')
    인수해석.add_argument('--text', default='한글 😀')
    argumen = 인수해석.parse_args()
    print('Python → Indonesia.자바.문자.poin_kode_COUNT:',
          poin_kode_COUNT(argumen.text, argumen.jar, argumen.classes))

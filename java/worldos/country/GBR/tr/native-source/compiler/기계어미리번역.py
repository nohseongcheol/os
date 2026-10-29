#!/usr/bin/env python3
"""Önceki_öğe Python 경로를 Java 미리 번역기에 연결한다. çevir_kaynak 구현은 자바도구/에 있다."""
from pathlib import Path
import subprocess
import sys
import tempfile
from derleyici import derleme_hatası

işlem_kök = Path(__file__).resolve().parent

class makine_KOD_derleyici:
    def __init__(자신, 입력클래스들, yürütme_hedef='kernel', yığın_Word_BAĞ_DEĞ_SAY=262144):
        자신.yol_Liste = [veri.yol for veri in 입력클래스들]
        자신.yürütme_hedef = yürütme_hedef
        자신.yığın_Word_BAĞ_DEĞ_SAY = yığın_Word_BAĞ_DEĞ_SAY

    def oluşturmak(자신, giriş_noktası, 내보내기목록, 범용문자표기=False):
        with tempfile.TemporaryDirectory(prefix='java-aot-') as 작업:
            KR_yol = Path(작업)/'generated.c'
            komut = ['sh', str(işlem_kök/'미리번역.sh'), '--entry', giriş_noktası,
                    '--profile', 자신.yürütme_hedef, '--heap-words', str(자신.yığın_Word_BAĞ_DEĞ_SAY), '-o', str(KR_yol)]
            if 범용문자표기: komut.append('--ucn')
            for Ata_değer in 내보내기목록: komut.extend(['--export', Ata_değer])
            komut.extend(str(yol) for yol in 자신.yol_Liste)
            sonuç = subprocess.run(komut, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if sonuç.returncode: raise derleme_hatası(sonuç.stderr.decode('utf-8', 'replace'))
            return KR_yol.read_text()

def çalıştır():
    raise SystemExit(subprocess.call(['sh', str(işlem_kök/'미리번역.sh')] + sys.argv[1:]))

if __name__ == '__main__': çalıştır()

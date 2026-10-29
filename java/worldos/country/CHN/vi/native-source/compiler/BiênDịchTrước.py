#!/usr/bin/env python3
"""phầnMụcTrướcĐó Python 경로를 Java 미리 번역기에 연결한다. dịchThuậtNguồn 구현은 CôngCụJava/에 있다."""
from pathlib import Path
import subprocess
import sys
import tempfile
from TrìnhBiênDịch import LỗiViệcBiênDịch

gốcCâyDựÁn = Path(__file__).resolve().parent

class TrìnhBiênDịchMãMáy:
    def __init__(giáTrịBảnThân, cácLớpĐầuVào, đốiĐíchViệcThựcThi='kernel', sốLượngTừVùngNhớĐộng=262144):
        giáTrịBảnThân.danhSáchĐườngDẫn = [DữLiệu.đườngDẫn for DữLiệu in cácLớpĐầuVào]
        giáTrịBảnThân.đốiĐíchViệcThựcThi = đốiĐíchViệcThựcThi
        giáTrịBảnThân.sốLượngTừVùngNhớĐộng = sốLượngTừVùngNhớĐộng

    def sinh(giáTrịBảnThân, điểmMục, cácMụcXuất, cáchKýHiệuKýTựPhổQuát=False):
        with tempfile.TemporaryDirectory(prefix='java-aot-') as TácVụ:
            đườngDẫnKếtQuả = Path(TácVụ)/'generated.c'
            lệnh = ['sh', str(gốcCâyDựÁn/'thờiGianCủaTrước.sh'), '--entry', điểmMục,
                    '--profile', giáTrịBảnThân.đốiĐíchViệcThựcThi, '--heap-words', str(giáTrịBảnThân.sốLượngTừVùngNhớĐộng), '-o', str(đườngDẫnKếtQuả)]
            if cáchKýHiệuKýTựPhổQuát: lệnh.append('--ucn')
            for giáTrịGán in cácMụcXuất: lệnh.extend(['--export', giáTrịGán])
            lệnh.extend(str(đườngDẫn) for đườngDẫn in giáTrịBảnThân.danhSáchĐườngDẫn)
            kếtQuả = subprocess.run(lệnh, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if kếtQuả.returncode: raise LỗiViệcBiênDịch(kếtQuả.stderr.decode('utf-8', 'replace'))
            return đườngDẫnKếtQuả.read_text()

def chạy():
    raise SystemExit(subprocess.call(['sh', str(gốcCâyDựÁn/'thờiGianCủaTrước.sh')] + sys.argv[1:]))

if __name__ == '__main__': chạy()

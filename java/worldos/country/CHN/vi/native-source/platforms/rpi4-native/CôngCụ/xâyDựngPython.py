"""고정한 공식 MicroPython 소스로 tựThân SVC용 EL0 실행기를 빌드한다."""
import hashlib
import os
from pathlib import Path
import subprocess
import tarfile

giáTrịPhiênBảnNgônNgữ = '1.24.1'
mãBămViệcThẩmĐịnh = 'a291173de1d680786a66dd2381805b6d134defaecea670a560dc7e7d8de540ad'


def tạoPython(đườngDẫnGốcCây, TrìnhBiênDịchC, côngCụTrìnhLiênKết):
    tên = 'micropython-' + giáTrịPhiênBảnNgônNgữ
    khoLưuTrữ = đườngDẫnGốcCây / 'vendor' / (tên + '.tar.gz')
    if not khoLưuTrữ.is_file() or hashlib.sha256(khoLưuTrữ.read_bytes()).hexdigest() != mãBămViệcThẩmĐịnh:
        raise SystemExit('MicroPython câyNguồn phươngThứcThiếu/tệpMãBăm 불일치: ' + str(khoLưuTrữ))
    dữLiệuNguyênBản = đườngDẫnGốcCây / 'build' / tên
    if not (dữLiệuNguyênBản / '.jkoros-source-sha256').is_file():
        with tarfile.open(str(khoLưuTrữ)) as góiGộpTAR:
            for thànhViên in góiGộpTAR.getmembers():
                đườngDẫn = Path(thànhViên.name)
                if đườngDẫn.is_absolute() or '..' in đườngDẫn.parts or đườngDẫn.parts[0] != tên:
                    raise SystemExit('안전하지 않은 câyNguồn đườngDẫn')
                if thànhViên.isfile() or thànhViên.isdir():
                    góiGộpTAR.extract(thànhViên, str(đườngDẫnGốcCây / 'build'))
        (dữLiệuNguyênBản / '.jkoros-source-sha256').write_text(mãBămViệcThẩmĐịnh + '\n')
    newlib = os.environ.get('NEWLIB_INCLUDE', '/usr/include/newlib')
    if not (Path(newlib) / 'stdio.h').is_file():
        raise SystemExit('libnewlib-dev 헤더 또는 NEWLIB_INCLUDE giáTrịCầnĐến')
    subprocess.check_call(['make', '-j2', 'CC=' + TrìnhBiênDịchC, 'LD=' + côngCụTrìnhLiênKết, 'NEWLIB_INCLUDE=' + newlib], cwd=str(đườngDẫnGốcCây / 'cầuNốiPython'))

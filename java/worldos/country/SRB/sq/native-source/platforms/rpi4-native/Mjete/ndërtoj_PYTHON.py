"""고정한 공식 MicroPython 소스로 자체 SVC용 EL0 실행기를 빌드한다."""
import hashlib
import os
from pathlib import Path
import subprocess
import tarfile

배포판 = '1.24.1'
miratim_hash = 'a291173de1d680786a66dd2381805b6d134defaecea670a560dc7e7d8de540ad'


def Krijo_PYTHON(rrënjë_shteg, 시언어번역기, 연결편집기):
    Emër = 'micropython-' + 배포판
    arkiv = rrënjë_shteg / 'vendor' / (Emër + '.tar.gz')
    if not arkiv.is_file() or hashlib.sha256(arkiv.read_bytes()).hexdigest() != miratim_hash:
        raise SystemExit('MicroPython burim_degëzim 없음/hash_skedar 불일치: ' + str(arkiv))
    원본자료 = rrënjë_shteg / 'build' / Emër
    if not (원본자료 / '.jkoros-source-sha256').is_file():
        with tarfile.open(str(arkiv)) as 타르꾸러미:
            for anëtar in 타르꾸러미.getmembers():
                POZICIONI = Path(anëtar.name)
                if POZICIONI.is_absolute() or '..' in POZICIONI.parts or POZICIONI.parts[0] != Emër:
                    raise SystemExit('안전하지 않은 burim_degëzim POZICIONI')
                if anëtar.isfile() or anëtar.isdir():
                    타르꾸러미.extract(anëtar, str(rrënjë_shteg / 'build'))
        (원본자료 / '.jkoros-source-sha256').write_text(miratim_hash + '\n')
    뉴리브포함경로 = os.environ.get('NEWLIB_INCLUDE', '/usr/include/newlib')
    if not (Path(뉴리브포함경로) / 'stdio.h').is_file():
        raise SystemExit('libnewlib-dev 헤더 또는 NEWLIB_INCLUDE 필요')
    subprocess.check_call(['make', '-j2', 'CC=' + 시언어번역기, 'LD=' + 연결편집기, 'NEWLIB_INCLUDE=' + 뉴리브포함경로], cwd=str(rrënjë_shteg / 'PYTHON_urë'))

"""고정한 공식 MicroPython 소스로 자체 SVC용 EL0 실행기를 빌드한다."""
import hashlib
import os
from pathlib import Path
import subprocess
import tarfile

uitgawe_VALUE = '1.24.1'
validering_huts = 'a291173de1d680786a66dd2381805b6d134defaecea670a560dc7e7d8de540ad'


def Skep_PYTHON(wortel_pad, 시언어번역기, 연결편집기):
    Naam = 'micropython-' + uitgawe_VALUE
    Argief = wortel_pad / 'vendor' / (Naam + '.tar.gz')
    if not Argief.is_file() or hashlib.sha256(Argief.read_bytes()).hexdigest() != validering_huts:
        raise SystemExit('MicroPython bron_boom 없음/huts_lêer 불일치: ' + str(Argief))
    원본자료 = wortel_pad / 'build' / Naam
    if not (원본자료 / '.jkoros-source-sha256').is_file():
        with tarfile.open(str(Argief)) as 타르꾸러미:
            for lid in 타르꾸러미.getmembers():
                Pad = Path(lid.name)
                if Pad.is_absolute() or '..' in Pad.parts or Pad.parts[0] != Naam:
                    raise SystemExit('안전하지 않은 bron_boom Pad')
                if lid.isfile() or lid.isdir():
                    타르꾸러미.extract(lid, str(wortel_pad / 'build'))
        (원본자료 / '.jkoros-source-sha256').write_text(validering_huts + '\n')
    뉴리브포함경로 = os.environ.get('NEWLIB_INCLUDE', '/usr/include/newlib')
    if not (Path(뉴리브포함경로) / 'stdio.h').is_file():
        raise SystemExit('libnewlib-dev 헤더 또는 NEWLIB_INCLUDE 필요')
    subprocess.check_call(['make', '-j2', 'CC=' + 시언어번역기, 'LD=' + 연결편집기, 'NEWLIB_INCLUDE=' + 뉴리브포함경로], cwd=str(wortel_pad / 'PYTHON_brug'))

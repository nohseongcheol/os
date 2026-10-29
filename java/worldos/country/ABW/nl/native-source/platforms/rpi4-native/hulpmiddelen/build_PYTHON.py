"""고정한 공식 MicroPython 소스로 Eigen SVC용 EL0 실행기를 빌드한다."""
import hashlib
import os
from pathlib import Path
import subprocess
import tarfile

editie_WAARDE = '1.24.1'
validatie_hash = 'a291173de1d680786a66dd2381805b6d134defaecea670a560dc7e7d8de540ad'


def maken_PYTHON(wortel_pad, C_compiler, linker_hulpmiddel):
    Naam = 'micropython-' + editie_WAARDE
    Archief = wortel_pad / 'vendor' / (Naam + '.tar.gz')
    if not Archief.is_file() or hashlib.sha256(Archief.read_bytes()).hexdigest() != validatie_hash:
        raise SystemExit('MicroPython bron_structuur 없음/hash_Bestand 불일치: ' + str(Archief))
    원본자료 = wortel_pad / 'build' / Naam
    if not (원본자료 / '.jkoros-source-sha256').is_file():
        with tarfile.open(str(Archief)) as 타르꾸러미:
            for lid in 타르꾸러미.getmembers():
                pad = Path(lid.name)
                if pad.is_absolute() or '..' in pad.parts or pad.parts[0] != Naam:
                    raise SystemExit('안전하지 않은 bron_structuur pad')
                if lid.isfile() or lid.isdir():
                    타르꾸러미.extract(lid, str(wortel_pad / 'build'))
        (원본자료 / '.jkoros-source-sha256').write_text(validatie_hash + '\n')
    뉴리브포함경로 = os.environ.get('NEWLIB_INCLUDE', '/usr/include/newlib')
    if not (Path(뉴리브포함경로) / 'stdio.h').is_file():
        raise SystemExit('libnewlib-dev 헤더 또는 NEWLIB_INCLUDE 필요')
    subprocess.check_call(['make', '-j2', 'CC=' + C_compiler, 'LD=' + linker_hulpmiddel, 'NEWLIB_INCLUDE=' + 뉴리브포함경로], cwd=str(wortel_pad / 'PYTHON_brug'))

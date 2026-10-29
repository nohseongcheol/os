"""고정한 공식 MicroPython 소스로 saját SVC용 EL0 실행기를 빌드한다."""
import hashlib
import os
from pathlib import Path
import subprocess
import tarfile

kiadás_ÉRTÉK = '1.24.1'
ellenőrzés_kivonat = 'a291173de1d680786a66dd2381805b6d134defaecea670a560dc7e7d8de540ad'


def készít_PYTHON(gyök_útvonal, C_fordítóprogram, kapcsolószerkesztő_eszköz):
    Név = 'micropython-' + kiadás_ÉRTÉK
    archív = gyök_útvonal / 'vendor' / (Név + '.tar.gz')
    if not archív.is_file() or hashlib.sha256(archív.read_bytes()).hexdigest() != ellenőrzés_kivonat:
        raise SystemExit('MicroPython forrás_fa 없음/kivonat_Fájl 불일치: ' + str(archív))
    원본자료 = gyök_útvonal / 'build' / Név
    if not (원본자료 / '.jkoros-source-sha256').is_file():
        with tarfile.open(str(archív)) as 타르꾸러미:
            for tag in 타르꾸러미.getmembers():
                ÚTVONAL = Path(tag.name)
                if ÚTVONAL.is_absolute() or '..' in ÚTVONAL.parts or ÚTVONAL.parts[0] != Név:
                    raise SystemExit('안전하지 않은 forrás_fa ÚTVONAL')
                if tag.isfile() or tag.isdir():
                    타르꾸러미.extract(tag, str(gyök_útvonal / 'build'))
        (원본자료 / '.jkoros-source-sha256').write_text(ellenőrzés_kivonat + '\n')
    뉴리브포함경로 = os.environ.get('NEWLIB_INCLUDE', '/usr/include/newlib')
    if not (Path(뉴리브포함경로) / 'stdio.h').is_file():
        raise SystemExit('libnewlib-dev 헤더 또는 NEWLIB_INCLUDE 필요')
    subprocess.check_call(['make', '-j2', 'CC=' + C_fordítóprogram, 'LD=' + kapcsolószerkesztő_eszköz, 'NEWLIB_INCLUDE=' + 뉴리브포함경로], cwd=str(gyök_útvonal / 'PYTHON_híd'))

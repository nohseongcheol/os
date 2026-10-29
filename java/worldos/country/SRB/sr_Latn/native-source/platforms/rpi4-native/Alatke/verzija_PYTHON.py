"""고정한 공식 MicroPython 소스로 자체 SVC용 EL0 실행기를 빌드한다."""
import hashlib
import os
from pathlib import Path
import subprocess
import tarfile

izdanje_VALUE = '1.24.1'
provera_valjanosti_heš = 'a291173de1d680786a66dd2381805b6d134defaecea670a560dc7e7d8de540ad'


def Create_PYTHON(koren_putanja, C_kompajler, 연결편집기):
    ime = 'micropython-' + izdanje_VALUE
    Arhiva = koren_putanja / 'vendor' / (ime + '.tar.gz')
    if not Arhiva.is_file() or hashlib.sha256(Arhiva.read_bytes()).hexdigest() != provera_valjanosti_heš:
        raise SystemExit('MicroPython izvor_stablo 없음/heš_Datoteka 불일치: ' + str(Arhiva))
    원본자료 = koren_putanja / 'build' / ime
    if not (원본자료 / '.jkoros-source-sha256').is_file():
        with tarfile.open(str(Arhiva)) as 타르꾸러미:
            for član in 타르꾸러미.getmembers():
                putanja = Path(član.name)
                if putanja.is_absolute() or '..' in putanja.parts or putanja.parts[0] != ime:
                    raise SystemExit('안전하지 않은 izvor_stablo putanja')
                if član.isfile() or član.isdir():
                    타르꾸러미.extract(član, str(koren_putanja / 'build'))
        (원본자료 / '.jkoros-source-sha256').write_text(provera_valjanosti_heš + '\n')
    뉴리브포함경로 = os.environ.get('NEWLIB_INCLUDE', '/usr/include/newlib')
    if not (Path(뉴리브포함경로) / 'stdio.h').is_file():
        raise SystemExit('libnewlib-dev 헤더 또는 NEWLIB_INCLUDE 필요')
    subprocess.check_call(['make', '-j2', 'CC=' + C_kompajler, 'LD=' + 연결편집기, 'NEWLIB_INCLUDE=' + 뉴리브포함경로], cwd=str(koren_putanja / 'PYTHON_most'))

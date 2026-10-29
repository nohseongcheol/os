"""고정한 공식 MicroPython 소스로 lastno SVC용 EL0 실행기를 빌드한다."""
import hashlib
import os
from pathlib import Path
import subprocess
import tarfile

izdaja_VALUE = '1.24.1'
preverjanje_veljavnosti_zgoščena_vrednost = 'a291173de1d680786a66dd2381805b6d134defaecea670a560dc7e7d8de540ad'


def Ustvari_PYTHON(koren_pot, C_prevajalnik, 연결편집기):
    Ime = 'micropython-' + izdaja_VALUE
    Arhiv = koren_pot / 'vendor' / (Ime + '.tar.gz')
    if not Arhiv.is_file() or hashlib.sha256(Arhiv.read_bytes()).hexdigest() != preverjanje_veljavnosti_zgoščena_vrednost:
        raise SystemExit('MicroPython vir_drevo 없음/zgoščena_vrednost_Datoteka 불일치: ' + str(Arhiv))
    원본자료 = koren_pot / 'build' / Ime
    if not (원본자료 / '.jkoros-source-sha256').is_file():
        with tarfile.open(str(Arhiv)) as 타르꾸러미:
            for član in 타르꾸러미.getmembers():
                POT = Path(član.name)
                if POT.is_absolute() or '..' in POT.parts or POT.parts[0] != Ime:
                    raise SystemExit('안전하지 않은 vir_drevo POT')
                if član.isfile() or član.isdir():
                    타르꾸러미.extract(član, str(koren_pot / 'build'))
        (원본자료 / '.jkoros-source-sha256').write_text(preverjanje_veljavnosti_zgoščena_vrednost + '\n')
    뉴리브포함경로 = os.environ.get('NEWLIB_INCLUDE', '/usr/include/newlib')
    if not (Path(뉴리브포함경로) / 'stdio.h').is_file():
        raise SystemExit('libnewlib-dev 헤더 또는 NEWLIB_INCLUDE 필요')
    subprocess.check_call(['make', '-j2', 'CC=' + C_prevajalnik, 'LD=' + 연결편집기, 'NEWLIB_INCLUDE=' + 뉴리브포함경로], cwd=str(koren_pot / 'PYTHON_most'))

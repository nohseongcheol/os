"""고정한 공식 MicroPython 소스로 propriu SVC용 EL0 실행기를 빌드한다."""
import hashlib
import os
from pathlib import Path
import subprocess
import tarfile

ediție_VALUE = '1.24.1'
validare_cod_hash = 'a291173de1d680786a66dd2381805b6d134defaecea670a560dc7e7d8de540ad'


def crea_PYTHON(rădăcină_cale, C_compilator, 연결편집기):
    Nume = 'micropython-' + ediție_VALUE
    Arhivă = rădăcină_cale / 'vendor' / (Nume + '.tar.gz')
    if not Arhivă.is_file() or hashlib.sha256(Arhivă.read_bytes()).hexdigest() != validare_cod_hash:
        raise SystemExit('MicroPython sursă_arborescență 없음/cod_hash_Fișier 불일치: ' + str(Arhivă))
    원본자료 = rădăcină_cale / 'build' / Nume
    if not (원본자료 / '.jkoros-source-sha256').is_file():
        with tarfile.open(str(Arhivă)) as 타르꾸러미:
            for membru in 타르꾸러미.getmembers():
                Cale = Path(membru.name)
                if Cale.is_absolute() or '..' in Cale.parts or Cale.parts[0] != Nume:
                    raise SystemExit('안전하지 않은 sursă_arborescență Cale')
                if membru.isfile() or membru.isdir():
                    타르꾸러미.extract(membru, str(rădăcină_cale / 'build'))
        (원본자료 / '.jkoros-source-sha256').write_text(validare_cod_hash + '\n')
    뉴리브포함경로 = os.environ.get('NEWLIB_INCLUDE', '/usr/include/newlib')
    if not (Path(뉴리브포함경로) / 'stdio.h').is_file():
        raise SystemExit('libnewlib-dev 헤더 또는 NEWLIB_INCLUDE 필요')
    subprocess.check_call(['make', '-j2', 'CC=' + C_compilator, 'LD=' + 연결편집기, 'NEWLIB_INCLUDE=' + 뉴리브포함경로], cwd=str(rădăcină_cale / 'PYTHON_punte'))

"""고정한 공식 MicroPython 소스로 자체 SVC용 EL0 실행기를 빌드한다."""
import hashlib
import os
from pathlib import Path
import subprocess
import tarfile

배포판 = '1.24.1'
provjera_raspršivanje = 'a291173de1d680786a66dd2381805b6d134defaecea670a560dc7e7d8de540ad'


def Create_PYTHON(koijen_put, 시언어번역기, 연결편집기):
    Naziv = 'micropython-' + 배포판
    Arhiva = koijen_put / 'vendor' / (Naziv + '.tar.gz')
    if not Arhiva.is_file() or hashlib.sha256(Arhiva.read_bytes()).hexdigest() != provjera_raspršivanje:
        raise SystemExit('MicroPython izvor_stablo 없음/raspršivanje_fajl 불일치: ' + str(Arhiva))
    원본자료 = koijen_put / 'build' / Naziv
    if not (원본자료 / '.jkoros-source-sha256').is_file():
        with tarfile.open(str(Arhiva)) as 타르꾸러미:
            for član in 타르꾸러미.getmembers():
                Putanja = Path(član.name)
                if Putanja.is_absolute() or '..' in Putanja.parts or Putanja.parts[0] != Naziv:
                    raise SystemExit('안전하지 않은 izvor_stablo Putanja')
                if član.isfile() or član.isdir():
                    타르꾸러미.extract(član, str(koijen_put / 'build'))
        (원본자료 / '.jkoros-source-sha256').write_text(provjera_raspršivanje + '\n')
    뉴리브포함경로 = os.environ.get('NEWLIB_INCLUDE', '/usr/include/newlib')
    if not (Path(뉴리브포함경로) / 'stdio.h').is_file():
        raise SystemExit('libnewlib-dev 헤더 또는 NEWLIB_INCLUDE 필요')
    subprocess.check_call(['make', '-j2', 'CC=' + 시언어번역기, 'LD=' + 연결편집기, 'NEWLIB_INCLUDE=' + 뉴리브포함경로], cwd=str(koijen_put / 'PYTHON_most'))

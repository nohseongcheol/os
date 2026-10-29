"""고정한 공식 MicroPython 소스로 vlastné SVC용 EL0 실행기를 빌드한다."""
import hashlib
import os
from pathlib import Path
import subprocess
import tarfile

vydanie_VALUE = '1.24.1'
overenie_hodnota_hash = 'a291173de1d680786a66dd2381805b6d134defaecea670a560dc7e7d8de540ad'


def Create_PYTHON(koreň_cesta, C_kompilátor, 연결편집기):
    Názov = 'micropython-' + vydanie_VALUE
    Archív = koreň_cesta / 'vendor' / (Názov + '.tar.gz')
    if not Archív.is_file() or hashlib.sha256(Archív.read_bytes()).hexdigest() != overenie_hodnota_hash:
        raise SystemExit('MicroPython zdroj_strom 없음/hodnota_hash_Súbor 불일치: ' + str(Archív))
    원본자료 = koreň_cesta / 'build' / Názov
    if not (원본자료 / '.jkoros-source-sha256').is_file():
        with tarfile.open(str(Archív)) as 타르꾸러미:
            for člen in 타르꾸러미.getmembers():
                Cesta = Path(člen.name)
                if Cesta.is_absolute() or '..' in Cesta.parts or Cesta.parts[0] != Názov:
                    raise SystemExit('안전하지 않은 zdroj_strom Cesta')
                if člen.isfile() or člen.isdir():
                    타르꾸러미.extract(člen, str(koreň_cesta / 'build'))
        (원본자료 / '.jkoros-source-sha256').write_text(overenie_hodnota_hash + '\n')
    뉴리브포함경로 = os.environ.get('NEWLIB_INCLUDE', '/usr/include/newlib')
    if not (Path(뉴리브포함경로) / 'stdio.h').is_file():
        raise SystemExit('libnewlib-dev 헤더 또는 NEWLIB_INCLUDE 필요')
    subprocess.check_call(['make', '-j2', 'CC=' + C_kompilátor, 'LD=' + 연결편집기, 'NEWLIB_INCLUDE=' + 뉴리브포함경로], cwd=str(koreň_cesta / 'PYTHON_most'))

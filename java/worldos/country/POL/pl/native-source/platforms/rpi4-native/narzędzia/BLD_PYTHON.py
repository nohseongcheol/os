"""고정한 공식 MicroPython 소스로 własny SVC용 EL0 실행기를 빌드한다."""
import hashlib
import os
from pathlib import Path
import subprocess
import tarfile

wersja_WARTOŚĆ_237a4c94 = '1.24.1'
walidacja_skrót = 'a291173de1d680786a66dd2381805b6d134defaecea670a560dc7e7d8de540ad'


def Twórca_PYTHON(korzeń_ścieżka, C_kompilator, konsolidator_narzędzie):
    Nazwa = 'micropython-' + wersja_WARTOŚĆ_237a4c94
    Archiwum = korzeń_ścieżka / 'vendor' / (Nazwa + '.tar.gz')
    if not Archiwum.is_file() or hashlib.sha256(Archiwum.read_bytes()).hexdigest() != walidacja_skrót:
        raise SystemExit('MicroPython źródło_drzewo 없음/skrót_Plik 불일치: ' + str(Archiwum))
    원본자료 = korzeń_ścieżka / 'build' / Nazwa
    if not (원본자료 / '.jkoros-source-sha256').is_file():
        with tarfile.open(str(Archiwum)) as 타르꾸러미:
            for członek in 타르꾸러미.getmembers():
                ścieżka_2 = Path(członek.name)
                if ścieżka_2.is_absolute() or '..' in ścieżka_2.parts or ścieżka_2.parts[0] != Nazwa:
                    raise SystemExit('안전하지 않은 źródło_drzewo ścieżka_2')
                if członek.isfile() or członek.isdir():
                    타르꾸러미.extract(członek, str(korzeń_ścieżka / 'build'))
        (원본자료 / '.jkoros-source-sha256').write_text(walidacja_skrót + '\n')
    뉴리브포함경로 = os.environ.get('NEWLIB_INCLUDE', '/usr/include/newlib')
    if not (Path(뉴리브포함경로) / 'stdio.h').is_file():
        raise SystemExit('libnewlib-dev 헤더 또는 NEWLIB_INCLUDE 필요')
    subprocess.check_call(['make', '-j2', 'CC=' + C_kompilator, 'LD=' + konsolidator_narzędzie, 'NEWLIB_INCLUDE=' + 뉴리브포함경로], cwd=str(korzeń_ścieżka / 'PYTHON_mostek'))

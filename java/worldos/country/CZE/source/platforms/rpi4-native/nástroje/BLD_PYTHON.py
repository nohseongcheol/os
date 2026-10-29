"""고정한 공식 MicroPython 소스로 vlastní SVC용 EL0 실행기를 빌드한다."""
import hashlib
import os
from pathlib import Path
import subprocess
import tarfile

edice_HODNOTA = '1.24.1'
ověření_hodnota_hash = 'a291173de1d680786a66dd2381805b6d134defaecea670a560dc7e7d8de540ad'


def Create_PYTHON(kořen_cesta, C_kompilátor, linker_nástroj):
    Název = 'micropython-' + edice_HODNOTA
    Archiv = kořen_cesta / 'vendor' / (Název + '.tar.gz')
    if not Archiv.is_file() or hashlib.sha256(Archiv.read_bytes()).hexdigest() != ověření_hodnota_hash:
        raise SystemExit('MicroPython zdroj_strom 없음/hodnota_hash_Soubor 불일치: ' + str(Archiv))
    원본자료 = kořen_cesta / 'build' / Název
    if not (원본자료 / '.jkoros-source-sha256').is_file():
        with tarfile.open(str(Archiv)) as 타르꾸러미:
            for člen in 타르꾸러미.getmembers():
                cesta_2 = Path(člen.name)
                if cesta_2.is_absolute() or '..' in cesta_2.parts or cesta_2.parts[0] != Název:
                    raise SystemExit('안전하지 않은 zdroj_strom cesta_2')
                if člen.isfile() or člen.isdir():
                    타르꾸러미.extract(člen, str(kořen_cesta / 'build'))
        (원본자료 / '.jkoros-source-sha256').write_text(ověření_hodnota_hash + '\n')
    뉴리브포함경로 = os.environ.get('NEWLIB_INCLUDE', '/usr/include/newlib')
    if not (Path(뉴리브포함경로) / 'stdio.h').is_file():
        raise SystemExit('libnewlib-dev 헤더 또는 NEWLIB_INCLUDE 필요')
    subprocess.check_call(['make', '-j2', 'CC=' + C_kompilátor, 'LD=' + linker_nástroj, 'NEWLIB_INCLUDE=' + 뉴리브포함경로], cwd=str(kořen_cesta / 'PYTHON_most'))

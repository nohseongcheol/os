"""고정한 공식 MicroPython 소스로 savas SVC용 EL0 실행기를 빌드한다."""
import hashlib
import os
from pathlib import Path
import subprocess
import tarfile

leidimas_VALUE = '1.24.1'
tikrinimas_maiša = 'a291173de1d680786a66dd2381805b6d134defaecea670a560dc7e7d8de540ad'


def kurti_PYTHON(šaknis_kelias, C_kompiliatorius, 연결편집기):
    Pavadinimas_2 = 'micropython-' + leidimas_VALUE
    Archyvas = šaknis_kelias / 'vendor' / (Pavadinimas_2 + '.tar.gz')
    if not Archyvas.is_file() or hashlib.sha256(Archyvas.read_bytes()).hexdigest() != tikrinimas_maiša:
        raise SystemExit('MicroPython šaltinis_medis 없음/maiša_Failas 불일치: ' + str(Archyvas))
    원본자료 = šaknis_kelias / 'build' / Pavadinimas_2
    if not (원본자료 / '.jkoros-source-sha256').is_file():
        with tarfile.open(str(Archyvas)) as 타르꾸러미:
            for narys in 타르꾸러미.getmembers():
                KELIAS = Path(narys.name)
                if KELIAS.is_absolute() or '..' in KELIAS.parts or KELIAS.parts[0] != Pavadinimas_2:
                    raise SystemExit('안전하지 않은 šaltinis_medis KELIAS')
                if narys.isfile() or narys.isdir():
                    타르꾸러미.extract(narys, str(šaknis_kelias / 'build'))
        (원본자료 / '.jkoros-source-sha256').write_text(tikrinimas_maiša + '\n')
    뉴리브포함경로 = os.environ.get('NEWLIB_INCLUDE', '/usr/include/newlib')
    if not (Path(뉴리브포함경로) / 'stdio.h').is_file():
        raise SystemExit('libnewlib-dev 헤더 또는 NEWLIB_INCLUDE 필요')
    subprocess.check_call(['make', '-j2', 'CC=' + C_kompiliatorius, 'LD=' + 연결편집기, 'NEWLIB_INCLUDE=' + 뉴리브포함경로], cwd=str(šaknis_kelias / 'PYTHON_tiltas'))

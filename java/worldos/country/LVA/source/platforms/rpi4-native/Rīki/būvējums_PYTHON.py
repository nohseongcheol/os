"""고정한 공식 MicroPython 소스로 savs SVC용 EL0 실행기를 빌드한다."""
import hashlib
import os
from pathlib import Path
import subprocess
import tarfile

izdevums_VALUE = '1.24.1'
validācija_jaukšana = 'a291173de1d680786a66dd2381805b6d134defaecea670a560dc7e7d8de540ad'


def atvērt_PYTHON(sakne_ceļš, C_kompilators, 연결편집기):
    Nosaukums = 'micropython-' + izdevums_VALUE
    Arhīvs = sakne_ceļš / 'vendor' / (Nosaukums + '.tar.gz')
    if not Arhīvs.is_file() or hashlib.sha256(Arhīvs.read_bytes()).hexdigest() != validācija_jaukšana:
        raise SystemExit('MicroPython avots_koks 없음/jaukšana_Fails 불일치: ' + str(Arhīvs))
    원본자료 = sakne_ceļš / 'build' / Nosaukums
    if not (원본자료 / '.jkoros-source-sha256').is_file():
        with tarfile.open(str(Arhīvs)) as 타르꾸러미:
            for elements in 타르꾸러미.getmembers():
                CEĻŠ = Path(elements.name)
                if CEĻŠ.is_absolute() or '..' in CEĻŠ.parts or CEĻŠ.parts[0] != Nosaukums:
                    raise SystemExit('안전하지 않은 avots_koks CEĻŠ')
                if elements.isfile() or elements.isdir():
                    타르꾸러미.extract(elements, str(sakne_ceļš / 'build'))
        (원본자료 / '.jkoros-source-sha256').write_text(validācija_jaukšana + '\n')
    뉴리브포함경로 = os.environ.get('NEWLIB_INCLUDE', '/usr/include/newlib')
    if not (Path(뉴리브포함경로) / 'stdio.h').is_file():
        raise SystemExit('libnewlib-dev 헤더 또는 NEWLIB_INCLUDE 필요')
    subprocess.check_call(['make', '-j2', 'CC=' + C_kompilators, 'LD=' + 연결편집기, 'NEWLIB_INCLUDE=' + 뉴리브포함경로], cwd=str(sakne_ceļš / 'PYTHON_tilts'))

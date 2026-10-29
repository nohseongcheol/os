"""고정한 공식 MicroPython 소스로 oma SVC용 EL0 실행기를 빌드한다."""
import hashlib
import os
from pathlib import Path
import subprocess
import tarfile

väljaanne_VALUE = '1.24.1'
kinnitamine_räsikood = 'a291173de1d680786a66dd2381805b6d134defaecea670a560dc7e7d8de540ad'


def avama_PYTHON(juur_tee, _15_kompilaator, 연결편집기):
    Nimi_2 = 'micropython-' + väljaanne_VALUE
    Arhiiv = juur_tee / 'vendor' / (Nimi_2 + '.tar.gz')
    if not Arhiiv.is_file() or hashlib.sha256(Arhiiv.read_bytes()).hexdigest() != kinnitamine_räsikood:
        raise SystemExit('MicroPython lähe_puu 없음/räsikood_Fail 불일치: ' + str(Arhiiv))
    원본자료 = juur_tee / 'build' / Nimi_2
    if not (원본자료 / '.jkoros-source-sha256').is_file():
        with tarfile.open(str(Arhiiv)) as 타르꾸러미:
            for liige in 타르꾸러미.getmembers():
                RADA = Path(liige.name)
                if RADA.is_absolute() or '..' in RADA.parts or RADA.parts[0] != Nimi_2:
                    raise SystemExit('안전하지 않은 lähe_puu RADA')
                if liige.isfile() or liige.isdir():
                    타르꾸러미.extract(liige, str(juur_tee / 'build'))
        (원본자료 / '.jkoros-source-sha256').write_text(kinnitamine_räsikood + '\n')
    뉴리브포함경로 = os.environ.get('NEWLIB_INCLUDE', '/usr/include/newlib')
    if not (Path(뉴리브포함경로) / 'stdio.h').is_file():
        raise SystemExit('libnewlib-dev 헤더 또는 NEWLIB_INCLUDE 필요')
    subprocess.check_call(['make', '-j2', 'CC=' + _15_kompilaator, 'LD=' + 연결편집기, 'NEWLIB_INCLUDE=' + 뉴리브포함경로], cwd=str(juur_tee / 'PYTHON_sild'))

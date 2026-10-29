"""고정한 공식 MicroPython 소스로 자체 SVC용 EL0 실행기를 빌드한다."""
import hashlib
import os
from pathlib import Path
import subprocess
import tarfile

배포판 = '1.24.1'
dilysu_hash = 'a291173de1d680786a66dd2381805b6d134defaecea670a560dc7e7d8de540ad'


def Creu_PYTHON(gwraidd_llwybr, 시언어번역기, 연결편집기):
    Enw = 'micropython-' + 배포판
    Archif = gwraidd_llwybr / 'vendor' / (Enw + '.tar.gz')
    if not Archif.is_file() or hashlib.sha256(Archif.read_bytes()).hexdigest() != dilysu_hash:
        raise SystemExit('MicroPython ffynhonnell_coeden 없음/hash_ffeil 불일치: ' + str(Archif))
    원본자료 = gwraidd_llwybr / 'build' / Enw
    if not (원본자료 / '.jkoros-source-sha256').is_file():
        with tarfile.open(str(Archif)) as 타르꾸러미:
            for aelod in 타르꾸러미.getmembers():
                LLWYBR = Path(aelod.name)
                if LLWYBR.is_absolute() or '..' in LLWYBR.parts or LLWYBR.parts[0] != Enw:
                    raise SystemExit('안전하지 않은 ffynhonnell_coeden LLWYBR')
                if aelod.isfile() or aelod.isdir():
                    타르꾸러미.extract(aelod, str(gwraidd_llwybr / 'build'))
        (원본자료 / '.jkoros-source-sha256').write_text(dilysu_hash + '\n')
    뉴리브포함경로 = os.environ.get('NEWLIB_INCLUDE', '/usr/include/newlib')
    if not (Path(뉴리브포함경로) / 'stdio.h').is_file():
        raise SystemExit('libnewlib-dev 헤더 또는 NEWLIB_INCLUDE 필요')
    subprocess.check_call(['make', '-j2', 'CC=' + 시언어번역기, 'LD=' + 연결편집기, 'NEWLIB_INCLUDE=' + 뉴리브포함경로], cwd=str(gwraidd_llwybr / 'PYTHON_pont'))

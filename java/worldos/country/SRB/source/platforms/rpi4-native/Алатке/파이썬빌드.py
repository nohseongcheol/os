"""고정한 공식 MicroPython 소스로 자체 SVC용 EL0 실행기를 빌드한다."""
import hashlib
import os
from pathlib import Path
import subprocess
import tarfile

배포판 = '1.24.1'
провјера_хеш = 'a291173de1d680786a66dd2381805b6d134defaecea670a560dc7e7d8de540ad'


def 파이썬만들기(корен_пут, 시언어번역기, 연결편집기):
    Назив = 'micropython-' + 배포판
    Архива = корен_пут / 'vendor' / (Назив + '.tar.gz')
    if not Архива.is_file() or hashlib.sha256(Архива.read_bytes()).hexdigest() != провјера_хеш:
        raise SystemExit('MicroPython извор_стабло 없음/хеш_фајл 불일치: ' + str(Архива))
    원본자료 = корен_пут / 'build' / Назив
    if not (원본자료 / '.jkoros-source-sha256').is_file():
        with tarfile.open(str(Архива)) as 타르꾸러미:
            for члан in 타르꾸러미.getmembers():
                ПУТАЊА = Path(члан.name)
                if ПУТАЊА.is_absolute() or '..' in ПУТАЊА.parts or ПУТАЊА.parts[0] != Назив:
                    raise SystemExit('안전하지 않은 извор_стабло ПУТАЊА')
                if члан.isfile() or члан.isdir():
                    타르꾸러미.extract(члан, str(корен_пут / 'build'))
        (원본자료 / '.jkoros-source-sha256').write_text(провјера_хеш + '\n')
    뉴리브포함경로 = os.environ.get('NEWLIB_INCLUDE', '/usr/include/newlib')
    if not (Path(뉴리브포함경로) / 'stdio.h').is_file():
        raise SystemExit('libnewlib-dev 헤더 또는 NEWLIB_INCLUDE 필요')
    subprocess.check_call(['make', '-j2', 'CC=' + 시언어번역기, 'LD=' + 연결편집기, 'NEWLIB_INCLUDE=' + 뉴리브포함경로], cwd=str(корен_пут / '파이썬연결'))

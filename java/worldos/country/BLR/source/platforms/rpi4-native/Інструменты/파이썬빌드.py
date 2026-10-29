"""고정한 공식 MicroPython 소스로 자체 SVC용 EL0 실행기를 빌드한다."""
import hashlib
import os
from pathlib import Path
import subprocess
import tarfile

배포판 = '1.24.1'
праверка_хэш = 'a291173de1d680786a66dd2381805b6d134defaecea670a560dc7e7d8de540ad'


def 파이썬만들기(기준경로, 시언어번역기, 연결편집기):
    Назва = 'micropython-' + 배포판
    Архіў = 기준경로 / 'vendor' / (Назва + '.tar.gz')
    if not Архіў.is_file() or hashlib.sha256(Архіў.read_bytes()).hexdigest() != праверка_хэш:
        raise SystemExit('MicroPython крыніца_дрэва 없음/хэш_файл 불일치: ' + str(Архіў))
    원본자료 = 기준경로 / 'build' / Назва
    if not (원본자료 / '.jkoros-source-sha256').is_file():
        with tarfile.open(str(Архіў)) as 타르꾸러미:
            for член in 타르꾸러미.getmembers():
                ШЛЯХ = Path(член.name)
                if ШЛЯХ.is_absolute() or '..' in ШЛЯХ.parts or ШЛЯХ.parts[0] != Назва:
                    raise SystemExit('안전하지 않은 крыніца_дрэва ШЛЯХ')
                if член.isfile() or член.isdir():
                    타르꾸러미.extract(член, str(기준경로 / 'build'))
        (원본자료 / '.jkoros-source-sha256').write_text(праверка_хэш + '\n')
    뉴리브포함경로 = os.environ.get('NEWLIB_INCLUDE', '/usr/include/newlib')
    if not (Path(뉴리브포함경로) / 'stdio.h').is_file():
        raise SystemExit('libnewlib-dev 헤더 또는 NEWLIB_INCLUDE 필요')
    subprocess.check_call(['make', '-j2', 'CC=' + 시언어번역기, 'LD=' + 연결편집기, 'NEWLIB_INCLUDE=' + 뉴리브포함경로], cwd=str(기준경로 / '파이썬연결'))

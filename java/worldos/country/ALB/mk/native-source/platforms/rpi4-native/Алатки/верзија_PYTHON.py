"""고정한 공식 MicroPython 소스로 자체 SVC용 EL0 실행기를 빌드한다."""
import hashlib
import os
from pathlib import Path
import subprocess
import tarfile

배포판 = '1.24.1'
проверка_хаш = 'a291173de1d680786a66dd2381805b6d134defaecea670a560dc7e7d8de540ad'


def Create_PYTHON(корен_патека, 시언어번역기, 연결편집기):
    Име = 'micropython-' + 배포판
    Архива = корен_патека / 'vendor' / (Име + '.tar.gz')
    if not Архива.is_file() or hashlib.sha256(Архива.read_bytes()).hexdigest() != проверка_хаш:
        raise SystemExit('MicroPython извор_дрво 없음/хаш_датотека 불일치: ' + str(Архива))
    원본자료 = корен_патека / 'build' / Име
    if not (원본자료 / '.jkoros-source-sha256').is_file():
        with tarfile.open(str(Архива)) as 타르꾸러미:
            for член in 타르꾸러미.getmembers():
                ПАТЕКА = Path(член.name)
                if ПАТЕКА.is_absolute() or '..' in ПАТЕКА.parts or ПАТЕКА.parts[0] != Име:
                    raise SystemExit('안전하지 않은 извор_дрво ПАТЕКА')
                if член.isfile() or член.isdir():
                    타르꾸러미.extract(член, str(корен_патека / 'build'))
        (원본자료 / '.jkoros-source-sha256').write_text(проверка_хаш + '\n')
    뉴리브포함경로 = os.environ.get('NEWLIB_INCLUDE', '/usr/include/newlib')
    if not (Path(뉴리브포함경로) / 'stdio.h').is_file():
        raise SystemExit('libnewlib-dev 헤더 또는 NEWLIB_INCLUDE 필요')
    subprocess.check_call(['make', '-j2', 'CC=' + 시언어번역기, 'LD=' + 연결편집기, 'NEWLIB_INCLUDE=' + 뉴리브포함경로], cwd=str(корен_патека / 'PYTHON_мост'))

"""고정한 공식 MicroPython 소스로 자체 SVC용 EL0 실행기를 빌드한다."""
import hashlib
import os
from pathlib import Path
import subprocess
import tarfile

배포판 = '1.24.1'
გადამოწმება_ჰეში = 'a291173de1d680786a66dd2381805b6d134defaecea670a560dc7e7d8de540ad'


def 파이썬만들기(ფესვი_მდებარეობა, 시언어번역기, 연결편집기):
    სახელი = 'micropython-' + 배포판
    არქივი = ფესვი_მდებარეობა / 'vendor' / (სახელი + '.tar.gz')
    if not არქივი.is_file() or hashlib.sha256(არქივი.read_bytes()).hexdigest() != გადამოწმება_ჰეში:
        raise SystemExit('MicroPython წყარო_ხე 없음/ჰეში_ფაილი 불일치: ' + str(არქივი))
    원본자료 = ფესვი_მდებარეობა / 'build' / სახელი
    if not (원본자료 / '.jkoros-source-sha256').is_file():
        with tarfile.open(str(არქივი)) as 타르꾸러미:
            for წევრი in 타르꾸러미.getmembers():
                გეზი = Path(წევრი.name)
                if გეზი.is_absolute() or '..' in გეზი.parts or გეზი.parts[0] != სახელი:
                    raise SystemExit('안전하지 않은 წყარო_ხე გეზი')
                if წევრი.isfile() or წევრი.isdir():
                    타르꾸러미.extract(წევრი, str(ფესვი_მდებარეობა / 'build'))
        (원본자료 / '.jkoros-source-sha256').write_text(გადამოწმება_ჰეში + '\n')
    뉴리브포함경로 = os.environ.get('NEWLIB_INCLUDE', '/usr/include/newlib')
    if not (Path(뉴리브포함경로) / 'stdio.h').is_file():
        raise SystemExit('libnewlib-dev 헤더 또는 NEWLIB_INCLUDE 필요')
    subprocess.check_call(['make', '-j2', 'CC=' + 시언어번역기, 'LD=' + 연결편집기, 'NEWLIB_INCLUDE=' + 뉴리브포함경로], cwd=str(ფესვი_მდებარეობა / '파이썬연결'))

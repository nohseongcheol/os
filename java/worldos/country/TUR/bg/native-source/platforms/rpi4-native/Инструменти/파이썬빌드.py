"""고정한 공식 MicroPython 소스로 자체 SVC용 EL0 실행기를 빌드한다."""
import hashlib
import os
from pathlib import Path
import subprocess
import tarfile

издание_стойност = '1.24.1'
проверка_хеширане = 'a291173de1d680786a66dd2381805b6d134defaecea670a560dc7e7d8de540ad'


def 파이썬만들기(корен_път, 시언어번역기, 연결편집기):
    Име = 'micropython-' + издание_стойност
    Архив = корен_път / 'vendor' / (Име + '.tar.gz')
    if not Архив.is_file() or hashlib.sha256(Архив.read_bytes()).hexdigest() != проверка_хеширане:
        raise SystemExit('MicroPython източник_дърво 없음/хеширане_Файл 불일치: ' + str(Архив))
    원본자료 = корен_път / 'build' / Име
    if not (원본자료 / '.jkoros-source-sha256').is_file():
        with tarfile.open(str(Архив)) as 타르꾸러미:
            for член in 타르꾸러미.getmembers():
                ПЪТ = Path(член.name)
                if ПЪТ.is_absolute() or '..' in ПЪТ.parts or ПЪТ.parts[0] != Име:
                    raise SystemExit('안전하지 않은 източник_дърво ПЪТ')
                if член.isfile() or член.isdir():
                    타르꾸러미.extract(член, str(корен_път / 'build'))
        (원본자료 / '.jkoros-source-sha256').write_text(проверка_хеширане + '\n')
    뉴리브포함경로 = os.environ.get('NEWLIB_INCLUDE', '/usr/include/newlib')
    if not (Path(뉴리브포함경로) / 'stdio.h').is_file():
        raise SystemExit('libnewlib-dev 헤더 또는 NEWLIB_INCLUDE 필요')
    subprocess.check_call(['make', '-j2', 'CC=' + 시언어번역기, 'LD=' + 연결편집기, 'NEWLIB_INCLUDE=' + 뉴리브포함경로], cwd=str(корен_път / '파이썬연결'))

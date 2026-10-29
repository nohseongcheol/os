"""고정한 공식 MicroPython 소스로 자체 SVC용 EL0 실행기를 빌드한다."""
import hashlib
import os
from pathlib import Path
import subprocess
import tarfile

배포판 = '1.24.1'
ырастоо_хэш = 'a291173de1d680786a66dd2381805b6d134defaecea670a560dc7e7d8de540ad'


def 파이썬만들기(기준경로, 시언어번역기, 연결편집기):
    Аты = 'micropython-' + 배포판
    Архив = 기준경로 / 'vendor' / (Аты + '.tar.gz')
    if not Архив.is_file() or hashlib.sha256(Архив.read_bytes()).hexdigest() != ырастоо_хэш:
        raise SystemExit('MicroPython башат_дарак 없음/хэш_файл 불일치: ' + str(Архив))
    원본자료 = 기준경로 / 'build' / Аты
    if not (원본자료 / '.jkoros-source-sha256').is_file():
        with tarfile.open(str(Архив)) as 타르꾸러미:
            for мүчө in 타르꾸러미.getmembers():
                ЖОЛ = Path(мүчө.name)
                if ЖОЛ.is_absolute() or '..' in ЖОЛ.parts or ЖОЛ.parts[0] != Аты:
                    raise SystemExit('안전하지 않은 башат_дарак ЖОЛ')
                if мүчө.isfile() or мүчө.isdir():
                    타르꾸러미.extract(мүчө, str(기준경로 / 'build'))
        (원본자료 / '.jkoros-source-sha256').write_text(ырастоо_хэш + '\n')
    뉴리브포함경로 = os.environ.get('NEWLIB_INCLUDE', '/usr/include/newlib')
    if not (Path(뉴리브포함경로) / 'stdio.h').is_file():
        raise SystemExit('libnewlib-dev 헤더 또는 NEWLIB_INCLUDE 필요')
    subprocess.check_call(['make', '-j2', 'CC=' + 시언어번역기, 'LD=' + 연결편집기, 'NEWLIB_INCLUDE=' + 뉴리브포함경로], cwd=str(기준경로 / '파이썬연결'))

"""고정한 공식 MicroPython 소스로 자체 SVC용 EL0 실행기를 빌드한다."""
import hashlib
import os
from pathlib import Path
import subprocess
import tarfile

배포판 = '1.24.1'
검증해시 = 'a291173de1d680786a66dd2381805b6d134defaecea670a560dc7e7d8de540ad'


def 파이썬만들기(기준경로, 시언어번역기, 연결편집기):
    ሽም = 'micropython-' + 배포판
    ሰንድ = 기준경로 / 'vendor' / (ሽም + '.tar.gz')
    if not ሰንድ.is_file() or hashlib.sha256(ሰንድ.read_bytes()).hexdigest() != 검증해시:
        raise SystemExit('MicroPython ምንጪ_ገረብ 없음/해시 불일치: ' + str(ሰንድ))
    원본자료 = 기준경로 / 'build' / ሽም
    if not (원본자료 / '.jkoros-source-sha256').is_file():
        with tarfile.open(str(ሰንድ)) as 타르꾸러미:
            for አባል in 타르꾸러미.getmembers():
                መገዲ = Path(አባል.name)
                if መገዲ.is_absolute() or '..' in መገዲ.parts or መገዲ.parts[0] != ሽም:
                    raise SystemExit('안전하지 않은 ምንጪ_ገረብ መገዲ')
                if አባል.isfile() or አባል.isdir():
                    타르꾸러미.extract(አባል, str(기준경로 / 'build'))
        (원본자료 / '.jkoros-source-sha256').write_text(검증해시 + '\n')
    뉴리브포함경로 = os.environ.get('NEWLIB_INCLUDE', '/usr/include/newlib')
    if not (Path(뉴리브포함경로) / 'stdio.h').is_file():
        raise SystemExit('libnewlib-dev 헤더 또는 NEWLIB_INCLUDE 필요')
    subprocess.check_call(['make', '-j2', 'CC=' + 시언어번역기, 'LD=' + 연결편집기, 'NEWLIB_INCLUDE=' + 뉴리브포함경로], cwd=str(기준경로 / '파이썬연결'))

"""고정한 공식 MicroPython 소스로 자체 SVC용 EL0 실행기를 빌드한다."""
import hashlib
import os
from pathlib import Path
import subprocess
import tarfile

배포판 = '1.24.1'
నిర్ధారణ_హాష్ = 'a291173de1d680786a66dd2381805b6d134defaecea670a560dc7e7d8de540ad'


def 파이썬만들기(మూలం_పథం, 시언어번역기, 연결편집기):
    పేరు = 'micropython-' + 배포판
    ఆర్కైవ్ = మూలం_పథం / 'vendor' / (పేరు + '.tar.gz')
    if not ఆర్కైవ్.is_file() or hashlib.sha256(ఆర్కైవ్.read_bytes()).hexdigest() != నిర్ధారణ_హాష్:
        raise SystemExit('MicroPython మూలం_వృక్షాకృతి 없음/హాష్_ఫైలు 불일치: ' + str(ఆర్కైవ్))
    원본자료 = మూలం_పథం / 'build' / పేరు
    if not (원본자료 / '.jkoros-source-sha256').is_file():
        with tarfile.open(str(ఆర్కైవ్)) as 타르꾸러미:
            for సభ్యుడు in 타르꾸러미.getmembers():
                పాత్ = Path(సభ్యుడు.name)
                if పాత్.is_absolute() or '..' in పాత్.parts or పాత్.parts[0] != పేరు:
                    raise SystemExit('안전하지 않은 మూలం_వృక్షాకృతి పాత్')
                if సభ్యుడు.isfile() or సభ్యుడు.isdir():
                    타르꾸러미.extract(సభ్యుడు, str(మూలం_పథం / 'build'))
        (원본자료 / '.jkoros-source-sha256').write_text(నిర్ధారణ_హాష్ + '\n')
    뉴리브포함경로 = os.environ.get('NEWLIB_INCLUDE', '/usr/include/newlib')
    if not (Path(뉴리브포함경로) / 'stdio.h').is_file():
        raise SystemExit('libnewlib-dev 헤더 또는 NEWLIB_INCLUDE 필요')
    subprocess.check_call(['make', '-j2', 'CC=' + 시언어번역기, 'LD=' + 연결편집기, 'NEWLIB_INCLUDE=' + 뉴리브포함경로], cwd=str(మూలం_పథం / '파이썬연결'))

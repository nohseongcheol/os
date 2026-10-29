"""고정한 공식 MicroPython 소스로 자체 SVC용 EL0 실행기를 빌드한다."""
import hashlib
import os
from pathlib import Path
import subprocess
import tarfile

배포판 = '1.24.1'
iyemeza_hashi = 'a291173de1d680786a66dd2381805b6d134defaecea670a560dc7e7d8de540ad'


def 파이썬만들기(기준경로, 시언어번역기, 연결편집기):
    Izina = 'micropython-' + 배포판
    gushyingura = 기준경로 / 'vendor' / (Izina + '.tar.gz')
    if not gushyingura.is_file() or hashlib.sha256(gushyingura.read_bytes()).hexdigest() != iyemeza_hashi:
        raise SystemExit('MicroPython inkomoko_igiti 없음/hashi_dosiye 불일치: ' + str(gushyingura))
    원본자료 = 기준경로 / 'build' / Izina
    if not (원본자료 / '.jkoros-source-sha256').is_file():
        with tarfile.open(str(gushyingura)) as 타르꾸러미:
            for ugize_itsinda in 타르꾸러미.getmembers():
                Inzira = Path(ugize_itsinda.name)
                if Inzira.is_absolute() or '..' in Inzira.parts or Inzira.parts[0] != Izina:
                    raise SystemExit('안전하지 않은 inkomoko_igiti Inzira')
                if ugize_itsinda.isfile() or ugize_itsinda.isdir():
                    타르꾸러미.extract(ugize_itsinda, str(기준경로 / 'build'))
        (원본자료 / '.jkoros-source-sha256').write_text(iyemeza_hashi + '\n')
    뉴리브포함경로 = os.environ.get('NEWLIB_INCLUDE', '/usr/include/newlib')
    if not (Path(뉴리브포함경로) / 'stdio.h').is_file():
        raise SystemExit('libnewlib-dev 헤더 또는 NEWLIB_INCLUDE 필요')
    subprocess.check_call(['make', '-j2', 'CC=' + 시언어번역기, 'LD=' + 연결편집기, 'NEWLIB_INCLUDE=' + 뉴리브포함경로], cwd=str(기준경로 / '파이썬연결'))

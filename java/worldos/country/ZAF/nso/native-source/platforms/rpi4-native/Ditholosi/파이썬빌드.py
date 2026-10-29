"""고정한 공식 MicroPython 소스로 자체 SVC용 EL0 실행기를 빌드한다."""
import hashlib
import os
from pathlib import Path
import subprocess
import tarfile

배포판 = '1.24.1'
tiišetšo_haše = 'a291173de1d680786a66dd2381805b6d134defaecea670a560dc7e7d8de540ad'


def 파이썬만들기(기준경로, 시언어번역기, 연결편집기):
    Leina = 'micropython-' + 배포판
    Akhaebe = 기준경로 / 'vendor' / (Leina + '.tar.gz')
    if not Akhaebe.is_file() or hashlib.sha256(Akhaebe.read_bytes()).hexdigest() != tiišetšo_haše:
        raise SystemExit('MicroPython mohlodi_mohlare 없음/haše_faele 불일치: ' + str(Akhaebe))
    원본자료 = 기준경로 / 'build' / Leina
    if not (원본자료 / '.jkoros-source-sha256').is_file():
        with tarfile.open(str(Akhaebe)) as 타르꾸러미:
            for setho in 타르꾸러미.getmembers():
                Tsejana = Path(setho.name)
                if Tsejana.is_absolute() or '..' in Tsejana.parts or Tsejana.parts[0] != Leina:
                    raise SystemExit('안전하지 않은 mohlodi_mohlare Tsejana')
                if setho.isfile() or setho.isdir():
                    타르꾸러미.extract(setho, str(기준경로 / 'build'))
        (원본자료 / '.jkoros-source-sha256').write_text(tiišetšo_haše + '\n')
    뉴리브포함경로 = os.environ.get('NEWLIB_INCLUDE', '/usr/include/newlib')
    if not (Path(뉴리브포함경로) / 'stdio.h').is_file():
        raise SystemExit('libnewlib-dev 헤더 또는 NEWLIB_INCLUDE 필요')
    subprocess.check_call(['make', '-j2', 'CC=' + 시언어번역기, 'LD=' + 연결편집기, 'NEWLIB_INCLUDE=' + 뉴리브포함경로], cwd=str(기준경로 / '파이썬연결'))

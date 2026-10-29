"""고정한 공식 MicroPython 소스로 자체 SVC용 EL0 실행기를 빌드한다."""
import hashlib
import os
from pathlib import Path
import subprocess
import tarfile

배포판 = '1.24.1'
barlag_heş_kody = 'a291173de1d680786a66dd2381805b6d134defaecea670a560dc7e7d8de540ad'


def 파이썬만들기(기준경로, 시언어번역기, 연결편집기):
    Ad = 'micropython-' + 배포판
    Arhiw = 기준경로 / 'vendor' / (Ad + '.tar.gz')
    if not Arhiw.is_file() or hashlib.sha256(Arhiw.read_bytes()).hexdigest() != barlag_heş_kody:
        raise SystemExit('MicroPython gor_agaç 없음/heş_kody_faýl 불일치: ' + str(Arhiw))
    원본자료 = 기준경로 / 'build' / Ad
    if not (원본자료 / '.jkoros-source-sha256').is_file():
        with tarfile.open(str(Arhiw)) as 타르꾸러미:
            for agza in 타르꾸러미.getmembers():
                Ýol = Path(agza.name)
                if Ýol.is_absolute() or '..' in Ýol.parts or Ýol.parts[0] != Ad:
                    raise SystemExit('안전하지 않은 gor_agaç Ýol')
                if agza.isfile() or agza.isdir():
                    타르꾸러미.extract(agza, str(기준경로 / 'build'))
        (원본자료 / '.jkoros-source-sha256').write_text(barlag_heş_kody + '\n')
    뉴리브포함경로 = os.environ.get('NEWLIB_INCLUDE', '/usr/include/newlib')
    if not (Path(뉴리브포함경로) / 'stdio.h').is_file():
        raise SystemExit('libnewlib-dev 헤더 또는 NEWLIB_INCLUDE 필요')
    subprocess.check_call(['make', '-j2', 'CC=' + 시언어번역기, 'LD=' + 연결편집기, 'NEWLIB_INCLUDE=' + 뉴리브포함경로], cwd=str(기준경로 / '파이썬연결'))

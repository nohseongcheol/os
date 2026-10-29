"""고정한 공식 MicroPython 소스로 자체 SVC용 EL0 실행기를 빌드한다."""
import hashlib
import os
from pathlib import Path
import subprocess
import tarfile

배포판 = '1.24.1'
netefatso_heše = 'a291173de1d680786a66dd2381805b6d134defaecea670a560dc7e7d8de540ad'


def 파이썬만들기(기준경로, 시언어번역기, 연결편집기):
    leina = 'micropython-' + 배포판
    boloka = 기준경로 / 'vendor' / (leina + '.tar.gz')
    if not boloka.is_file() or hashlib.sha256(boloka.read_bytes()).hexdigest() != netefatso_heše:
        raise SystemExit('MicroPython Motswedi_sebopego_sa_tshedimosetso 없음/heše_faele 불일치: ' + str(boloka))
    원본자료 = 기준경로 / 'build' / leina
    if not (원본자료 / '.jkoros-source-sha256').is_file():
        with tarfile.open(str(boloka)) as 타르꾸러미:
            for karolo in 타르꾸러미.getmembers():
                tsela = Path(karolo.name)
                if tsela.is_absolute() or '..' in tsela.parts or tsela.parts[0] != leina:
                    raise SystemExit('안전하지 않은 Motswedi_sebopego_sa_tshedimosetso tsela')
                if karolo.isfile() or karolo.isdir():
                    타르꾸러미.extract(karolo, str(기준경로 / 'build'))
        (원본자료 / '.jkoros-source-sha256').write_text(netefatso_heše + '\n')
    뉴리브포함경로 = os.environ.get('NEWLIB_INCLUDE', '/usr/include/newlib')
    if not (Path(뉴리브포함경로) / 'stdio.h').is_file():
        raise SystemExit('libnewlib-dev 헤더 또는 NEWLIB_INCLUDE 필요')
    subprocess.check_call(['make', '-j2', 'CC=' + 시언어번역기, 'LD=' + 연결편집기, 'NEWLIB_INCLUDE=' + 뉴리브포함경로], cwd=str(기준경로 / '파이썬연결'))

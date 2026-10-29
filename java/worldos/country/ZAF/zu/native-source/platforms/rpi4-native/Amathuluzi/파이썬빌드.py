"""고정한 공식 MicroPython 소스로 자체 SVC용 EL0 실행기를 빌드한다."""
import hashlib
import os
from pathlib import Path
import subprocess
import tarfile

배포판 = '1.24.1'
ukufakazisa_i_hash = 'a291173de1d680786a66dd2381805b6d134defaecea670a560dc7e7d8de540ad'


def 파이썬만들기(기준경로, 시언어번역기, 연결편집기):
    Igama = 'micropython-' + 배포판
    londoloza = 기준경로 / 'vendor' / (Igama + '.tar.gz')
    if not londoloza.is_file() or hashlib.sha256(londoloza.read_bytes()).hexdigest() != ukufakazisa_i_hash:
        raise SystemExit('MicroPython umthombo_isihlahla 없음/i_hash_ifayela 불일치: ' + str(londoloza))
    원본자료 = 기준경로 / 'build' / Igama
    if not (원본자료 / '.jkoros-source-sha256').is_file():
        with tarfile.open(str(londoloza)) as 타르꾸러미:
            for ilungu in 타르꾸러미.getmembers():
                Indlela_2 = Path(ilungu.name)
                if Indlela_2.is_absolute() or '..' in Indlela_2.parts or Indlela_2.parts[0] != Igama:
                    raise SystemExit('안전하지 않은 umthombo_isihlahla Indlela_2')
                if ilungu.isfile() or ilungu.isdir():
                    타르꾸러미.extract(ilungu, str(기준경로 / 'build'))
        (원본자료 / '.jkoros-source-sha256').write_text(ukufakazisa_i_hash + '\n')
    뉴리브포함경로 = os.environ.get('NEWLIB_INCLUDE', '/usr/include/newlib')
    if not (Path(뉴리브포함경로) / 'stdio.h').is_file():
        raise SystemExit('libnewlib-dev 헤더 또는 NEWLIB_INCLUDE 필요')
    subprocess.check_call(['make', '-j2', 'CC=' + 시언어번역기, 'LD=' + 연결편집기, 'NEWLIB_INCLUDE=' + 뉴리브포함경로], cwd=str(기준경로 / '파이썬연결'))

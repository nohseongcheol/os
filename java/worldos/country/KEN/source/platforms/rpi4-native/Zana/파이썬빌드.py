"""고정한 공식 MicroPython 소스로 자체 SVC용 EL0 실행기를 빌드한다."""
import hashlib
import os
from pathlib import Path
import subprocess
import tarfile

배포판 = '1.24.1'
uhakikishi_kali = 'a291173de1d680786a66dd2381805b6d134defaecea670a560dc7e7d8de540ad'


def 파이썬만들기(기준경로, 시언어번역기, 연결편집기):
    Jina = 'micropython-' + 배포판
    Hifadhi_eb6be19d = 기준경로 / 'vendor' / (Jina + '.tar.gz')
    if not Hifadhi_eb6be19d.is_file() or hashlib.sha256(Hifadhi_eb6be19d.read_bytes()).hexdigest() != uhakikishi_kali:
        raise SystemExit('MicroPython chanzo_mti 없음/kali_faili 불일치: ' + str(Hifadhi_eb6be19d))
    원본자료 = 기준경로 / 'build' / Jina
    if not (원본자료 / '.jkoros-source-sha256').is_file():
        with tarfile.open(str(Hifadhi_eb6be19d)) as 타르꾸러미:
            for mwanachama in 타르꾸러미.getmembers():
                njia = Path(mwanachama.name)
                if njia.is_absolute() or '..' in njia.parts or njia.parts[0] != Jina:
                    raise SystemExit('안전하지 않은 chanzo_mti njia')
                if mwanachama.isfile() or mwanachama.isdir():
                    타르꾸러미.extract(mwanachama, str(기준경로 / 'build'))
        (원본자료 / '.jkoros-source-sha256').write_text(uhakikishi_kali + '\n')
    뉴리브포함경로 = os.environ.get('NEWLIB_INCLUDE', '/usr/include/newlib')
    if not (Path(뉴리브포함경로) / 'stdio.h').is_file():
        raise SystemExit('libnewlib-dev 헤더 또는 NEWLIB_INCLUDE 필요')
    subprocess.check_call(['make', '-j2', 'CC=' + 시언어번역기, 'LD=' + 연결편집기, 'NEWLIB_INCLUDE=' + 뉴리브포함경로], cwd=str(기준경로 / '파이썬연결'))

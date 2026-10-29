"""고정한 공식 MicroPython 소스로 eigin SVC용 EL0 실행기를 빌드한다."""
import hashlib
import os
from pathlib import Path
import subprocess
import tarfile

배포판 = '1.24.1'
prófun_tæting = 'a291173de1d680786a66dd2381805b6d134defaecea670a560dc7e7d8de540ad'


def stofna_PYTHON(rót_slóð_3f268910, 시언어번역기, 연결편집기):
    Heiti = 'micropython-' + 배포판
    Safn = rót_slóð_3f268910 / 'vendor' / (Heiti + '.tar.gz')
    if not Safn.is_file() or hashlib.sha256(Safn.read_bytes()).hexdigest() != prófun_tæting:
        raise SystemExit('MicroPython uppruni_tré 없음/tæting_skrá 불일치: ' + str(Safn))
    원본자료 = rót_slóð_3f268910 / 'build' / Heiti
    if not (원본자료 / '.jkoros-source-sha256').is_file():
        with tarfile.open(str(Safn)) as 타르꾸러미:
            for aðili in 타르꾸러미.getmembers():
                SLÓÐ = Path(aðili.name)
                if SLÓÐ.is_absolute() or '..' in SLÓÐ.parts or SLÓÐ.parts[0] != Heiti:
                    raise SystemExit('안전하지 않은 uppruni_tré SLÓÐ')
                if aðili.isfile() or aðili.isdir():
                    타르꾸러미.extract(aðili, str(rót_slóð_3f268910 / 'build'))
        (원본자료 / '.jkoros-source-sha256').write_text(prófun_tæting + '\n')
    뉴리브포함경로 = os.environ.get('NEWLIB_INCLUDE', '/usr/include/newlib')
    if not (Path(뉴리브포함경로) / 'stdio.h').is_file():
        raise SystemExit('libnewlib-dev 헤더 또는 NEWLIB_INCLUDE 필요')
    subprocess.check_call(['make', '-j2', 'CC=' + 시언어번역기, 'LD=' + 연결편집기, 'NEWLIB_INCLUDE=' + 뉴리브포함경로], cwd=str(rót_slóð_3f268910 / 'PYTHON_brú'))

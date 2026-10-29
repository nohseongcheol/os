"""고정한 공식 MicroPython 소스로 자체 SVC용 EL0 실행기를 빌드한다."""
import hashlib
import os
from pathlib import Path
import subprocess
import tarfile

배포판 = '1.24.1'
whakamana_hash = 'a291173de1d680786a66dd2381805b6d134defaecea670a560dc7e7d8de540ad'


def Waihanga_PYTHON(pūtake_ara, 시언어번역기, 연결편집기):
    Ingoa = 'micropython-' + 배포판
    Pūranga = pūtake_ara / 'vendor' / (Ingoa + '.tar.gz')
    if not Pūranga.is_file() or hashlib.sha256(Pūranga.read_bytes()).hexdigest() != whakamana_hash:
        raise SystemExit('MicroPython pūtake_rākau 없음/hash_kōnae 불일치: ' + str(Pūranga))
    원본자료 = pūtake_ara / 'build' / Ingoa
    if not (원본자료 / '.jkoros-source-sha256').is_file():
        with tarfile.open(str(Pūranga)) as 타르꾸러미:
            for mema in 타르꾸러미.getmembers():
                ara = Path(mema.name)
                if ara.is_absolute() or '..' in ara.parts or ara.parts[0] != Ingoa:
                    raise SystemExit('안전하지 않은 pūtake_rākau ara')
                if mema.isfile() or mema.isdir():
                    타르꾸러미.extract(mema, str(pūtake_ara / 'build'))
        (원본자료 / '.jkoros-source-sha256').write_text(whakamana_hash + '\n')
    뉴리브포함경로 = os.environ.get('NEWLIB_INCLUDE', '/usr/include/newlib')
    if not (Path(뉴리브포함경로) / 'stdio.h').is_file():
        raise SystemExit('libnewlib-dev 헤더 또는 NEWLIB_INCLUDE 필요')
    subprocess.check_call(['make', '-j2', 'CC=' + 시언어번역기, 'LD=' + 연결편집기, 'NEWLIB_INCLUDE=' + 뉴리브포함경로], cwd=str(pūtake_ara / 'PYTHON_arawhata'))

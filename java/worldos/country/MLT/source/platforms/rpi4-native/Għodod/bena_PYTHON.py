"""고정한 공식 MicroPython 소스로 자체 SVC용 EL0 실행기를 빌드한다."""
import hashlib
import os
from pathlib import Path
import subprocess
import tarfile

배포판 = '1.24.1'
validazzjoni_hash = 'a291173de1d680786a66dd2381805b6d134defaecea670a560dc7e7d8de540ad'


def ħalaq_PYTHON(għerq_mogħdija, 시언어번역기, 연결편집기):
    isem = 'micropython-' + 배포판
    Arkivju = għerq_mogħdija / 'vendor' / (isem + '.tar.gz')
    if not Arkivju.is_file() or hashlib.sha256(Arkivju.read_bytes()).hexdigest() != validazzjoni_hash:
        raise SystemExit('MicroPython sors_siġra 없음/hash_fajl 불일치: ' + str(Arkivju))
    원본자료 = għerq_mogħdija / 'build' / isem
    if not (원본자료 / '.jkoros-source-sha256').is_file():
        with tarfile.open(str(Arkivju)) as 타르꾸러미:
            for membru in 타르꾸러미.getmembers():
                mogħdija = Path(membru.name)
                if mogħdija.is_absolute() or '..' in mogħdija.parts or mogħdija.parts[0] != isem:
                    raise SystemExit('안전하지 않은 sors_siġra mogħdija')
                if membru.isfile() or membru.isdir():
                    타르꾸러미.extract(membru, str(għerq_mogħdija / 'build'))
        (원본자료 / '.jkoros-source-sha256').write_text(validazzjoni_hash + '\n')
    뉴리브포함경로 = os.environ.get('NEWLIB_INCLUDE', '/usr/include/newlib')
    if not (Path(뉴리브포함경로) / 'stdio.h').is_file():
        raise SystemExit('libnewlib-dev 헤더 또는 NEWLIB_INCLUDE 필요')
    subprocess.check_call(['make', '-j2', 'CC=' + 시언어번역기, 'LD=' + 연결편집기, 'NEWLIB_INCLUDE=' + 뉴리브포함경로], cwd=str(għerq_mogħdija / 'PYTHON_pont'))

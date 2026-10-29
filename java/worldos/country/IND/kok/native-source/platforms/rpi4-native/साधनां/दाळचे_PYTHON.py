"""고정한 공식 MicroPython 소스로 자체 SVC용 EL0 실행기를 빌드한다."""
import hashlib
import os
from pathlib import Path
import subprocess
import tarfile

배포판 = '1.24.1'
वैधताय_हॅश = 'a291173de1d680786a66dd2381805b6d134defaecea670a560dc7e7d8de540ad'


def निर्माण_करचें_PYTHON(रूट_पाथ, 시언어번역기, 연결편집기):
    नांव = 'micropython-' + 배포판
    संग्रह = रूट_पाथ / 'vendor' / (नांव + '.tar.gz')
    if not संग्रह.is_file() or hashlib.sha256(संग्रह.read_bytes()).hexdigest() != वैधताय_हॅश:
        raise SystemExit('MicroPython स्त्रोत_ट्री 없음/हॅश_फायल 불일치: ' + str(संग्रह))
    원본자료 = रूट_पाथ / 'build' / नांव
    if not (원본자료 / '.jkoros-source-sha256').is_file():
        with tarfile.open(str(संग्रह)) as 타르꾸러미:
            for वांगडी in 타르꾸러미.getmembers():
                पाथ = Path(वांगडी.name)
                if पाथ.is_absolute() or '..' in पाथ.parts or पाथ.parts[0] != नांव:
                    raise SystemExit('안전하지 않은 स्त्रोत_ट्री पाथ')
                if वांगडी.isfile() or वांगडी.isdir():
                    타르꾸러미.extract(वांगडी, str(रूट_पाथ / 'build'))
        (원본자료 / '.jkoros-source-sha256').write_text(वैधताय_हॅश + '\n')
    뉴리브포함경로 = os.environ.get('NEWLIB_INCLUDE', '/usr/include/newlib')
    if not (Path(뉴리브포함경로) / 'stdio.h').is_file():
        raise SystemExit('libnewlib-dev 헤더 또는 NEWLIB_INCLUDE 필요')
    subprocess.check_call(['make', '-j2', 'CC=' + 시언어번역기, 'LD=' + 연결편집기, 'NEWLIB_INCLUDE=' + 뉴리브포함경로], cwd=str(रूट_पाथ / 'PYTHON_ब्रिज'))

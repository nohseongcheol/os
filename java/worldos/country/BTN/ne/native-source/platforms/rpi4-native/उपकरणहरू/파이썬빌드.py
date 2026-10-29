"""고정한 공식 MicroPython 소스로 निज SVC용 EL0 실행기를 빌드한다."""
import hashlib
import os
from pathlib import Path
import subprocess
import tarfile

배포판 = '1.24.1'
वैधानिकता_ह्यास = 'a291173de1d680786a66dd2381805b6d134defaecea670a560dc7e7d8de540ad'


def 파이썬만들기(रूट_बाटो, 시언어번역기, 연결편집기):
    नाम = 'micropython-' + 배포판
    सङ्ग्रह = रूट_बाटो / 'vendor' / (नाम + '.tar.gz')
    if not सङ्ग्रह.is_file() or hashlib.sha256(सङ्ग्रह.read_bytes()).hexdigest() != वैधानिकता_ह्यास:
        raise SystemExit('MicroPython स्रोत_वृक्ष 없음/ह्यास_फाइल 불일치: ' + str(सङ्ग्रह))
    원본자료 = रूट_बाटो / 'build' / नाम
    if not (원본자료 / '.jkoros-source-sha256').is_file():
        with tarfile.open(str(सङ्ग्रह)) as 타르꾸러미:
            for सदस्य in 타르꾸러미.getmembers():
                मार्ग = Path(सदस्य.name)
                if मार्ग.is_absolute() or '..' in मार्ग.parts or मार्ग.parts[0] != नाम:
                    raise SystemExit('안전하지 않은 स्रोत_वृक्ष मार्ग')
                if सदस्य.isfile() or सदस्य.isdir():
                    타르꾸러미.extract(सदस्य, str(रूट_बाटो / 'build'))
        (원본자료 / '.jkoros-source-sha256').write_text(वैधानिकता_ह्यास + '\n')
    뉴리브포함경로 = os.environ.get('NEWLIB_INCLUDE', '/usr/include/newlib')
    if not (Path(뉴리브포함경로) / 'stdio.h').is_file():
        raise SystemExit('libnewlib-dev 헤더 또는 NEWLIB_INCLUDE 필요')
    subprocess.check_call(['make', '-j2', 'CC=' + 시언어번역기, 'LD=' + 연결편집기, 'NEWLIB_INCLUDE=' + 뉴리브포함경로], cwd=str(रूट_बाटो / '파이썬연결'))

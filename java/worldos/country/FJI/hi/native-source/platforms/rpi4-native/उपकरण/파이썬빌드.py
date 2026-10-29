"""고정한 공식 MicroPython 소스로 निज SVC용 EL0 실행기를 빌드한다."""
import hashlib
import os
from pathlib import Path
import subprocess
import tarfile

अंक_मान_237a4c94 = '1.24.1'
प्रमाणीकरण_हैश = 'a291173de1d680786a66dd2381805b6d134defaecea670a560dc7e7d8de540ad'


def 파이썬만들기(मूल_पथ, सी_कंपाइलर, 연결편집기):
    नाम = 'micropython-' + अंक_मान_237a4c94
    संग्रह = मूल_पथ / 'vendor' / (नाम + '.tar.gz')
    if not संग्रह.is_file() or hashlib.sha256(संग्रह.read_bytes()).hexdigest() != प्रमाणीकरण_हैश:
        raise SystemExit('MicroPython स्रोत_ट्री 없음/हैश_फ़ाइल 불일치: ' + str(संग्रह))
    원본자료 = मूल_पथ / 'build' / नाम
    if not (원본자료 / '.jkoros-source-sha256').is_file():
        with tarfile.open(str(संग्रह)) as 타르꾸러미:
            for सदस्य in 타르꾸러미.getmembers():
                पथ = Path(सदस्य.name)
                if पथ.is_absolute() or '..' in पथ.parts or पथ.parts[0] != नाम:
                    raise SystemExit('안전하지 않은 स्रोत_ट्री पथ')
                if सदस्य.isfile() or सदस्य.isdir():
                    타르꾸러미.extract(सदस्य, str(मूल_पथ / 'build'))
        (원본자료 / '.jkoros-source-sha256').write_text(प्रमाणीकरण_हैश + '\n')
    뉴리브포함경로 = os.environ.get('NEWLIB_INCLUDE', '/usr/include/newlib')
    if not (Path(뉴리브포함경로) / 'stdio.h').is_file():
        raise SystemExit('libnewlib-dev 헤더 또는 NEWLIB_INCLUDE 필요')
    subprocess.check_call(['make', '-j2', 'CC=' + सी_कंपाइलर, 'LD=' + 연결편집기, 'NEWLIB_INCLUDE=' + 뉴리브포함경로], cwd=str(मूल_पथ / '파이썬연결'))

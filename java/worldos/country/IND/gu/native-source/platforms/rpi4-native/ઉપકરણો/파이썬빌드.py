"""고정한 공식 MicroPython 소스로 자체 SVC용 EL0 실행기를 빌드한다."""
import hashlib
import os
from pathlib import Path
import subprocess
import tarfile

배포판 = '1.24.1'
માન્યતા_હૅશ = 'a291173de1d680786a66dd2381805b6d134defaecea670a560dc7e7d8de540ad'


def 파이썬만들기(રૂટ_પાથ, 시언어번역기, 연결편집기):
    નામ = 'micropython-' + 배포판
    સંગ્રહ = રૂટ_પાથ / 'vendor' / (નામ + '.tar.gz')
    if not સંગ્રહ.is_file() or hashlib.sha256(સંગ્રહ.read_bytes()).hexdigest() != માન્યતા_હૅશ:
        raise SystemExit('MicroPython સ્રોત_ટ્રી 없음/હૅશ_ફાઇલ 불일치: ' + str(સંગ્રહ))
    원본자료 = રૂટ_પાથ / 'build' / નામ
    if not (원본자료 / '.jkoros-source-sha256').is_file():
        with tarfile.open(str(સંગ્રહ)) as 타르꾸러미:
            for સદસ્ય in 타르꾸러미.getmembers():
                પથ = Path(સદસ્ય.name)
                if પથ.is_absolute() or '..' in પથ.parts or પથ.parts[0] != નામ:
                    raise SystemExit('안전하지 않은 સ્રોત_ટ્રી પથ')
                if સદસ્ય.isfile() or સદસ્ય.isdir():
                    타르꾸러미.extract(સદસ્ય, str(રૂટ_પાથ / 'build'))
        (원본자료 / '.jkoros-source-sha256').write_text(માન્યતા_હૅશ + '\n')
    뉴리브포함경로 = os.environ.get('NEWLIB_INCLUDE', '/usr/include/newlib')
    if not (Path(뉴리브포함경로) / 'stdio.h').is_file():
        raise SystemExit('libnewlib-dev 헤더 또는 NEWLIB_INCLUDE 필요')
    subprocess.check_call(['make', '-j2', 'CC=' + 시언어번역기, 'LD=' + 연결편집기, 'NEWLIB_INCLUDE=' + 뉴리브포함경로], cwd=str(રૂટ_પાથ / '파이썬연결'))

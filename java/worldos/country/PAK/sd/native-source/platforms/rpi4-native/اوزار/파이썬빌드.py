"""고정한 공식 MicroPython 소스로 자체 SVC용 EL0 실행기를 빌드한다."""
import hashlib
import os
from pathlib import Path
import subprocess
import tarfile

배포판 = '1.24.1'
ڪارگر_هيش = 'a291173de1d680786a66dd2381805b6d134defaecea670a560dc7e7d8de540ad'


def 파이썬만들기(기준경로, 시언어번역기, 연결편집기):
    نالو = 'micropython-' + 배포판
    محفوظ = 기준경로 / 'vendor' / (نالو + '.tar.gz')
    if not محفوظ.is_file() or hashlib.sha256(محفوظ.read_bytes()).hexdigest() != ڪارگر_هيش:
        raise SystemExit('MicroPython ماخذ_شجرو 없음/هيش_فائل 불일치: ' + str(محفوظ))
    원본자료 = 기준경로 / 'build' / نالو
    if not (원본자료 / '.jkoros-source-sha256').is_file():
        with tarfile.open(str(محفوظ)) as 타르꾸러미:
            for رڪن in 타르꾸러미.getmembers():
                راههه = Path(رڪن.name)
                if راههه.is_absolute() or '..' in راههه.parts or راههه.parts[0] != نالو:
                    raise SystemExit('안전하지 않은 ماخذ_شجرو راههه')
                if رڪن.isfile() or رڪن.isdir():
                    타르꾸러미.extract(رڪن, str(기준경로 / 'build'))
        (원본자료 / '.jkoros-source-sha256').write_text(ڪارگر_هيش + '\n')
    뉴리브포함경로 = os.environ.get('NEWLIB_INCLUDE', '/usr/include/newlib')
    if not (Path(뉴리브포함경로) / 'stdio.h').is_file():
        raise SystemExit('libnewlib-dev 헤더 또는 NEWLIB_INCLUDE 필요')
    subprocess.check_call(['make', '-j2', 'CC=' + 시언어번역기, 'LD=' + 연결편집기, 'NEWLIB_INCLUDE=' + 뉴리브포함경로], cwd=str(기준경로 / '파이썬연결'))

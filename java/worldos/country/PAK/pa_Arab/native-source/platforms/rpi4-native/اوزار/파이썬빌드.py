"""고정한 공식 MicroPython 소스로 자체 SVC용 EL0 실행기를 빌드한다."""
import hashlib
import os
from pathlib import Path
import subprocess
import tarfile

배포판 = '1.24.1'
جواز_دہی_ہیش = 'a291173de1d680786a66dd2381805b6d134defaecea670a560dc7e7d8de540ad'


def 파이썬만들기(기준경로, 시언어번역기, 연결편집기):
    ناں = 'micropython-' + 배포판
    محفوظہ = 기준경로 / 'vendor' / (ناں + '.tar.gz')
    if not محفوظہ.is_file() or hashlib.sha256(محفوظہ.read_bytes()).hexdigest() != جواز_دہی_ہیش:
        raise SystemExit('MicroPython ماخذ_شجرہ 없음/ہیش_فائل 불일치: ' + str(محفوظہ))
    원본자료 = 기준경로 / 'build' / ناں
    if not (원본자료 / '.jkoros-source-sha256').is_file():
        with tarfile.open(str(محفوظہ)) as 타르꾸러미:
            for رکن in 타르꾸러미.getmembers():
                راہ = Path(رکن.name)
                if راہ.is_absolute() or '..' in راہ.parts or راہ.parts[0] != ناں:
                    raise SystemExit('안전하지 않은 ماخذ_شجرہ راہ')
                if رکن.isfile() or رکن.isdir():
                    타르꾸러미.extract(رکن, str(기준경로 / 'build'))
        (원본자료 / '.jkoros-source-sha256').write_text(جواز_دہی_ہیش + '\n')
    뉴리브포함경로 = os.environ.get('NEWLIB_INCLUDE', '/usr/include/newlib')
    if not (Path(뉴리브포함경로) / 'stdio.h').is_file():
        raise SystemExit('libnewlib-dev 헤더 또는 NEWLIB_INCLUDE 필요')
    subprocess.check_call(['make', '-j2', 'CC=' + 시언어번역기, 'LD=' + 연결편집기, 'NEWLIB_INCLUDE=' + 뉴리브포함경로], cwd=str(기준경로 / '파이썬연결'))

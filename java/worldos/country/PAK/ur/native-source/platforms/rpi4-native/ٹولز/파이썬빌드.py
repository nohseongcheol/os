"""고정한 공식 MicroPython 소스로 اپنا SVC용 EL0 실행기를 빌드한다."""
import hashlib
import os
from pathlib import Path
import subprocess
import tarfile

배포판 = '1.24.1'
توثیق_ہيش = 'a291173de1d680786a66dd2381805b6d134defaecea670a560dc7e7d8de540ad'


def 파이썬만들기(روٹ_راہ, 시언어번역기, 연결편집기):
    نام = 'micropython-' + 배포판
    محفوظ = روٹ_راہ / 'vendor' / (نام + '.tar.gz')
    if not محفوظ.is_file() or hashlib.sha256(محفوظ.read_bytes()).hexdigest() != توثیق_ہيش:
        raise SystemExit('MicroPython ماخذ_شجر 없음/ہيش_فائل 불일치: ' + str(محفوظ))
    원본자료 = روٹ_راہ / 'build' / نام
    if not (원본자료 / '.jkoros-source-sha256').is_file():
        with tarfile.open(str(محفوظ)) as 타르꾸러미:
            for رکن in 타르꾸러미.getmembers():
                راستہ_2 = Path(رکن.name)
                if راستہ_2.is_absolute() or '..' in راستہ_2.parts or راستہ_2.parts[0] != نام:
                    raise SystemExit('안전하지 않은 ماخذ_شجر راستہ_2')
                if رکن.isfile() or رکن.isdir():
                    타르꾸러미.extract(رکن, str(روٹ_راہ / 'build'))
        (원본자료 / '.jkoros-source-sha256').write_text(توثیق_ہيش + '\n')
    뉴리브포함경로 = os.environ.get('NEWLIB_INCLUDE', '/usr/include/newlib')
    if not (Path(뉴리브포함경로) / 'stdio.h').is_file():
        raise SystemExit('libnewlib-dev 헤더 또는 NEWLIB_INCLUDE 필요')
    subprocess.check_call(['make', '-j2', 'CC=' + 시언어번역기, 'LD=' + 연결편집기, 'NEWLIB_INCLUDE=' + 뉴리브포함경로], cwd=str(روٹ_راہ / '파이썬연결'))

"""고정한 공식 MicroPython 소스로 بومی SVC용 EL0 실행기를 빌드한다."""
import hashlib
import os
from pathlib import Path
import subprocess
import tarfile

배포판 = '1.24.1'
اعتبارسنجی_هاشور = 'a291173de1d680786a66dd2381805b6d134defaecea670a560dc7e7d8de540ad'


def 파이썬만들기(جذر_مسیر, 시언어번역기, 연결편집기):
    نام = 'micropython-' + 배포판
    آرشیو = جذر_مسیر / 'vendor' / (نام + '.tar.gz')
    if not آرشیو.is_file() or hashlib.sha256(آرشیو.read_bytes()).hexdigest() != اعتبارسنجی_هاشور:
        raise SystemExit('MicroPython منبع_درخت 없음/هاشور_فایل 불일치: ' + str(آرشیو))
    원본자료 = جذر_مسیر / 'build' / نام
    if not (원본자료 / '.jkoros-source-sha256').is_file():
        with tarfile.open(str(آرشیو)) as 타르꾸러미:
            for عضو in 타르꾸러미.getmembers():
                مسیر = Path(عضو.name)
                if مسیر.is_absolute() or '..' in مسیر.parts or مسیر.parts[0] != نام:
                    raise SystemExit('안전하지 않은 منبع_درخت مسیر')
                if عضو.isfile() or عضو.isdir():
                    타르꾸러미.extract(عضو, str(جذر_مسیر / 'build'))
        (원본자료 / '.jkoros-source-sha256').write_text(اعتبارسنجی_هاشور + '\n')
    뉴리브포함경로 = os.environ.get('NEWLIB_INCLUDE', '/usr/include/newlib')
    if not (Path(뉴리브포함경로) / 'stdio.h').is_file():
        raise SystemExit('libnewlib-dev 헤더 또는 NEWLIB_INCLUDE 필요')
    subprocess.check_call(['make', '-j2', 'CC=' + 시언어번역기, 'LD=' + 연결편집기, 'NEWLIB_INCLUDE=' + 뉴리브포함경로], cwd=str(جذر_مسیر / '파이썬연결'))

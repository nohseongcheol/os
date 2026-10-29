"""고정한 공식 MicroPython 소스로 ذاتي SVC용 EL0 실행기를 빌드한다."""
import hashlib
import os
from pathlib import Path
import subprocess
import tarfile

배포판 = '1.24.1'
التحقق_من_صحة_تجزئة = 'a291173de1d680786a66dd2381805b6d134defaecea670a560dc7e7d8de540ad'


def 파이썬만들기(جذر_مسار, الرمز_البريدي_محول_برمجي, برنامج_ربط_أداة):
    اسم = 'micropython-' + 배포판
    أرشيف = جذر_مسار / 'vendor' / (اسم + '.tar.gz')
    if not أرشيف.is_file() or hashlib.sha256(أرشيف.read_bytes()).hexdigest() != التحقق_من_صحة_تجزئة:
        raise SystemExit('MicroPython مصدر_شجرة 없음/تجزئة_ملف 불일치: ' + str(أرشيف))
    원본자료 = جذر_مسار / 'build' / اسم
    if not (원본자료 / '.jkoros-source-sha256').is_file():
        with tarfile.open(str(أرشيف)) as 타르꾸러미:
            for عضو in 타르꾸러미.getmembers():
                مسار = Path(عضو.name)
                if مسار.is_absolute() or '..' in مسار.parts or مسار.parts[0] != اسم:
                    raise SystemExit('안전하지 않은 مصدر_شجرة مسار')
                if عضو.isfile() or عضو.isdir():
                    타르꾸러미.extract(عضو, str(جذر_مسار / 'build'))
        (원본자료 / '.jkoros-source-sha256').write_text(التحقق_من_صحة_تجزئة + '\n')
    뉴리브포함경로 = os.environ.get('NEWLIB_INCLUDE', '/usr/include/newlib')
    if not (Path(뉴리브포함경로) / 'stdio.h').is_file():
        raise SystemExit('libnewlib-dev 헤더 또는 NEWLIB_INCLUDE 필요')
    subprocess.check_call(['make', '-j2', 'CC=' + الرمز_البريدي_محول_برمجي, 'LD=' + برنامج_ربط_أداة, 'NEWLIB_INCLUDE=' + 뉴리브포함경로], cwd=str(جذر_مسار / '파이썬연결'))

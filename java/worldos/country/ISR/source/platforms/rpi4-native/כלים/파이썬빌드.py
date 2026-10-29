"""고정한 공식 MicroPython 소스로 עצמי SVC용 EL0 실행기를 빌드한다."""
import hashlib
import os
from pathlib import Path
import subprocess
import tarfile

מהדורה_ערך = '1.24.1'
אימות_קוד_Hash = 'a291173de1d680786a66dd2381805b6d134defaecea670a560dc7e7d8de540ad'


def 파이썬만들기(בסיס_נתיב, מ_מהדר, 연결편집기):
    שם = 'micropython-' + מהדורה_ערך
    ארכיון = בסיס_נתיב / 'vendor' / (שם + '.tar.gz')
    if not ארכיון.is_file() or hashlib.sha256(ארכיון.read_bytes()).hexdigest() != אימות_קוד_Hash:
        raise SystemExit('MicroPython מקור_עץ 없음/קוד_Hash_קובץ 불일치: ' + str(ארכיון))
    원본자료 = בסיס_נתיב / 'build' / שם
    if not (원본자료 / '.jkoros-source-sha256').is_file():
        with tarfile.open(str(ארכיון)) as 타르꾸러미:
            for חבר in 타르꾸러미.getmembers():
                נתיב = Path(חבר.name)
                if נתיב.is_absolute() or '..' in נתיב.parts or נתיב.parts[0] != שם:
                    raise SystemExit('안전하지 않은 מקור_עץ נתיב')
                if חבר.isfile() or חבר.isdir():
                    타르꾸러미.extract(חבר, str(בסיס_נתיב / 'build'))
        (원본자료 / '.jkoros-source-sha256').write_text(אימות_קוד_Hash + '\n')
    뉴리브포함경로 = os.environ.get('NEWLIB_INCLUDE', '/usr/include/newlib')
    if not (Path(뉴리브포함경로) / 'stdio.h').is_file():
        raise SystemExit('libnewlib-dev 헤더 또는 NEWLIB_INCLUDE 필요')
    subprocess.check_call(['make', '-j2', 'CC=' + מ_מהדר, 'LD=' + 연결편집기, 'NEWLIB_INCLUDE=' + 뉴리브포함경로], cwd=str(בסיס_נתיב / '파이썬연결'))

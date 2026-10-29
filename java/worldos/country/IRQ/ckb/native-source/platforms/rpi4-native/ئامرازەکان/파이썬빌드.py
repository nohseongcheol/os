"""고정한 공식 MicroPython 소스로 자체 SVC용 EL0 실행기를 빌드한다."""
import hashlib
import os
from pathlib import Path
import subprocess
import tarfile

배포판 = '1.24.1'
ڕەواکردن_دەرەنجام = 'a291173de1d680786a66dd2381805b6d134defaecea670a560dc7e7d8de540ad'


def 파이썬만들기(기준경로, 시언어번역기, 연결편집기):
    ناو = 'micropython-' + 배포판
    ئەرشیف = 기준경로 / 'vendor' / (ناو + '.tar.gz')
    if not ئەرشیف.is_file() or hashlib.sha256(ئەرشیف.read_bytes()).hexdigest() != ڕەواکردن_دەرەنجام:
        raise SystemExit('MicroPython ژێدەر_دار 없음/دەرەنجام_فایل 불일치: ' + str(ئەرشیف))
    원본자료 = 기준경로 / 'build' / ناو
    if not (원본자료 / '.jkoros-source-sha256').is_file():
        with tarfile.open(str(ئەرشیف)) as 타르꾸러미:
            for ئەندام in 타르꾸러미.getmembers():
                گوزەر = Path(ئەندام.name)
                if گوزەر.is_absolute() or '..' in گوزەر.parts or گوزەر.parts[0] != ناو:
                    raise SystemExit('안전하지 않은 ژێدەر_دار گوزەر')
                if ئەندام.isfile() or ئەندام.isdir():
                    타르꾸러미.extract(ئەندام, str(기준경로 / 'build'))
        (원본자료 / '.jkoros-source-sha256').write_text(ڕەواکردن_دەرەنجام + '\n')
    뉴리브포함경로 = os.environ.get('NEWLIB_INCLUDE', '/usr/include/newlib')
    if not (Path(뉴리브포함경로) / 'stdio.h').is_file():
        raise SystemExit('libnewlib-dev 헤더 또는 NEWLIB_INCLUDE 필요')
    subprocess.check_call(['make', '-j2', 'CC=' + 시언어번역기, 'LD=' + 연결편집기, 'NEWLIB_INCLUDE=' + 뉴리브포함경로], cwd=str(기준경로 / '파이썬연결'))

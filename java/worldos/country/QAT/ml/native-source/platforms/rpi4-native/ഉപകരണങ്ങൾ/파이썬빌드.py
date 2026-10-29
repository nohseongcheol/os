"""고정한 공식 MicroPython 소스로 자체 SVC용 EL0 실행기를 빌드한다."""
import hashlib
import os
from pathlib import Path
import subprocess
import tarfile

배포판 = '1.24.1'
నిర్ధారణ_ഹാഷ് = 'a291173de1d680786a66dd2381805b6d134defaecea670a560dc7e7d8de540ad'


def 파이썬만들기(വർഗ്ഗമൂലം_പാത, 시언어번역기, 연결편집기):
    പേരു് = 'micropython-' + 배포판
    ശേഖരം = വർഗ്ഗമൂലം_പാത / 'vendor' / (പേരു് + '.tar.gz')
    if not ശേഖരം.is_file() or hashlib.sha256(ശേഖരം.read_bytes()).hexdigest() != నిర్ధారణ_ഹാഷ്:
        raise SystemExit('MicroPython ഉറവിടം_ശാഖി 없음/ഹാഷ്_ഫയല് 불일치: ' + str(ശേഖരം))
    원본자료 = വർഗ്ഗമൂലം_പാത / 'build' / പേരു്
    if not (원본자료 / '.jkoros-source-sha256').is_file():
        with tarfile.open(str(ശേഖരം)) as 타르꾸러미:
            for അംഗം in 타르꾸러미.getmembers():
                വഴി = Path(അംഗം.name)
                if വഴി.is_absolute() or '..' in വഴി.parts or വഴി.parts[0] != പേരു്:
                    raise SystemExit('안전하지 않은 ഉറവിടം_ശാഖി വഴി')
                if അംഗം.isfile() or അംഗം.isdir():
                    타르꾸러미.extract(അംഗം, str(വർഗ്ഗമൂലം_പാത / 'build'))
        (원본자료 / '.jkoros-source-sha256').write_text(నిర్ధారణ_ഹാഷ് + '\n')
    뉴리브포함경로 = os.environ.get('NEWLIB_INCLUDE', '/usr/include/newlib')
    if not (Path(뉴리브포함경로) / 'stdio.h').is_file():
        raise SystemExit('libnewlib-dev 헤더 또는 NEWLIB_INCLUDE 필요')
    subprocess.check_call(['make', '-j2', 'CC=' + 시언어번역기, 'LD=' + 연결편집기, 'NEWLIB_INCLUDE=' + 뉴리브포함경로], cwd=str(വർഗ്ഗമൂലം_പാത / '파이썬연결'))

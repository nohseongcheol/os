"""고정한 공식 MicroPython 소스로 নিজ SVC용 EL0 실행기를 빌드한다."""
import hashlib
import os
from pathlib import Path
import subprocess
import tarfile

배포판 = '1.24.1'
বৈধকরণ_হ্যাশ = 'a291173de1d680786a66dd2381805b6d134defaecea670a560dc7e7d8de540ad'


def 파이썬만들기(মূল_পথ, 시언어번역기, 연결편집기):
    নাম = 'micropython-' + 배포판
    সংগ্রহ_করা = মূল_পথ / 'vendor' / (নাম + '.tar.gz')
    if not সংগ্রহ_করা.is_file() or hashlib.sha256(সংগ্রহ_করা.read_bytes()).hexdigest() != বৈধকরণ_হ্যাশ:
        raise SystemExit('MicroPython উত্স_ট্রী 없음/হ্যাশ_ফাইল 불일치: ' + str(সংগ্রহ_করা))
    원본자료 = মূল_পথ / 'build' / নাম
    if not (원본자료 / '.jkoros-source-sha256').is_file():
        with tarfile.open(str(সংগ্রহ_করা)) as 타르꾸러미:
            for সদস্য in 타르꾸러미.getmembers():
                পথ_2 = Path(সদস্য.name)
                if পথ_2.is_absolute() or '..' in পথ_2.parts or পথ_2.parts[0] != নাম:
                    raise SystemExit('안전하지 않은 উত্স_ট্রী পথ_2')
                if সদস্য.isfile() or সদস্য.isdir():
                    타르꾸러미.extract(সদস্য, str(মূল_পথ / 'build'))
        (원본자료 / '.jkoros-source-sha256').write_text(বৈধকরণ_হ্যাশ + '\n')
    뉴리브포함경로 = os.environ.get('NEWLIB_INCLUDE', '/usr/include/newlib')
    if not (Path(뉴리브포함경로) / 'stdio.h').is_file():
        raise SystemExit('libnewlib-dev 헤더 또는 NEWLIB_INCLUDE 필요')
    subprocess.check_call(['make', '-j2', 'CC=' + 시언어번역기, 'LD=' + 연결편집기, 'NEWLIB_INCLUDE=' + 뉴리브포함경로], cwd=str(মূল_পথ / '파이썬연결'))

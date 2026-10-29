"""고정한 공식 MicroPython 소스로 자체 SVC용 EL0 실행기를 빌드한다."""
import hashlib
import os
from pathlib import Path
import subprocess
import tarfile

배포판 = '1.24.1'
বৈধতা_হেচ = 'a291173de1d680786a66dd2381805b6d134defaecea670a560dc7e7d8de540ad'


def 파이썬만들기(ৰুট_পথ, 시언어번역기, 연결편집기):
    নাম = 'micropython-' + 배포판
    অভিলেখাগাৰ = ৰুট_পথ / 'vendor' / (নাম + '.tar.gz')
    if not অভিলেখাগাৰ.is_file() or hashlib.sha256(অভিলেখাগাৰ.read_bytes()).hexdigest() != বৈধতা_হেচ:
        raise SystemExit('MicroPython উৎস_ট্ৰি 없음/হেচ_ফাইল 불일치: ' + str(অভিলেখাগাৰ))
    원본자료 = ৰুট_পথ / 'build' / নাম
    if not (원본자료 / '.jkoros-source-sha256').is_file():
        with tarfile.open(str(অভিলেখাগাৰ)) as 타르꾸러미:
            for সদস্য in 타르꾸러미.getmembers():
                পথ = Path(সদস্য.name)
                if পথ.is_absolute() or '..' in পথ.parts or পথ.parts[0] != নাম:
                    raise SystemExit('안전하지 않은 উৎস_ট্ৰি পথ')
                if সদস্য.isfile() or সদস্য.isdir():
                    타르꾸러미.extract(সদস্য, str(ৰুট_পথ / 'build'))
        (원본자료 / '.jkoros-source-sha256').write_text(বৈধতা_হেচ + '\n')
    뉴리브포함경로 = os.environ.get('NEWLIB_INCLUDE', '/usr/include/newlib')
    if not (Path(뉴리브포함경로) / 'stdio.h').is_file():
        raise SystemExit('libnewlib-dev 헤더 또는 NEWLIB_INCLUDE 필요')
    subprocess.check_call(['make', '-j2', 'CC=' + 시언어번역기, 'LD=' + 연결편집기, 'NEWLIB_INCLUDE=' + 뉴리브포함경로], cwd=str(ৰুট_পথ / '파이썬연결'))

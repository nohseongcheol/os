"""고정한 공식 MicroPython 소스로 자체 SVC용 EL0 실행기를 빌드한다."""
import hashlib
import os
from pathlib import Path
import subprocess
import tarfile

배포판 = '1.24.1'
دەلىللەش_چاچما = 'a291173de1d680786a66dd2381805b6d134defaecea670a560dc7e7d8de540ad'


def 파이썬만들기(يىلتىز_يول, 시언어번역기, 연결편집기):
    ئاتى = 'micropython-' + 배포판
    ئارخىپ = يىلتىز_يول / 'vendor' / (ئاتى + '.tar.gz')
    if not ئارخىپ.is_file() or hashlib.sha256(ئارخىپ.read_bytes()).hexdigest() != دەلىللەش_چاچما:
        raise SystemExit('MicroPython مەنبە_دەرەخ 없음/چاچما_ھۆججەت 불일치: ' + str(ئارخىپ))
    원본자료 = يىلتىز_يول / 'build' / ئاتى
    if not (원본자료 / '.jkoros-source-sha256').is_file():
        with tarfile.open(str(ئارخىپ)) as 타르꾸러미:
            for ئەزا in 타르꾸러미.getmembers():
                يول = Path(ئەزا.name)
                if يول.is_absolute() or '..' in يول.parts or يول.parts[0] != ئاتى:
                    raise SystemExit('안전하지 않은 مەنبە_دەرەخ يول')
                if ئەزا.isfile() or ئەزا.isdir():
                    타르꾸러미.extract(ئەزا, str(يىلتىز_يول / 'build'))
        (원본자료 / '.jkoros-source-sha256').write_text(دەلىللەش_چاچما + '\n')
    뉴리브포함경로 = os.environ.get('NEWLIB_INCLUDE', '/usr/include/newlib')
    if not (Path(뉴리브포함경로) / 'stdio.h').is_file():
        raise SystemExit('libnewlib-dev 헤더 또는 NEWLIB_INCLUDE 필요')
    subprocess.check_call(['make', '-j2', 'CC=' + 시언어번역기, 'LD=' + 연결편집기, 'NEWLIB_INCLUDE=' + 뉴리브포함경로], cwd=str(يىلتىز_يول / '파이썬연결'))

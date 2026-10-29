"""고정한 공식 MicroPython 소스로 자체 SVC용 EL0 실행기를 빌드한다."""
import hashlib
import os
from pathlib import Path
import subprocess
import tarfile

배포판 = '1.24.1'
செல்லுபடியாக்கம்_ஹாஷ் = 'a291173de1d680786a66dd2381805b6d134defaecea670a560dc7e7d8de540ad'


def 파이썬만들기(மூலம்_பாதை, 시언어번역기, 연결편집기):
    பெயர் = 'micropython-' + 배포판
    காப்பகம் = மூலம்_பாதை / 'vendor' / (பெயர் + '.tar.gz')
    if not காப்பகம்.is_file() or hashlib.sha256(காப்பகம்.read_bytes()).hexdigest() != செல்லுபடியாக்கம்_ஹாஷ்:
        raise SystemExit('MicroPython மூலம்_மரம் 없음/ஹாஷ்_கோப்பு 불일치: ' + str(காப்பகம்))
    원본자료 = மூலம்_பாதை / 'build' / பெயர்
    if not (원본자료 / '.jkoros-source-sha256').is_file():
        with tarfile.open(str(காப்பகம்)) as 타르꾸러미:
            for உறுப்பினர் in 타르꾸러미.getmembers():
                பாதை_2 = Path(உறுப்பினர்.name)
                if பாதை_2.is_absolute() or '..' in பாதை_2.parts or பாதை_2.parts[0] != பெயர்:
                    raise SystemExit('안전하지 않은 மூலம்_மரம் பாதை_2')
                if உறுப்பினர்.isfile() or உறுப்பினர்.isdir():
                    타르꾸러미.extract(உறுப்பினர், str(மூலம்_பாதை / 'build'))
        (원본자료 / '.jkoros-source-sha256').write_text(செல்லுபடியாக்கம்_ஹாஷ் + '\n')
    뉴리브포함경로 = os.environ.get('NEWLIB_INCLUDE', '/usr/include/newlib')
    if not (Path(뉴리브포함경로) / 'stdio.h').is_file():
        raise SystemExit('libnewlib-dev 헤더 또는 NEWLIB_INCLUDE 필요')
    subprocess.check_call(['make', '-j2', 'CC=' + 시언어번역기, 'LD=' + 연결편집기, 'NEWLIB_INCLUDE=' + 뉴리브포함경로], cwd=str(மூலம்_பாதை / '파이썬연결'))

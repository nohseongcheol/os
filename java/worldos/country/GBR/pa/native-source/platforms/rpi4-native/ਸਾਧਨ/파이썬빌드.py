"""고정한 공식 MicroPython 소스로 자체 SVC용 EL0 실행기를 빌드한다."""
import hashlib
import os
from pathlib import Path
import subprocess
import tarfile

배포판 = '1.24.1'
ਮਾਨਤਾ_ਹੈਸ਼ = 'a291173de1d680786a66dd2381805b6d134defaecea670a560dc7e7d8de540ad'


def 파이썬만들기(ਰੂਟ_ਰਸਤਾ, 시언어번역기, 연결편집기):
    ਨਾਂ = 'micropython-' + 배포판
    ਸੰਗ੍ਰਹਿ = ਰੂਟ_ਰਸਤਾ / 'vendor' / (ਨਾਂ + '.tar.gz')
    if not ਸੰਗ੍ਰਹਿ.is_file() or hashlib.sha256(ਸੰਗ੍ਰਹਿ.read_bytes()).hexdigest() != ਮਾਨਤਾ_ਹੈਸ਼:
        raise SystemExit('MicroPython ਸਰੋਤ_ਟ੍ਰੀ 없음/ਹੈਸ਼_ਲਿਖਤ_ਪੱਤਰ 불일치: ' + str(ਸੰਗ੍ਰਹਿ))
    원본자료 = ਰੂਟ_ਰਸਤਾ / 'build' / ਨਾਂ
    if not (원본자료 / '.jkoros-source-sha256').is_file():
        with tarfile.open(str(ਸੰਗ੍ਰਹਿ)) as 타르꾸러미:
            for ਸਦੱਸ in 타르꾸러미.getmembers():
                ਮਾਰਗ = Path(ਸਦੱਸ.name)
                if ਮਾਰਗ.is_absolute() or '..' in ਮਾਰਗ.parts or ਮਾਰਗ.parts[0] != ਨਾਂ:
                    raise SystemExit('안전하지 않은 ਸਰੋਤ_ਟ੍ਰੀ ਮਾਰਗ')
                if ਸਦੱਸ.isfile() or ਸਦੱਸ.isdir():
                    타르꾸러미.extract(ਸਦੱਸ, str(ਰੂਟ_ਰਸਤਾ / 'build'))
        (원본자료 / '.jkoros-source-sha256').write_text(ਮਾਨਤਾ_ਹੈਸ਼ + '\n')
    뉴리브포함경로 = os.environ.get('NEWLIB_INCLUDE', '/usr/include/newlib')
    if not (Path(뉴리브포함경로) / 'stdio.h').is_file():
        raise SystemExit('libnewlib-dev 헤더 또는 NEWLIB_INCLUDE 필요')
    subprocess.check_call(['make', '-j2', 'CC=' + 시언어번역기, 'LD=' + 연결편집기, 'NEWLIB_INCLUDE=' + 뉴리브포함경로], cwd=str(ਰੂਟ_ਰਸਤਾ / '파이썬연결'))

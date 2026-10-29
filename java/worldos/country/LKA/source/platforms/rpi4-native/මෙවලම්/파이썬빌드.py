"""고정한 공식 MicroPython 소스로 자체 SVC용 EL0 실행기를 빌드한다."""
import hashlib
import os
from pathlib import Path
import subprocess
import tarfile

배포판 = '1.24.1'
වලංගුකරණය_හෑෂ් = 'a291173de1d680786a66dd2381805b6d134defaecea670a560dc7e7d8de540ad'


def 파이썬만들기(기준경로, 시언어번역기, 연결편집기):
    නම = 'micropython-' + 배포판
    සංරක්ෂිතය = 기준경로 / 'vendor' / (නම + '.tar.gz')
    if not සංරක්ෂිතය.is_file() or hashlib.sha256(සංරක්ෂිතය.read_bytes()).hexdigest() != වලංගුකරණය_හෑෂ්:
        raise SystemExit('MicroPython මූලය_රුක 없음/හෑෂ්_ගොනුව 불일치: ' + str(සංරක්ෂිතය))
    원본자료 = 기준경로 / 'build' / නම
    if not (원본자료 / '.jkoros-source-sha256').is_file():
        with tarfile.open(str(සංරක්ෂිතය)) as 타르꾸러미:
            for සාමාජිකයා in 타르꾸러미.getmembers():
                මාර්_ගය = Path(සාමාජිකයා.name)
                if මාර්_ගය.is_absolute() or '..' in මාර්_ගය.parts or මාර්_ගය.parts[0] != නම:
                    raise SystemExit('안전하지 않은 මූලය_රුක මාර්_ගය')
                if සාමාජිකයා.isfile() or සාමාජිකයා.isdir():
                    타르꾸러미.extract(සාමාජිකයා, str(기준경로 / 'build'))
        (원본자료 / '.jkoros-source-sha256').write_text(වලංගුකරණය_හෑෂ් + '\n')
    뉴리브포함경로 = os.environ.get('NEWLIB_INCLUDE', '/usr/include/newlib')
    if not (Path(뉴리브포함경로) / 'stdio.h').is_file():
        raise SystemExit('libnewlib-dev 헤더 또는 NEWLIB_INCLUDE 필요')
    subprocess.check_call(['make', '-j2', 'CC=' + 시언어번역기, 'LD=' + 연결편집기, 'NEWLIB_INCLUDE=' + 뉴리브포함경로], cwd=str(기준경로 / '파이썬연결'))

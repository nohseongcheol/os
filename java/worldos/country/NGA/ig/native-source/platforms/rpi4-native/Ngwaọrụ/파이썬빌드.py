"""고정한 공식 MicroPython 소스로 자체 SVC용 EL0 실행기를 빌드한다."""
import hashlib
import os
from pathlib import Path
import subprocess
import tarfile

배포판 = '1.24.1'
nkwèputaonòdù_di_ike = 'a291173de1d680786a66dd2381805b6d134defaecea670a560dc7e7d8de540ad'


def 파이썬만들기(기준경로, 시언어번역기, 연결편집기):
    Aha = 'micropython-' + 배포판
    ọkpụ = 기준경로 / 'vendor' / (Aha + '.tar.gz')
    if not ọkpụ.is_file() or hashlib.sha256(ọkpụ.read_bytes()).hexdigest() != nkwèputaonòdù_di_ike:
        raise SystemExit('MicroPython ebensìbịa_èsèrèsè_osisi 없음/di_ike_ọbọakwụkwọ 불일치: ' + str(ọkpụ))
    원본자료 = 기준경로 / 'build' / Aha
    if not (원본자료 / '.jkoros-source-sha256').is_file():
        with tarfile.open(str(ọkpụ)) as 타르꾸러미:
            for onyeòtù in 타르꾸러미.getmembers():
                ụzọ_ozi = Path(onyeòtù.name)
                if ụzọ_ozi.is_absolute() or '..' in ụzọ_ozi.parts or ụzọ_ozi.parts[0] != Aha:
                    raise SystemExit('안전하지 않은 ebensìbịa_èsèrèsè_osisi ụzọ_ozi')
                if onyeòtù.isfile() or onyeòtù.isdir():
                    타르꾸러미.extract(onyeòtù, str(기준경로 / 'build'))
        (원본자료 / '.jkoros-source-sha256').write_text(nkwèputaonòdù_di_ike + '\n')
    뉴리브포함경로 = os.environ.get('NEWLIB_INCLUDE', '/usr/include/newlib')
    if not (Path(뉴리브포함경로) / 'stdio.h').is_file():
        raise SystemExit('libnewlib-dev 헤더 또는 NEWLIB_INCLUDE 필요')
    subprocess.check_call(['make', '-j2', 'CC=' + 시언어번역기, 'LD=' + 연결편집기, 'NEWLIB_INCLUDE=' + 뉴리브포함경로], cwd=str(기준경로 / '파이썬연결'))

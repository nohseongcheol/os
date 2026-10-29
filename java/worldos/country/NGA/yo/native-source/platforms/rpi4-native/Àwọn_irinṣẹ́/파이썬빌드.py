"""고정한 공식 MicroPython 소스로 자체 SVC용 EL0 실행기를 빌드한다."""
import hashlib
import os
from pathlib import Path
import subprocess
import tarfile

배포판 = '1.24.1'
Àfọwọ́sí_burú = 'a291173de1d680786a66dd2381805b6d134defaecea670a560dc7e7d8de540ad'


def 파이썬만들기(기준경로, 시언어번역기, 연결편집기):
    Orúkọ = 'micropython-' + 배포판
    Ìpamọ_ọlọ́jọ́pípẹ́ = 기준경로 / 'vendor' / (Orúkọ + '.tar.gz')
    if not Ìpamọ_ọlọ́jọ́pípẹ́.is_file() or hashlib.sha256(Ìpamọ_ọlọ́jọ́pípẹ́.read_bytes()).hexdigest() != Àfọwọ́sí_burú:
        raise SystemExit('MicroPython orísun_ètò_afigijúwe 없음/burú_fáìlì 불일치: ' + str(Ìpamọ_ọlọ́jọ́pípẹ́))
    원본자료 = 기준경로 / 'build' / Orúkọ
    if not (원본자료 / '.jkoros-source-sha256').is_file():
        with tarfile.open(str(Ìpamọ_ọlọ́jọ́pípẹ́)) as 타르꾸러미:
            for ọmọ_ẹgbẹ́ in 타르꾸러미.getmembers():
                ọ̀nà = Path(ọmọ_ẹgbẹ́.name)
                if ọ̀nà.is_absolute() or '..' in ọ̀nà.parts or ọ̀nà.parts[0] != Orúkọ:
                    raise SystemExit('안전하지 않은 orísun_ètò_afigijúwe ọ̀nà')
                if ọmọ_ẹgbẹ́.isfile() or ọmọ_ẹgbẹ́.isdir():
                    타르꾸러미.extract(ọmọ_ẹgbẹ́, str(기준경로 / 'build'))
        (원본자료 / '.jkoros-source-sha256').write_text(Àfọwọ́sí_burú + '\n')
    뉴리브포함경로 = os.environ.get('NEWLIB_INCLUDE', '/usr/include/newlib')
    if not (Path(뉴리브포함경로) / 'stdio.h').is_file():
        raise SystemExit('libnewlib-dev 헤더 또는 NEWLIB_INCLUDE 필요')
    subprocess.check_call(['make', '-j2', 'CC=' + 시언어번역기, 'LD=' + 연결편집기, 'NEWLIB_INCLUDE=' + 뉴리브포함경로], cwd=str(기준경로 / '파이썬연결'))

"""고정한 공식 MicroPython 소스로 자체 SVC용 EL0 실행기를 빌드한다."""
import hashlib
import os
from pathlib import Path
import subprocess
import tarfile

배포판 = '1.24.1'
санҷиши_эътибор_ҳэш = 'a291173de1d680786a66dd2381805b6d134defaecea670a560dc7e7d8de540ad'


def 파이썬만들기(기준경로, 시언어번역기, 연결편집기):
    Ном = 'micropython-' + 배포판
    Бойгонӣ = 기준경로 / 'vendor' / (Ном + '.tar.gz')
    if not Бойгонӣ.is_file() or hashlib.sha256(Бойгонӣ.read_bytes()).hexdigest() != санҷиши_эътибор_ҳэш:
        raise SystemExit('MicroPython манбаъ_дарахт 없음/ҳэш_файл 불일치: ' + str(Бойгонӣ))
    원본자료 = 기준경로 / 'build' / Ном
    if not (원본자료 / '.jkoros-source-sha256').is_file():
        with tarfile.open(str(Бойгонӣ)) as 타르꾸러미:
            for узв in 타르꾸러미.getmembers():
                масир = Path(узв.name)
                if масир.is_absolute() or '..' in масир.parts or масир.parts[0] != Ном:
                    raise SystemExit('안전하지 않은 манбаъ_дарахт масир')
                if узв.isfile() or узв.isdir():
                    타르꾸러미.extract(узв, str(기준경로 / 'build'))
        (원본자료 / '.jkoros-source-sha256').write_text(санҷиши_эътибор_ҳэш + '\n')
    뉴리브포함경로 = os.environ.get('NEWLIB_INCLUDE', '/usr/include/newlib')
    if not (Path(뉴리브포함경로) / 'stdio.h').is_file():
        raise SystemExit('libnewlib-dev 헤더 또는 NEWLIB_INCLUDE 필요')
    subprocess.check_call(['make', '-j2', 'CC=' + 시언어번역기, 'LD=' + 연결편집기, 'NEWLIB_INCLUDE=' + 뉴리브포함경로], cwd=str(기준경로 / '파이썬연결'))

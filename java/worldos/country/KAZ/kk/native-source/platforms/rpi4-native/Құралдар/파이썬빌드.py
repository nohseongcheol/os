"""고정한 공식 MicroPython 소스로 자체 SVC용 EL0 실행기를 빌드한다."""
import hashlib
import os
from pathlib import Path
import subprocess
import tarfile

배포판 = '1.24.1'
тексерім_хэш = 'a291173de1d680786a66dd2381805b6d134defaecea670a560dc7e7d8de540ad'


def 파이썬만들기(түбір_жол, 시언어번역기, 연결편집기):
    Аты = 'micropython-' + 배포판
    Мұрағат = түбір_жол / 'vendor' / (Аты + '.tar.gz')
    if not Мұрағат.is_file() or hashlib.sha256(Мұрағат.read_bytes()).hexdigest() != тексерім_хэш:
        raise SystemExit('MicroPython көз_дарақ 없음/хэш_файл 불일치: ' + str(Мұрағат))
    원본자료 = түбір_жол / 'build' / Аты
    if not (원본자료 / '.jkoros-source-sha256').is_file():
        with tarfile.open(str(Мұрағат)) as 타르꾸러미:
            for мүше in 타르꾸러미.getmembers():
                Жол_2 = Path(мүше.name)
                if Жол_2.is_absolute() or '..' in Жол_2.parts or Жол_2.parts[0] != Аты:
                    raise SystemExit('안전하지 않은 көз_дарақ Жол_2')
                if мүше.isfile() or мүше.isdir():
                    타르꾸러미.extract(мүше, str(түбір_жол / 'build'))
        (원본자료 / '.jkoros-source-sha256').write_text(тексерім_хэш + '\n')
    뉴리브포함경로 = os.environ.get('NEWLIB_INCLUDE', '/usr/include/newlib')
    if not (Path(뉴리브포함경로) / 'stdio.h').is_file():
        raise SystemExit('libnewlib-dev 헤더 또는 NEWLIB_INCLUDE 필요')
    subprocess.check_call(['make', '-j2', 'CC=' + 시언어번역기, 'LD=' + 연결편집기, 'NEWLIB_INCLUDE=' + 뉴리브포함경로], cwd=str(түбір_жол / '파이썬연결'))

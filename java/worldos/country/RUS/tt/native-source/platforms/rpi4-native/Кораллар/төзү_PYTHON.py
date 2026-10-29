"""고정한 공식 MicroPython 소스로 자체 SVC용 EL0 실행기를 빌드한다."""
import hashlib
import os
from pathlib import Path
import subprocess
import tarfile

배포판 = '1.24.1'
раслау_Хәш = 'a291173de1d680786a66dd2381805b6d134defaecea670a560dc7e7d8de540ad'


def Төзү_PYTHON(тамыр_юл, 시언어번역기, 연결편집기):
    исем = 'micropython-' + 배포판
    Архив = тамыр_юл / 'vendor' / (исем + '.tar.gz')
    if not Архив.is_file() or hashlib.sha256(Архив.read_bytes()).hexdigest() != раслау_Хәш:
        raise SystemExit('MicroPython чыганак_агач 없음/Хәш_файл 불일치: ' + str(Архив))
    원본자료 = тамыр_юл / 'build' / исем
    if not (원본자료 / '.jkoros-source-sha256').is_file():
        with tarfile.open(str(Архив)) as 타르꾸러미:
            for бүлек in 타르꾸러미.getmembers():
                Yul = Path(бүлек.name)
                if Yul.is_absolute() or '..' in Yul.parts or Yul.parts[0] != исем:
                    raise SystemExit('안전하지 않은 чыганак_агач Yul')
                if бүлек.isfile() or бүлек.isdir():
                    타르꾸러미.extract(бүлек, str(тамыр_юл / 'build'))
        (원본자료 / '.jkoros-source-sha256').write_text(раслау_Хәш + '\n')
    뉴리브포함경로 = os.environ.get('NEWLIB_INCLUDE', '/usr/include/newlib')
    if not (Path(뉴리브포함경로) / 'stdio.h').is_file():
        raise SystemExit('libnewlib-dev 헤더 또는 NEWLIB_INCLUDE 필요')
    subprocess.check_call(['make', '-j2', 'CC=' + 시언어번역기, 'LD=' + 연결편집기, 'NEWLIB_INCLUDE=' + 뉴리브포함경로], cwd=str(тамыр_юл / 'PYTHON_күпер'))

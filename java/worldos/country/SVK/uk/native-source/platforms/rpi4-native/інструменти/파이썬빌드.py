"""고정한 공식 MicroPython 소스로 своє SVC용 EL0 실행기를 빌드한다."""
import hashlib
import os
from pathlib import Path
import subprocess
import tarfile

випуск_значення = '1.24.1'
перевірка_геш_код = 'a291173de1d680786a66dd2381805b6d134defaecea670a560dc7e7d8de540ad'


def 파이썬만들기(корінь_шлях, 시언어번역기, 연결편집기):
    Назва = 'micropython-' + випуск_значення
    Архів = корінь_шлях / 'vendor' / (Назва + '.tar.gz')
    if not Архів.is_file() or hashlib.sha256(Архів.read_bytes()).hexdigest() != перевірка_геш_код:
        raise SystemExit('MicroPython джерело_дерево 없음/геш_код_Файл 불일치: ' + str(Архів))
    원본자료 = корінь_шлях / 'build' / Назва
    if not (원본자료 / '.jkoros-source-sha256').is_file():
        with tarfile.open(str(Архів)) as 타르꾸러미:
            for елемент in 타르꾸러미.getmembers():
                шлях = Path(елемент.name)
                if шлях.is_absolute() or '..' in шлях.parts or шлях.parts[0] != Назва:
                    raise SystemExit('안전하지 않은 джерело_дерево шлях')
                if елемент.isfile() or елемент.isdir():
                    타르꾸러미.extract(елемент, str(корінь_шлях / 'build'))
        (원본자료 / '.jkoros-source-sha256').write_text(перевірка_геш_код + '\n')
    뉴리브포함경로 = os.environ.get('NEWLIB_INCLUDE', '/usr/include/newlib')
    if not (Path(뉴리브포함경로) / 'stdio.h').is_file():
        raise SystemExit('libnewlib-dev 헤더 또는 NEWLIB_INCLUDE 필요')
    subprocess.check_call(['make', '-j2', 'CC=' + 시언어번역기, 'LD=' + 연결편집기, 'NEWLIB_INCLUDE=' + 뉴리브포함경로], cwd=str(корінь_шлях / '파이썬연결'))

"""고정한 공식 MicroPython 소스로 свой SVC용 EL0 실행기를 빌드한다."""
import hashlib
import os
from pathlib import Path
import subprocess
import tarfile

выпуск_ЗНАЧЕН_237a4c94 = '1.24.1'
проверка_хэш = 'a291173de1d680786a66dd2381805b6d134defaecea670a560dc7e7d8de540ad'


def Create_PYTHON(корень_путь, C_компилятор, компоновщик_средство):
    Название = 'micropython-' + выпуск_ЗНАЧЕН_237a4c94
    Архив = корень_путь / 'vendor' / (Название + '.tar.gz')
    if not Архив.is_file() or hashlib.sha256(Архив.read_bytes()).hexdigest() != проверка_хэш:
        raise SystemExit('MicroPython источник_дерево 없음/хэш_файл 불일치: ' + str(Архив))
    원본자료 = корень_путь / 'build' / Название
    if not (원본자료 / '.jkoros-source-sha256').is_file():
        with tarfile.open(str(Архив)) as TAR_пакет:
            for член in TAR_пакет.getmembers():
                путь = Path(член.name)
                if путь.is_absolute() or '..' in путь.parts or путь.parts[0] != Название:
                    raise SystemExit('안전하지 않은 источник_дерево путь')
                if член.isfile() or член.isdir():
                    TAR_пакет.extract(член, str(корень_путь / 'build'))
        (원본자료 / '.jkoros-source-sha256').write_text(проверка_хэш + '\n')
    뉴리브포함경로 = os.environ.get('NEWLIB_INCLUDE', '/usr/include/newlib')
    if not (Path(뉴리브포함경로) / 'stdio.h').is_file():
        raise SystemExit('libnewlib-dev 헤더 또는 NEWLIB_INCLUDE 필요')
    subprocess.check_call(['make', '-j2', 'CC=' + C_компилятор, 'LD=' + компоновщик_средство, 'NEWLIB_INCLUDE=' + 뉴리브포함경로], cwd=str(корень_путь / 'PYTHON_мост'))

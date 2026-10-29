"""고정한 공식 MicroPython 소스로 자체 SVC용 EL0 실행기를 빌드한다."""
import hashlib
import os
from pathlib import Path
import subprocess
import tarfile

배포판 = '1.24.1'
validación_hash = 'a291173de1d680786a66dd2381805b6d134defaecea670a560dc7e7d8de540ad'


def crear_PYTHON(raíz_camiño, 시언어번역기, 연결편집기):
    Nome = 'micropython-' + 배포판
    Arquivo = raíz_camiño / 'vendor' / (Nome + '.tar.gz')
    if not Arquivo.is_file() or hashlib.sha256(Arquivo.read_bytes()).hexdigest() != validación_hash:
        raise SystemExit('MicroPython fonte_árbore 없음/hash_Ficheiro 불일치: ' + str(Arquivo))
    원본자료 = raíz_camiño / 'build' / Nome
    if not (원본자료 / '.jkoros-source-sha256').is_file():
        with tarfile.open(str(Arquivo)) as 타르꾸러미:
            for membro in 타르꾸러미.getmembers():
                CAMIÑO = Path(membro.name)
                if CAMIÑO.is_absolute() or '..' in CAMIÑO.parts or CAMIÑO.parts[0] != Nome:
                    raise SystemExit('안전하지 않은 fonte_árbore CAMIÑO')
                if membro.isfile() or membro.isdir():
                    타르꾸러미.extract(membro, str(raíz_camiño / 'build'))
        (원본자료 / '.jkoros-source-sha256').write_text(validación_hash + '\n')
    뉴리브포함경로 = os.environ.get('NEWLIB_INCLUDE', '/usr/include/newlib')
    if not (Path(뉴리브포함경로) / 'stdio.h').is_file():
        raise SystemExit('libnewlib-dev 헤더 또는 NEWLIB_INCLUDE 필요')
    subprocess.check_call(['make', '-j2', 'CC=' + 시언어번역기, 'LD=' + 연결편집기, 'NEWLIB_INCLUDE=' + 뉴리브포함경로], cwd=str(raíz_camiño / 'PYTHON_ponte'))

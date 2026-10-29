"""고정한 공식 MicroPython 소스로 nativo SVC용 EL0 실행기를 빌드한다."""
import hashlib
import os
from pathlib import Path
import subprocess
import tarfile

edizione_VALORE = '1.24.1'
convalida_hash = 'a291173de1d680786a66dd2381805b6d134defaecea670a560dc7e7d8de540ad'


def Crea_PYTHON(radice_percorso, C_compilatore, linker_strumento):
    Nome = 'micropython-' + edizione_VALORE
    Archivio = radice_percorso / 'vendor' / (Nome + '.tar.gz')
    if not Archivio.is_file() or hashlib.sha256(Archivio.read_bytes()).hexdigest() != convalida_hash:
        raise SystemExit('MicroPython fonte_albero 없음/hash_File 불일치: ' + str(Archivio))
    원본자료 = radice_percorso / 'build' / Nome
    if not (원본자료 / '.jkoros-source-sha256').is_file():
        with tarfile.open(str(Archivio)) as tar_aggregare:
            for membro in tar_aggregare.getmembers():
                percorso = Path(membro.name)
                if percorso.is_absolute() or '..' in percorso.parts or percorso.parts[0] != Nome:
                    raise SystemExit('안전하지 않은 fonte_albero percorso')
                if membro.isfile() or membro.isdir():
                    tar_aggregare.extract(membro, str(radice_percorso / 'build'))
        (원본자료 / '.jkoros-source-sha256').write_text(convalida_hash + '\n')
    뉴리브포함경로 = os.environ.get('NEWLIB_INCLUDE', '/usr/include/newlib')
    if not (Path(뉴리브포함경로) / 'stdio.h').is_file():
        raise SystemExit('libnewlib-dev 헤더 또는 NEWLIB_INCLUDE 필요')
    subprocess.check_call(['make', '-j2', 'CC=' + C_compilatore, 'LD=' + linker_strumento, 'NEWLIB_INCLUDE=' + 뉴리브포함경로], cwd=str(radice_percorso / 'PYTHON_bridge'))

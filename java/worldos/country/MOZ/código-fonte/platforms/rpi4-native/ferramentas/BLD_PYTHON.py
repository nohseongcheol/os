"""고정한 공식 MicroPython 소스로 nativo SVC용 EL0 실행기를 빌드한다."""
import hashlib
import os
from pathlib import Path
import subprocess
import tarfile

edição_VALOR = '1.24.1'
validação_hash = 'a291173de1d680786a66dd2381805b6d134defaecea670a560dc7e7d8de540ad'


def Criar_PYTHON(raiz_caminho, C_compilador, vinculador_ferramenta):
    Nome = 'micropython-' + edição_VALOR
    arquivo = raiz_caminho / 'vendor' / (Nome + '.tar.gz')
    if not arquivo.is_file() or hashlib.sha256(arquivo.read_bytes()).hexdigest() != validação_hash:
        raise SystemExit('MicroPython fonte_árvore 없음/hash_Arquivo 불일치: ' + str(arquivo))
    원본자료 = raiz_caminho / 'build' / Nome
    if not (원본자료 / '.jkoros-source-sha256').is_file():
        with tarfile.open(str(arquivo)) as 타르꾸러미:
            for membro in 타르꾸러미.getmembers():
                caminho = Path(membro.name)
                if caminho.is_absolute() or '..' in caminho.parts or caminho.parts[0] != Nome:
                    raise SystemExit('안전하지 않은 fonte_árvore caminho')
                if membro.isfile() or membro.isdir():
                    타르꾸러미.extract(membro, str(raiz_caminho / 'build'))
        (원본자료 / '.jkoros-source-sha256').write_text(validação_hash + '\n')
    뉴리브포함경로 = os.environ.get('NEWLIB_INCLUDE', '/usr/include/newlib')
    if not (Path(뉴리브포함경로) / 'stdio.h').is_file():
        raise SystemExit('libnewlib-dev 헤더 또는 NEWLIB_INCLUDE 필요')
    subprocess.check_call(['make', '-j2', 'CC=' + C_compilador, 'LD=' + vinculador_ferramenta, 'NEWLIB_INCLUDE=' + 뉴리브포함경로], cwd=str(raiz_caminho / 'PYTHON_ponte'))

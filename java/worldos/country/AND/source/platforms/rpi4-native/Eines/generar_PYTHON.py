"""고정한 공식 MicroPython 소스로 propi SVC용 EL0 실행기를 빌드한다."""
import hashlib
import os
from pathlib import Path
import subprocess
import tarfile

배포판 = '1.24.1'
validació_hash = 'a291173de1d680786a66dd2381805b6d134defaecea670a560dc7e7d8de540ad'


def Crear_PYTHON(rel_camí, 시언어번역기, 연결편집기):
    Nom = 'micropython-' + 배포판
    Arxiu = rel_camí / 'vendor' / (Nom + '.tar.gz')
    if not Arxiu.is_file() or hashlib.sha256(Arxiu.read_bytes()).hexdigest() != validació_hash:
        raise SystemExit('MicroPython font_arbre 없음/hash_arxiu 불일치: ' + str(Arxiu))
    원본자료 = rel_camí / 'build' / Nom
    if not (원본자료 / '.jkoros-source-sha256').is_file():
        with tarfile.open(str(Arxiu)) as 타르꾸러미:
            for membre in 타르꾸러미.getmembers():
                Camí = Path(membre.name)
                if Camí.is_absolute() or '..' in Camí.parts or Camí.parts[0] != Nom:
                    raise SystemExit('안전하지 않은 font_arbre Camí')
                if membre.isfile() or membre.isdir():
                    타르꾸러미.extract(membre, str(rel_camí / 'build'))
        (원본자료 / '.jkoros-source-sha256').write_text(validació_hash + '\n')
    뉴리브포함경로 = os.environ.get('NEWLIB_INCLUDE', '/usr/include/newlib')
    if not (Path(뉴리브포함경로) / 'stdio.h').is_file():
        raise SystemExit('libnewlib-dev 헤더 또는 NEWLIB_INCLUDE 필요')
    subprocess.check_call(['make', '-j2', 'CC=' + 시언어번역기, 'LD=' + 연결편집기, 'NEWLIB_INCLUDE=' + 뉴리브포함경로], cwd=str(rel_camí / 'PYTHON_pont'))

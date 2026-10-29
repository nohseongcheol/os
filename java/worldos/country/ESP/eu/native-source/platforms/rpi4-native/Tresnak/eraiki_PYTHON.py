"""고정한 공식 MicroPython 소스로 자체 SVC용 EL0 실행기를 빌드한다."""
import hashlib
import os
from pathlib import Path
import subprocess
import tarfile

배포판 = '1.24.1'
balidazio_hash = 'a291173de1d680786a66dd2381805b6d134defaecea670a560dc7e7d8de540ad'


def sortu_PYTHON(erro_bide_izen, 시언어번역기, 연결편집기):
    Izena = 'micropython-' + 배포판
    artxibo = erro_bide_izen / 'vendor' / (Izena + '.tar.gz')
    if not artxibo.is_file() or hashlib.sha256(artxibo.read_bytes()).hexdigest() != balidazio_hash:
        raise SystemExit('MicroPython iturburu_zuhaitz 없음/hash_fitxategi 불일치: ' + str(artxibo))
    원본자료 = erro_bide_izen / 'build' / Izena
    if not (원본자료 / '.jkoros-source-sha256').is_file():
        with tarfile.open(str(artxibo)) as 타르꾸러미:
            for kide in 타르꾸러미.getmembers():
                Bide_izena = Path(kide.name)
                if Bide_izena.is_absolute() or '..' in Bide_izena.parts or Bide_izena.parts[0] != Izena:
                    raise SystemExit('안전하지 않은 iturburu_zuhaitz Bide_izena')
                if kide.isfile() or kide.isdir():
                    타르꾸러미.extract(kide, str(erro_bide_izen / 'build'))
        (원본자료 / '.jkoros-source-sha256').write_text(balidazio_hash + '\n')
    뉴리브포함경로 = os.environ.get('NEWLIB_INCLUDE', '/usr/include/newlib')
    if not (Path(뉴리브포함경로) / 'stdio.h').is_file():
        raise SystemExit('libnewlib-dev 헤더 또는 NEWLIB_INCLUDE 필요')
    subprocess.check_call(['make', '-j2', 'CC=' + 시언어번역기, 'LD=' + 연결편집기, 'NEWLIB_INCLUDE=' + 뉴리브포함경로], cwd=str(erro_bide_izen / 'PYTHON_zubi'))

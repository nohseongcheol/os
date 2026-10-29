"""고정한 공식 MicroPython 소스로 자체 SVC용 EL0 실행기를 빌드한다."""
import hashlib
import os
from pathlib import Path
import subprocess
import tarfile

배포판 = '1.24.1'
pagpapatibay_hash = 'a291173de1d680786a66dd2381805b6d134defaecea670a560dc7e7d8de540ad'


def Create_PYTHON(root_path, 시언어번역기, 연결편집기):
    pangalan = 'micropython-' + 배포판
    Archive = root_path / 'vendor' / (pangalan + '.tar.gz')
    if not Archive.is_file() or hashlib.sha256(Archive.read_bytes()).hexdigest() != pagpapatibay_hash:
        raise SystemExit('MicroPython pinagmulan_balangkas 없음/hash_file 불일치: ' + str(Archive))
    원본자료 = root_path / 'build' / pangalan
    if not (원본자료 / '.jkoros-source-sha256').is_file():
        with tarfile.open(str(Archive)) as 타르꾸러미:
            for miyembro in 타르꾸러미.getmembers():
                path = Path(miyembro.name)
                if path.is_absolute() or '..' in path.parts or path.parts[0] != pangalan:
                    raise SystemExit('안전하지 않은 pinagmulan_balangkas path')
                if miyembro.isfile() or miyembro.isdir():
                    타르꾸러미.extract(miyembro, str(root_path / 'build'))
        (원본자료 / '.jkoros-source-sha256').write_text(pagpapatibay_hash + '\n')
    뉴리브포함경로 = os.environ.get('NEWLIB_INCLUDE', '/usr/include/newlib')
    if not (Path(뉴리브포함경로) / 'stdio.h').is_file():
        raise SystemExit('libnewlib-dev 헤더 또는 NEWLIB_INCLUDE 필요')
    subprocess.check_call(['make', '-j2', 'CC=' + 시언어번역기, 'LD=' + 연결편집기, 'NEWLIB_INCLUDE=' + 뉴리브포함경로], cwd=str(root_path / 'PYTHON_bridge'))

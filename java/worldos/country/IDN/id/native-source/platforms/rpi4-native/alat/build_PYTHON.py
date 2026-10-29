"""고정한 공식 MicroPython 소스로 Asli SVC용 EL0 실행기를 빌드한다."""
import hashlib
import os
from pathlib import Path
import subprocess
import tarfile

배포판 = '1.24.1'
validasi_hash = 'a291173de1d680786a66dd2381805b6d134defaecea670a560dc7e7d8de540ad'


def Buat_PYTHON(akar_jalur, 시언어번역기, 연결편집기):
    Nama_2 = 'micropython-' + 배포판
    Arsip = akar_jalur / 'vendor' / (Nama_2 + '.tar.gz')
    if not Arsip.is_file() or hashlib.sha256(Arsip.read_bytes()).hexdigest() != validasi_hash:
        raise SystemExit('MicroPython sumber_pohon 없음/hash_file 불일치: ' + str(Arsip))
    원본자료 = akar_jalur / 'build' / Nama_2
    if not (원본자료 / '.jkoros-source-sha256').is_file():
        with tarfile.open(str(Arsip)) as 타르꾸러미:
            for anggota in 타르꾸러미.getmembers():
                jalur = Path(anggota.name)
                if jalur.is_absolute() or '..' in jalur.parts or jalur.parts[0] != Nama_2:
                    raise SystemExit('안전하지 않은 sumber_pohon jalur')
                if anggota.isfile() or anggota.isdir():
                    타르꾸러미.extract(anggota, str(akar_jalur / 'build'))
        (원본자료 / '.jkoros-source-sha256').write_text(validasi_hash + '\n')
    뉴리브포함경로 = os.environ.get('NEWLIB_INCLUDE', '/usr/include/newlib')
    if not (Path(뉴리브포함경로) / 'stdio.h').is_file():
        raise SystemExit('libnewlib-dev 헤더 또는 NEWLIB_INCLUDE 필요')
    subprocess.check_call(['make', '-j2', 'CC=' + 시언어번역기, 'LD=' + 연결편집기, 'NEWLIB_INCLUDE=' + 뉴리브포함경로], cwd=str(akar_jalur / 'PYTHON_bridge'))

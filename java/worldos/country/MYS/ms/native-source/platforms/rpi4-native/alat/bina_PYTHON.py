"""고정한 공식 MicroPython 소스로 Asli SVC용 EL0 실행기를 빌드한다."""
import hashlib
import os
from pathlib import Path
import subprocess
import tarfile

배포판 = '1.24.1'
pensahihan_cincangan = 'a291173de1d680786a66dd2381805b6d134defaecea670a560dc7e7d8de540ad'


def cipta_PYTHON(akar_laluan, 시언어번역기, pemaut_alat):
    Nama = 'micropython-' + 배포판
    Arkib = akar_laluan / 'vendor' / (Nama + '.tar.gz')
    if not Arkib.is_file() or hashlib.sha256(Arkib.read_bytes()).hexdigest() != pensahihan_cincangan:
        raise SystemExit('MicroPython sumber_pepohon 없음/cincangan_fail 불일치: ' + str(Arkib))
    원본자료 = akar_laluan / 'build' / Nama
    if not (원본자료 / '.jkoros-source-sha256').is_file():
        with tarfile.open(str(Arkib)) as 타르꾸러미:
            for ahli in 타르꾸러미.getmembers():
                LALUAN = Path(ahli.name)
                if LALUAN.is_absolute() or '..' in LALUAN.parts or LALUAN.parts[0] != Nama:
                    raise SystemExit('안전하지 않은 sumber_pepohon LALUAN')
                if ahli.isfile() or ahli.isdir():
                    타르꾸러미.extract(ahli, str(akar_laluan / 'build'))
        (원본자료 / '.jkoros-source-sha256').write_text(pensahihan_cincangan + '\n')
    뉴리브포함경로 = os.environ.get('NEWLIB_INCLUDE', '/usr/include/newlib')
    if not (Path(뉴리브포함경로) / 'stdio.h').is_file():
        raise SystemExit('libnewlib-dev 헤더 또는 NEWLIB_INCLUDE 필요')
    subprocess.check_call(['make', '-j2', 'CC=' + 시언어번역기, 'LD=' + pemaut_alat, 'NEWLIB_INCLUDE=' + 뉴리브포함경로], cwd=str(akar_laluan / 'PYTHON_penghubung'))

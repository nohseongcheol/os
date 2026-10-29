"""고정한 공식 MicroPython 소스로 eget SVC용 EL0 실행기를 빌드한다."""
import hashlib
import os
from pathlib import Path
import subprocess
import tarfile

utgave_Edition_VERDI = '1.24.1'
validering_hash = 'a291173de1d680786a66dd2381805b6d134defaecea670a560dc7e7d8de540ad'


def åpne_PYTHON(rot_bane, C_kompilator, koblingsprogram_verktøy):
    Navn = 'micropython-' + utgave_Edition_VERDI
    Arkiv = rot_bane / 'vendor' / (Navn + '.tar.gz')
    if not Arkiv.is_file() or hashlib.sha256(Arkiv.read_bytes()).hexdigest() != validering_hash:
        raise SystemExit('MicroPython kilde_tre 없음/hash_Fil 불일치: ' + str(Arkiv))
    원본자료 = rot_bane / 'build' / Navn
    if not (원본자료 / '.jkoros-source-sha256').is_file():
        with tarfile.open(str(Arkiv)) as 타르꾸러미:
            for medlem in 타르꾸러미.getmembers():
                Sti = Path(medlem.name)
                if Sti.is_absolute() or '..' in Sti.parts or Sti.parts[0] != Navn:
                    raise SystemExit('안전하지 않은 kilde_tre Sti')
                if medlem.isfile() or medlem.isdir():
                    타르꾸러미.extract(medlem, str(rot_bane / 'build'))
        (원본자료 / '.jkoros-source-sha256').write_text(validering_hash + '\n')
    뉴리브포함경로 = os.environ.get('NEWLIB_INCLUDE', '/usr/include/newlib')
    if not (Path(뉴리브포함경로) / 'stdio.h').is_file():
        raise SystemExit('libnewlib-dev 헤더 또는 NEWLIB_INCLUDE 필요')
    subprocess.check_call(['make', '-j2', 'CC=' + C_kompilator, 'LD=' + koblingsprogram_verktøy, 'NEWLIB_INCLUDE=' + 뉴리브포함경로], cwd=str(rot_bane / 'PYTHON_bro'))

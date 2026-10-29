"""고정한 공식 MicroPython 소스로 eget SVC용 EL0 실행기를 빌드한다."""
import hashlib
import os
from pathlib import Path
import subprocess
import tarfile

utgåva_värde = '1.24.1'
validering_hash = 'a291173de1d680786a66dd2381805b6d134defaecea670a560dc7e7d8de540ad'


def Skapa_PYTHON(rot_väg, C_kompilerare, länkare_verktyg):
    Namn = 'micropython-' + utgåva_värde
    Arkiv = rot_väg / 'vendor' / (Namn + '.tar.gz')
    if not Arkiv.is_file() or hashlib.sha256(Arkiv.read_bytes()).hexdigest() != validering_hash:
        raise SystemExit('MicroPython källa_träd 없음/hash_fil 불일치: ' + str(Arkiv))
    원본자료 = rot_väg / 'build' / Namn
    if not (원본자료 / '.jkoros-source-sha256').is_file():
        with tarfile.open(str(Arkiv)) as 타르꾸러미:
            for medlem in 타르꾸러미.getmembers():
                sökväg_2 = Path(medlem.name)
                if sökväg_2.is_absolute() or '..' in sökväg_2.parts or sökväg_2.parts[0] != Namn:
                    raise SystemExit('안전하지 않은 källa_träd sökväg_2')
                if medlem.isfile() or medlem.isdir():
                    타르꾸러미.extract(medlem, str(rot_väg / 'build'))
        (원본자료 / '.jkoros-source-sha256').write_text(validering_hash + '\n')
    뉴리브포함경로 = os.environ.get('NEWLIB_INCLUDE', '/usr/include/newlib')
    if not (Path(뉴리브포함경로) / 'stdio.h').is_file():
        raise SystemExit('libnewlib-dev 헤더 또는 NEWLIB_INCLUDE 필요')
    subprocess.check_call(['make', '-j2', 'CC=' + C_kompilerare, 'LD=' + länkare_verktyg, 'NEWLIB_INCLUDE=' + 뉴리브포함경로], cwd=str(rot_väg / 'PYTHON_brygga'))

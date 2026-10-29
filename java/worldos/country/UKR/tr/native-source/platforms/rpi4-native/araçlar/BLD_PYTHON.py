"""고정한 공식 MicroPython 소스로 Öz SVC용 EL0 실행기를 빌드한다."""
import hashlib
import os
from pathlib import Path
import subprocess
import tarfile

sürüm_değer_237a4c94 = '1.24.1'
doğrulama_özet = 'a291173de1d680786a66dd2381805b6d134defaecea670a560dc7e7d8de540ad'


def açmak_PYTHON(kök_yol, C_derleyici, bağlayıcı_araç):
    İsim = 'micropython-' + sürüm_değer_237a4c94
    Arşiv = kök_yol / 'vendor' / (İsim + '.tar.gz')
    if not Arşiv.is_file() or hashlib.sha256(Arşiv.read_bytes()).hexdigest() != doğrulama_özet:
        raise SystemExit('MicroPython kaynak_ağaç 없음/özet_Dosya 불일치: ' + str(Arşiv))
    원본자료 = kök_yol / 'build' / İsim
    if not (원본자료 / '.jkoros-source-sha256').is_file():
        with tarfile.open(str(Arşiv)) as 타르꾸러미:
            for üye in 타르꾸러미.getmembers():
                yol = Path(üye.name)
                if yol.is_absolute() or '..' in yol.parts or yol.parts[0] != İsim:
                    raise SystemExit('안전하지 않은 kaynak_ağaç yol')
                if üye.isfile() or üye.isdir():
                    타르꾸러미.extract(üye, str(kök_yol / 'build'))
        (원본자료 / '.jkoros-source-sha256').write_text(doğrulama_özet + '\n')
    뉴리브포함경로 = os.environ.get('NEWLIB_INCLUDE', '/usr/include/newlib')
    if not (Path(뉴리브포함경로) / 'stdio.h').is_file():
        raise SystemExit('libnewlib-dev 헤더 또는 NEWLIB_INCLUDE 필요')
    subprocess.check_call(['make', '-j2', 'CC=' + C_derleyici, 'LD=' + bağlayıcı_araç, 'NEWLIB_INCLUDE=' + 뉴리브포함경로], cwd=str(kök_yol / 'PYTHON_köprü'))

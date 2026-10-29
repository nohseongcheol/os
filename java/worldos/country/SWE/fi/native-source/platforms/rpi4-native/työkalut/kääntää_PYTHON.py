"""고정한 공식 MicroPython 소스로 oma SVC용 EL0 실행기를 빌드한다."""
import hashlib
import os
from pathlib import Path
import subprocess
import tarfile

versio_ARVO_237a4c94 = '1.24.1'
vahvistus_hajautusarvo = 'a291173de1d680786a66dd2381805b6d134defaecea670a560dc7e7d8de540ad'


def Luo_PYTHON(juuri_polku, C_kääntäjä, linkitin_työkalu):
    Nimi = 'micropython-' + versio_ARVO_237a4c94
    Arkisto = juuri_polku / 'vendor' / (Nimi + '.tar.gz')
    if not Arkisto.is_file() or hashlib.sha256(Arkisto.read_bytes()).hexdigest() != vahvistus_hajautusarvo:
        raise SystemExit('MicroPython lähde_puu 없음/hajautusarvo_Tiedosto 불일치: ' + str(Arkisto))
    원본자료 = juuri_polku / 'build' / Nimi
    if not (원본자료 / '.jkoros-source-sha256').is_file():
        with tarfile.open(str(Arkisto)) as 타르꾸러미:
            for jäsen in 타르꾸러미.getmembers():
                polku_2 = Path(jäsen.name)
                if polku_2.is_absolute() or '..' in polku_2.parts or polku_2.parts[0] != Nimi:
                    raise SystemExit('안전하지 않은 lähde_puu polku_2')
                if jäsen.isfile() or jäsen.isdir():
                    타르꾸러미.extract(jäsen, str(juuri_polku / 'build'))
        (원본자료 / '.jkoros-source-sha256').write_text(vahvistus_hajautusarvo + '\n')
    뉴리브포함경로 = os.environ.get('NEWLIB_INCLUDE', '/usr/include/newlib')
    if not (Path(뉴리브포함경로) / 'stdio.h').is_file():
        raise SystemExit('libnewlib-dev 헤더 또는 NEWLIB_INCLUDE 필요')
    subprocess.check_call(['make', '-j2', 'CC=' + C_kääntäjä, 'LD=' + linkitin_työkalu, 'NEWLIB_INCLUDE=' + 뉴리브포함경로], cwd=str(juuri_polku / 'PYTHON_silta'))

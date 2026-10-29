"""고정한 공식 MicroPython 소스로 자체 SVC용 EL0 실행기를 빌드한다."""
import hashlib
import os
from pathlib import Path
import subprocess
import tarfile

배포판 = '1.24.1'
Validatioun_Hash = 'a291173de1d680786a66dd2381805b6d134defaecea670a560dc7e7d8de540ad'


def Create_PYTHON(Racinn_Wee, 시언어번역기, 연결편집기):
    Numm = 'micropython-' + 배포판
    Archiv = Racinn_Wee / 'vendor' / (Numm + '.tar.gz')
    if not Archiv.is_file() or hashlib.sha256(Archiv.read_bytes()).hexdigest() != Validatioun_Hash:
        raise SystemExit('MicroPython Quell_Bamstruktur 없음/Hash_Fichier 불일치: ' + str(Archiv))
    원본자료 = Racinn_Wee / 'build' / Numm
    if not (원본자료 / '.jkoros-source-sha256').is_file():
        with tarfile.open(str(Archiv)) as 타르꾸러미:
            for Member in 타르꾸러미.getmembers():
                Wee = Path(Member.name)
                if Wee.is_absolute() or '..' in Wee.parts or Wee.parts[0] != Numm:
                    raise SystemExit('안전하지 않은 Quell_Bamstruktur Wee')
                if Member.isfile() or Member.isdir():
                    타르꾸러미.extract(Member, str(Racinn_Wee / 'build'))
        (원본자료 / '.jkoros-source-sha256').write_text(Validatioun_Hash + '\n')
    뉴리브포함경로 = os.environ.get('NEWLIB_INCLUDE', '/usr/include/newlib')
    if not (Path(뉴리브포함경로) / 'stdio.h').is_file():
        raise SystemExit('libnewlib-dev 헤더 또는 NEWLIB_INCLUDE 필요')
    subprocess.check_call(['make', '-j2', 'CC=' + 시언어번역기, 'LD=' + 연결편집기, 'NEWLIB_INCLUDE=' + 뉴리브포함경로], cwd=str(Racinn_Wee / 'PYTHON_Bréck'))

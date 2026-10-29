"""고정한 공식 MicroPython 소스로 자체 SVC용 EL0 실행기를 빌드한다."""
import hashlib
import os
from pathlib import Path
import subprocess
import tarfile

배포판 = '1.24.1'
amincewa_hash = 'a291173de1d680786a66dd2381805b6d134defaecea670a560dc7e7d8de540ad'


def 파이썬만들기(기준경로, 시언어번역기, 연결편집기):
    Suna = 'micropython-' + 배포판
    Rumbun_ajiya = 기준경로 / 'vendor' / (Suna + '.tar.gz')
    if not Rumbun_ajiya.is_file() or hashlib.sha256(Rumbun_ajiya.read_bytes()).hexdigest() != amincewa_hash:
        raise SystemExit('MicroPython tushe_Li_irabin_tarin_bayanai 없음/hash_Fayil 불일치: ' + str(Rumbun_ajiya))
    원본자료 = 기준경로 / 'build' / Suna
    if not (원본자료 / '.jkoros-source-sha256').is_file():
        with tarfile.open(str(Rumbun_ajiya)) as 타르꾸러미:
            for Memba in 타르꾸러미.getmembers():
                Hanyar_shiga = Path(Memba.name)
                if Hanyar_shiga.is_absolute() or '..' in Hanyar_shiga.parts or Hanyar_shiga.parts[0] != Suna:
                    raise SystemExit('안전하지 않은 tushe_Li_irabin_tarin_bayanai Hanyar_shiga')
                if Memba.isfile() or Memba.isdir():
                    타르꾸러미.extract(Memba, str(기준경로 / 'build'))
        (원본자료 / '.jkoros-source-sha256').write_text(amincewa_hash + '\n')
    뉴리브포함경로 = os.environ.get('NEWLIB_INCLUDE', '/usr/include/newlib')
    if not (Path(뉴리브포함경로) / 'stdio.h').is_file():
        raise SystemExit('libnewlib-dev 헤더 또는 NEWLIB_INCLUDE 필요')
    subprocess.check_call(['make', '-j2', 'CC=' + 시언어번역기, 'LD=' + 연결편집기, 'NEWLIB_INCLUDE=' + 뉴리브포함경로], cwd=str(기준경로 / '파이썬연결'))

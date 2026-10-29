"""고정한 공식 MicroPython 소스로 자체 SVC용 EL0 실행기를 빌드한다."""
import hashlib
import os
from pathlib import Path
import subprocess
import tarfile

배포판 = '1.24.1'
bailíochtú_hais = 'a291173de1d680786a66dd2381805b6d134defaecea670a560dc7e7d8de540ad'


def Create_PYTHON(fréamh_cosán, 시언어번역기, 연결편집기):
    Ainm = 'micropython-' + 배포판
    Cartlann = fréamh_cosán / 'vendor' / (Ainm + '.tar.gz')
    if not Cartlann.is_file() or hashlib.sha256(Cartlann.read_bytes()).hexdigest() != bailíochtú_hais:
        raise SystemExit('MicroPython foinse_crann 없음/hais_comhad 불일치: ' + str(Cartlann))
    원본자료 = fréamh_cosán / 'build' / Ainm
    if not (원본자료 / '.jkoros-source-sha256').is_file():
        with tarfile.open(str(Cartlann)) as 타르꾸러미:
            for ball in 타르꾸러미.getmembers():
                CONAIR = Path(ball.name)
                if CONAIR.is_absolute() or '..' in CONAIR.parts or CONAIR.parts[0] != Ainm:
                    raise SystemExit('안전하지 않은 foinse_crann CONAIR')
                if ball.isfile() or ball.isdir():
                    타르꾸러미.extract(ball, str(fréamh_cosán / 'build'))
        (원본자료 / '.jkoros-source-sha256').write_text(bailíochtú_hais + '\n')
    뉴리브포함경로 = os.environ.get('NEWLIB_INCLUDE', '/usr/include/newlib')
    if not (Path(뉴리브포함경로) / 'stdio.h').is_file():
        raise SystemExit('libnewlib-dev 헤더 또는 NEWLIB_INCLUDE 필요')
    subprocess.check_call(['make', '-j2', 'CC=' + 시언어번역기, 'LD=' + 연결편집기, 'NEWLIB_INCLUDE=' + 뉴리브포함경로], cwd=str(fréamh_cosán / 'PYTHON_traschóiritheoir'))

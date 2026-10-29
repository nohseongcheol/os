"""고정한 공식 MicroPython 소스로 자체 SVC용 EL0 실행기를 빌드한다."""
import hashlib
import os
from pathlib import Path
import subprocess
import tarfile

배포판 = '1.24.1'
dearbhadh_hais = 'a291173de1d680786a66dd2381805b6d134defaecea670a560dc7e7d8de540ad'


def Create_PYTHON(freumh_slighe, 시언어번역기, 연결편집기):
    Ainm = 'micropython-' + 배포판
    taisg = freumh_slighe / 'vendor' / (Ainm + '.tar.gz')
    if not taisg.is_file() or hashlib.sha256(taisg.read_bytes()).hexdigest() != dearbhadh_hais:
        raise SystemExit('MicroPython tùs_craobh 없음/hais_faidhle 불일치: ' + str(taisg))
    원본자료 = freumh_slighe / 'build' / Ainm
    if not (원본자료 / '.jkoros-source-sha256').is_file():
        with tarfile.open(str(taisg)) as 타르꾸러미:
            for ball in 타르꾸러미.getmembers():
                Slighe = Path(ball.name)
                if Slighe.is_absolute() or '..' in Slighe.parts or Slighe.parts[0] != Ainm:
                    raise SystemExit('안전하지 않은 tùs_craobh Slighe')
                if ball.isfile() or ball.isdir():
                    타르꾸러미.extract(ball, str(freumh_slighe / 'build'))
        (원본자료 / '.jkoros-source-sha256').write_text(dearbhadh_hais + '\n')
    뉴리브포함경로 = os.environ.get('NEWLIB_INCLUDE', '/usr/include/newlib')
    if not (Path(뉴리브포함경로) / 'stdio.h').is_file():
        raise SystemExit('libnewlib-dev 헤더 또는 NEWLIB_INCLUDE 필요')
    subprocess.check_call(['make', '-j2', 'CC=' + 시언어번역기, 'LD=' + 연결편집기, 'NEWLIB_INCLUDE=' + 뉴리브포함경로], cwd=str(freumh_slighe / 'PYTHON_drochaid'))

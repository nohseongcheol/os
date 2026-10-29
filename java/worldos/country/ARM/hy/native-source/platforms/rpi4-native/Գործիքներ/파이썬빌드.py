"""고정한 공식 MicroPython 소스로 자체 SVC용 EL0 실행기를 빌드한다."""
import hashlib
import os
from pathlib import Path
import subprocess
import tarfile

배포판 = '1.24.1'
վավերացում_պատահական_տվյալներ = 'a291173de1d680786a66dd2381805b6d134defaecea670a560dc7e7d8de540ad'


def 파이썬만들기(արմատ_ուղի, 시언어번역기, 연결편집기):
    Անուն = 'micropython-' + 배포판
    Պահոց = արմատ_ուղի / 'vendor' / (Անուն + '.tar.gz')
    if not Պահոց.is_file() or hashlib.sha256(Պահոց.read_bytes()).hexdigest() != վավերացում_պատահական_տվյալներ:
        raise SystemExit('MicroPython աղբյուր_ծառ 없음/պատահական_տվյալներ_նիշք 불일치: ' + str(Պահոց))
    원본자료 = արմատ_ուղի / 'build' / Անուն
    if not (원본자료 / '.jkoros-source-sha256').is_file():
        with tarfile.open(str(Պահոց)) as 타르꾸러미:
            for անդամ in 타르꾸러미.getmembers():
                Ճանապարհ = Path(անդամ.name)
                if Ճանապարհ.is_absolute() or '..' in Ճանապարհ.parts or Ճանապարհ.parts[0] != Անուն:
                    raise SystemExit('안전하지 않은 աղբյուր_ծառ Ճանապարհ')
                if անդամ.isfile() or անդամ.isdir():
                    타르꾸러미.extract(անդամ, str(արմատ_ուղի / 'build'))
        (원본자료 / '.jkoros-source-sha256').write_text(վավերացում_պատահական_տվյալներ + '\n')
    뉴리브포함경로 = os.environ.get('NEWLIB_INCLUDE', '/usr/include/newlib')
    if not (Path(뉴리브포함경로) / 'stdio.h').is_file():
        raise SystemExit('libnewlib-dev 헤더 또는 NEWLIB_INCLUDE 필요')
    subprocess.check_call(['make', '-j2', 'CC=' + 시언어번역기, 'LD=' + 연결편집기, 'NEWLIB_INCLUDE=' + 뉴리브포함경로], cwd=str(արմատ_ուղի / '파이썬연결'))

"""고정한 공식 MicroPython 소스로 자체 SVC용 EL0 실행기를 빌드한다."""
import hashlib
import os
from pathlib import Path
import subprocess
import tarfile

배포판 = '1.24.1'
ማረጋገጥ_ሃሽ = 'a291173de1d680786a66dd2381805b6d134defaecea670a560dc7e7d8de540ad'


def 파이썬만들기(ስር_ዱካ, 시언어번역기, 연결편집기):
    ስም = 'micropython-' + 배포판
    ከዝን = ስር_ዱካ / 'vendor' / (ስም + '.tar.gz')
    if not ከዝን.is_file() or hashlib.sha256(ከዝን.read_bytes()).hexdigest() != ማረጋገጥ_ሃሽ:
        raise SystemExit('MicroPython ምንጭ_ዛፍ 없음/ሃሽ_ፋይል 불일치: ' + str(ከዝን))
    원본자료 = ስር_ዱካ / 'build' / ስም
    if not (원본자료 / '.jkoros-source-sha256').is_file():
        with tarfile.open(str(ከዝን)) as 타르꾸러미:
            for አባል in 타르꾸러미.getmembers():
                መተላለፊያ = Path(አባል.name)
                if መተላለፊያ.is_absolute() or '..' in መተላለፊያ.parts or መተላለፊያ.parts[0] != ስም:
                    raise SystemExit('안전하지 않은 ምንጭ_ዛፍ መተላለፊያ')
                if አባል.isfile() or አባል.isdir():
                    타르꾸러미.extract(አባል, str(ስር_ዱካ / 'build'))
        (원본자료 / '.jkoros-source-sha256').write_text(ማረጋገጥ_ሃሽ + '\n')
    뉴리브포함경로 = os.environ.get('NEWLIB_INCLUDE', '/usr/include/newlib')
    if not (Path(뉴리브포함경로) / 'stdio.h').is_file():
        raise SystemExit('libnewlib-dev 헤더 또는 NEWLIB_INCLUDE 필요')
    subprocess.check_call(['make', '-j2', 'CC=' + 시언어번역기, 'LD=' + 연결편집기, 'NEWLIB_INCLUDE=' + 뉴리브포함경로], cwd=str(ስር_ዱካ / '파이썬연결'))

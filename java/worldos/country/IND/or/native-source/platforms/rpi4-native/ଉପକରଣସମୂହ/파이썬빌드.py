"""고정한 공식 MicroPython 소스로 자체 SVC용 EL0 실행기를 빌드한다."""
import hashlib
import os
from pathlib import Path
import subprocess
import tarfile

배포판 = '1.24.1'
ବୈଧକରଣ_ହାସ୍ = 'a291173de1d680786a66dd2381805b6d134defaecea670a560dc7e7d8de540ad'


def 파이썬만들기(ରୁଟ୍_ପଥ, 시언어번역기, 연결편집기):
    ନାମ = 'micropython-' + 배포판
    ଅଭିଲେଖାଗାର = ରୁଟ୍_ପଥ / 'vendor' / (ନାମ + '.tar.gz')
    if not ଅଭିଲେଖାଗାର.is_file() or hashlib.sha256(ଅଭିଲେଖାଗାର.read_bytes()).hexdigest() != ବୈଧକରଣ_ହାସ୍:
        raise SystemExit('MicroPython ଉତ୍ସ_ବୃକ୍ଷ 없음/ହାସ୍_ଫାଇଲ୍ 불일치: ' + str(ଅଭିଲେଖାଗାର))
    원본자료 = ରୁଟ୍_ପଥ / 'build' / ନାମ
    if not (원본자료 / '.jkoros-source-sha256').is_file():
        with tarfile.open(str(ଅଭିଲେଖାଗାର)) as 타르꾸러미:
            for ସଭ୍ୟ in 타르꾸러미.getmembers():
                ପଥ = Path(ସଭ୍ୟ.name)
                if ପଥ.is_absolute() or '..' in ପଥ.parts or ପଥ.parts[0] != ନାମ:
                    raise SystemExit('안전하지 않은 ଉତ୍ସ_ବୃକ୍ଷ ପଥ')
                if ସଭ୍ୟ.isfile() or ସଭ୍ୟ.isdir():
                    타르꾸러미.extract(ସଭ୍ୟ, str(ରୁଟ୍_ପଥ / 'build'))
        (원본자료 / '.jkoros-source-sha256').write_text(ବୈଧକରଣ_ହାସ୍ + '\n')
    뉴리브포함경로 = os.environ.get('NEWLIB_INCLUDE', '/usr/include/newlib')
    if not (Path(뉴리브포함경로) / 'stdio.h').is_file():
        raise SystemExit('libnewlib-dev 헤더 또는 NEWLIB_INCLUDE 필요')
    subprocess.check_call(['make', '-j2', 'CC=' + 시언어번역기, 'LD=' + 연결편집기, 'NEWLIB_INCLUDE=' + 뉴리브포함경로], cwd=str(ରୁଟ୍_ପଥ / '파이썬연결'))

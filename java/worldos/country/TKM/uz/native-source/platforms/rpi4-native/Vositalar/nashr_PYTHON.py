"""고정한 공식 MicroPython 소스로 자체 SVC용 EL0 실행기를 빌드한다."""
import hashlib
import os
from pathlib import Path
import subprocess
import tarfile

배포판 = '1.24.1'
tasdiq_tasodifiy_ma_lumot = 'a291173de1d680786a66dd2381805b6d134defaecea670a560dc7e7d8de540ad'


def Yaratish_PYTHON(ildiz_yo_l, 시언어번역기, 연결편집기):
    Nomi = 'micropython-' + 배포판
    Arxiv = ildiz_yo_l / 'vendor' / (Nomi + '.tar.gz')
    if not Arxiv.is_file() or hashlib.sha256(Arxiv.read_bytes()).hexdigest() != tasdiq_tasodifiy_ma_lumot:
        raise SystemExit('MicroPython manba_daraxt 없음/tasodifiy_ma_lumot_fayl 불일치: ' + str(Arxiv))
    원본자료 = ildiz_yo_l / 'build' / Nomi
    if not (원본자료 / '.jkoros-source-sha256').is_file():
        with tarfile.open(str(Arxiv)) as 타르꾸러미:
            for a_zo in 타르꾸러미.getmembers():
                yo_l = Path(a_zo.name)
                if yo_l.is_absolute() or '..' in yo_l.parts or yo_l.parts[0] != Nomi:
                    raise SystemExit('안전하지 않은 manba_daraxt yo_l')
                if a_zo.isfile() or a_zo.isdir():
                    타르꾸러미.extract(a_zo, str(ildiz_yo_l / 'build'))
        (원본자료 / '.jkoros-source-sha256').write_text(tasdiq_tasodifiy_ma_lumot + '\n')
    뉴리브포함경로 = os.environ.get('NEWLIB_INCLUDE', '/usr/include/newlib')
    if not (Path(뉴리브포함경로) / 'stdio.h').is_file():
        raise SystemExit('libnewlib-dev 헤더 또는 NEWLIB_INCLUDE 필요')
    subprocess.check_call(['make', '-j2', 'CC=' + 시언어번역기, 'LD=' + 연결편집기, 'NEWLIB_INCLUDE=' + 뉴리브포함경로], cwd=str(ildiz_yo_l / '파이썬연결'))

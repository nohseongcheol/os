"""고정한 공식 MicroPython 소스로 자체 SVC용 EL0 실행기를 빌드한다."""
import hashlib
import os
from pathlib import Path
import subprocess
import tarfile

배포판 = '1.24.1'
yoxlama_heş = 'a291173de1d680786a66dd2381805b6d134defaecea670a560dc7e7d8de540ad'


def yarat_PYTHON(kök_yol, 시언어번역기, 연결편집기):
    Ad = 'micropython-' + 배포판
    Arxiv = kök_yol / 'vendor' / (Ad + '.tar.gz')
    if not Arxiv.is_file() or hashlib.sha256(Arxiv.read_bytes()).hexdigest() != yoxlama_heş:
        raise SystemExit('MicroPython mənbə_ağac 없음/heş_fayl 불일치: ' + str(Arxiv))
    원본자료 = kök_yol / 'build' / Ad
    if not (원본자료 / '.jkoros-source-sha256').is_file():
        with tarfile.open(str(Arxiv)) as 타르꾸러미:
            for üzv in 타르꾸러미.getmembers():
                Cığır = Path(üzv.name)
                if Cığır.is_absolute() or '..' in Cığır.parts or Cığır.parts[0] != Ad:
                    raise SystemExit('안전하지 않은 mənbə_ağac Cığır')
                if üzv.isfile() or üzv.isdir():
                    타르꾸러미.extract(üzv, str(kök_yol / 'build'))
        (원본자료 / '.jkoros-source-sha256').write_text(yoxlama_heş + '\n')
    뉴리브포함경로 = os.environ.get('NEWLIB_INCLUDE', '/usr/include/newlib')
    if not (Path(뉴리브포함경로) / 'stdio.h').is_file():
        raise SystemExit('libnewlib-dev 헤더 또는 NEWLIB_INCLUDE 필요')
    subprocess.check_call(['make', '-j2', 'CC=' + 시언어번역기, 'LD=' + 연결편집기, 'NEWLIB_INCLUDE=' + 뉴리브포함경로], cwd=str(kök_yol / 'PYTHON_körpü'))

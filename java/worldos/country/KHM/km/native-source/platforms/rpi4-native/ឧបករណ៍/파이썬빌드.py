"""고정한 공식 MicroPython 소스로 자체 SVC용 EL0 실행기를 빌드한다."""
import hashlib
import os
from pathlib import Path
import subprocess
import tarfile

배포판 = '1.24.1'
សុពលភាព_ហាស = 'a291173de1d680786a66dd2381805b6d134defaecea670a560dc7e7d8de540ad'


def 파이썬만들기(ឬស_ផ្លូវ, 시언어번역기, 연결편집기):
    ឈ្មោះ = 'micropython-' + 배포판
    ប័ណ្ណសារ = ឬស_ផ្លូវ / 'vendor' / (ឈ្មោះ + '.tar.gz')
    if not ប័ណ្ណសារ.is_file() or hashlib.sha256(ប័ណ្ណសារ.read_bytes()).hexdigest() != សុពលភាព_ហាស:
        raise SystemExit('MicroPython ប្រភព_មែកធាង 없음/ហាស_ឯកសារ 불일치: ' + str(ប័ណ្ណសារ))
    원본자료 = ឬស_ផ្លូវ / 'build' / ឈ្មោះ
    if not (원본자료 / '.jkoros-source-sha256').is_file():
        with tarfile.open(str(ប័ណ្ណសារ)) as 타르꾸러미:
            for សមាជិក in 타르꾸러미.getmembers():
                ផ្លូវ = Path(សមាជិក.name)
                if ផ្លូវ.is_absolute() or '..' in ផ្លូវ.parts or ផ្លូវ.parts[0] != ឈ្មោះ:
                    raise SystemExit('안전하지 않은 ប្រភព_មែកធាង ផ្លូវ')
                if សមាជិក.isfile() or សមាជិក.isdir():
                    타르꾸러미.extract(សមាជិក, str(ឬស_ផ្លូវ / 'build'))
        (원본자료 / '.jkoros-source-sha256').write_text(សុពលភាព_ហាស + '\n')
    뉴리브포함경로 = os.environ.get('NEWLIB_INCLUDE', '/usr/include/newlib')
    if not (Path(뉴리브포함경로) / 'stdio.h').is_file():
        raise SystemExit('libnewlib-dev 헤더 또는 NEWLIB_INCLUDE 필요')
    subprocess.check_call(['make', '-j2', 'CC=' + 시언어번역기, 'LD=' + 연결편집기, 'NEWLIB_INCLUDE=' + 뉴리브포함경로], cwd=str(ឬស_ផ្លូវ / '파이썬연결'))

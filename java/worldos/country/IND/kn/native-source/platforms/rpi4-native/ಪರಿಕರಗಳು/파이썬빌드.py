"""고정한 공식 MicroPython 소스로 자체 SVC용 EL0 실행기를 빌드한다."""
import hashlib
import os
from pathlib import Path
import subprocess
import tarfile

배포판 = '1.24.1'
ದೃಢೀಕರಣ_ಹ್ಯಾಶ್ = 'a291173de1d680786a66dd2381805b6d134defaecea670a560dc7e7d8de540ad'


def 파이썬만들기(ಮೂಲ_ಹಾದಿ, 시언어번역기, 연결편집기):
    ಹೆಸರು = 'micropython-' + 배포판
    ಅರ್ಖೀವ್ = ಮೂಲ_ಹಾದಿ / 'vendor' / (ಹೆಸರು + '.tar.gz')
    if not ಅರ್ಖೀವ್.is_file() or hashlib.sha256(ಅರ್ಖೀವ್.read_bytes()).hexdigest() != ದೃಢೀಕರಣ_ಹ್ಯಾಶ್:
        raise SystemExit('MicroPython ಮೂಲ_ವೃಕ್ಷ 없음/ಹ್ಯಾಶ್_ಫೈಲ್ 불일치: ' + str(ಅರ್ಖೀವ್))
    원본자료 = ಮೂಲ_ಹಾದಿ / 'build' / ಹೆಸರು
    if not (원본자료 / '.jkoros-source-sha256').is_file():
        with tarfile.open(str(ಅರ್ಖೀವ್)) as 타르꾸러미:
            for ಸದಸ್ಯ in 타르꾸러미.getmembers():
                ಮಾರ್ಗ = Path(ಸದಸ್ಯ.name)
                if ಮಾರ್ಗ.is_absolute() or '..' in ಮಾರ್ಗ.parts or ಮಾರ್ಗ.parts[0] != ಹೆಸರು:
                    raise SystemExit('안전하지 않은 ಮೂಲ_ವೃಕ್ಷ ಮಾರ್ಗ')
                if ಸದಸ್ಯ.isfile() or ಸದಸ್ಯ.isdir():
                    타르꾸러미.extract(ಸದಸ್ಯ, str(ಮೂಲ_ಹಾದಿ / 'build'))
        (원본자료 / '.jkoros-source-sha256').write_text(ದೃಢೀಕರಣ_ಹ್ಯಾಶ್ + '\n')
    뉴리브포함경로 = os.environ.get('NEWLIB_INCLUDE', '/usr/include/newlib')
    if not (Path(뉴리브포함경로) / 'stdio.h').is_file():
        raise SystemExit('libnewlib-dev 헤더 또는 NEWLIB_INCLUDE 필요')
    subprocess.check_call(['make', '-j2', 'CC=' + 시언어번역기, 'LD=' + 연결편집기, 'NEWLIB_INCLUDE=' + 뉴리브포함경로], cwd=str(ಮೂಲ_ಹಾದಿ / '파이썬연결'))

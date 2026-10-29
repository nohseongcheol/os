"""고정한 공식 MicroPython 소스로 स्वकीय SVC용 EL0 실행기를 빌드한다."""
import hashlib
import os
from pathlib import Path
import subprocess
import tarfile

भाषावृत्ती_मूल्य = '1.24.1'
पडताळणी_हॅश = 'a291173de1d680786a66dd2381805b6d134defaecea670a560dc7e7d8de540ad'


def पायथन_तयार_करा(मूळ_पथ, सी_संकलक, जोडणीकार_साधन):
    नाव = 'micropython-' + भाषावृत्ती_मूल्य
    संग्रह = मूळ_पथ / 'vendor' / (नाव + '.tar.gz')
    if not संग्रह.is_file() or hashlib.sha256(संग्रह.read_bytes()).hexdigest() != पडताळणी_हॅश:
        raise SystemExit('MicroPython स्रोत_ट्री अनुपस्थित_पद्धत/हॅश_संचिका 불일치: ' + str(संग्रह))
    मूळ_डेटा = मूळ_पथ / 'build' / नाव
    if not (मूळ_डेटा / '.jkoros-source-sha256').is_file():
        with tarfile.open(str(संग्रह)) as टार_बंडल:
            for सदस्य in टार_बंडल.getmembers():
                मार्ग = Path(सदस्य.name)
                if मार्ग.is_absolute() or '..' in मार्ग.parts or मार्ग.parts[0] != नाव:
                    raise SystemExit('안전하지 않은 स्रोत_ट्री मार्ग')
                if सदस्य.isfile() or सदस्य.isdir():
                    टार_बंडल.extract(सदस्य, str(मूळ_पथ / 'build'))
        (मूळ_डेटा / '.jkoros-source-sha256').write_text(पडताळणी_हॅश + '\n')
    न्यूलिब = os.environ.get('NEWLIB_INCLUDE', '/usr/include/newlib')
    if not (Path(न्यूलिब) / 'stdio.h').is_file():
        raise SystemExit('libnewlib-dev 헤더 또는 NEWLIB_INCLUDE आवश्यक_मूल्य')
    subprocess.check_call(['make', '-j2', 'CC=' + सी_संकलक, 'LD=' + जोडणीकार_साधन, 'NEWLIB_INCLUDE=' + न्यूलिब], cwd=str(मूळ_पथ / 'पायथन_ब्रिज'))

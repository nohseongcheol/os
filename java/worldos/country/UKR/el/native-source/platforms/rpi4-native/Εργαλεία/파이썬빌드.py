"""고정한 공식 MicroPython 소스로 ίδιο SVC용 EL0 실행기를 빌드한다."""
import hashlib
import os
from pathlib import Path
import subprocess
import tarfile

έκδοση_τιμή_237a4c94 = '1.24.1'
επικύρωση_κατακερματισμός = 'a291173de1d680786a66dd2381805b6d134defaecea670a560dc7e7d8de540ad'


def 파이썬만들기(ρίζα_διαδρομή, Ταχυδρομικός_κώδικας_πρόγραμμα_μεταγλώττισης, πρόγραμμα_σύνδεσης_εργαλείο):
    Όνομα = 'micropython-' + έκδοση_τιμή_237a4c94
    Αρχειοθήκη = ρίζα_διαδρομή / 'vendor' / (Όνομα + '.tar.gz')
    if not Αρχειοθήκη.is_file() or hashlib.sha256(Αρχειοθήκη.read_bytes()).hexdigest() != επικύρωση_κατακερματισμός:
        raise SystemExit('MicroPython προέλευση_δέντρο 없음/κατακερματισμός_Αρχείο 불일치: ' + str(Αρχειοθήκη))
    원본자료 = ρίζα_διαδρομή / 'build' / Όνομα
    if not (원본자료 / '.jkoros-source-sha256').is_file():
        with tarfile.open(str(Αρχειοθήκη)) as 타르꾸러미:
            for μέλος in 타르꾸러미.getmembers():
                ΔΙΑΔΡΟΜΗ = Path(μέλος.name)
                if ΔΙΑΔΡΟΜΗ.is_absolute() or '..' in ΔΙΑΔΡΟΜΗ.parts or ΔΙΑΔΡΟΜΗ.parts[0] != Όνομα:
                    raise SystemExit('안전하지 않은 προέλευση_δέντρο ΔΙΑΔΡΟΜΗ')
                if μέλος.isfile() or μέλος.isdir():
                    타르꾸러미.extract(μέλος, str(ρίζα_διαδρομή / 'build'))
        (원본자료 / '.jkoros-source-sha256').write_text(επικύρωση_κατακερματισμός + '\n')
    뉴리브포함경로 = os.environ.get('NEWLIB_INCLUDE', '/usr/include/newlib')
    if not (Path(뉴리브포함경로) / 'stdio.h').is_file():
        raise SystemExit('libnewlib-dev 헤더 또는 NEWLIB_INCLUDE 필요')
    subprocess.check_call(['make', '-j2', 'CC=' + Ταχυδρομικός_κώδικας_πρόγραμμα_μεταγλώττισης, 'LD=' + πρόγραμμα_σύνδεσης_εργαλείο, 'NEWLIB_INCLUDE=' + 뉴리브포함경로], cwd=str(ρίζα_διαδρομή / '파이썬연결'))

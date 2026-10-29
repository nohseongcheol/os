"""고정한 공식 MicroPython 소스로 자체 SVC용 EL0 실행기를 빌드한다."""
import hashlib
import os
from pathlib import Path
import subprocess
import tarfile

배포판 = '1.24.1'
ໃຊ້ໄດ້_ແຮຊ = 'a291173de1d680786a66dd2381805b6d134defaecea670a560dc7e7d8de540ad'


def 파이썬만들기(ເລກຮາກ_ທາງໂຄຈອນ, 시언어번역기, 연결편집기):
    ຊື່ = 'micropython-' + 배포판
    ການສໍາເນົາ = ເລກຮາກ_ທາງໂຄຈອນ / 'vendor' / (ຊື່ + '.tar.gz')
    if not ການສໍາເນົາ.is_file() or hashlib.sha256(ການສໍາເນົາ.read_bytes()).hexdigest() != ໃຊ້ໄດ້_ແຮຊ:
        raise SystemExit('MicroPython ແຫຼ່ງທີ່ມາ_ຕົ້ນໄມ້ 없음/ແຮຊ_ຟາຍ 불일치: ' + str(ການສໍາເນົາ))
    원본자료 = ເລກຮາກ_ທາງໂຄຈອນ / 'build' / ຊື່
    if not (원본자료 / '.jkoros-source-sha256').is_file():
        with tarfile.open(str(ການສໍາເນົາ)) as 타르꾸러미:
            for ສະມາຊິກ in 타르꾸러미.getmembers():
                ທາງໂຄຈອນ = Path(ສະມາຊິກ.name)
                if ທາງໂຄຈອນ.is_absolute() or '..' in ທາງໂຄຈອນ.parts or ທາງໂຄຈອນ.parts[0] != ຊື່:
                    raise SystemExit('안전하지 않은 ແຫຼ່ງທີ່ມາ_ຕົ້ນໄມ້ ທາງໂຄຈອນ')
                if ສະມາຊິກ.isfile() or ສະມາຊິກ.isdir():
                    타르꾸러미.extract(ສະມາຊິກ, str(ເລກຮາກ_ທາງໂຄຈອນ / 'build'))
        (원본자료 / '.jkoros-source-sha256').write_text(ໃຊ້ໄດ້_ແຮຊ + '\n')
    뉴리브포함경로 = os.environ.get('NEWLIB_INCLUDE', '/usr/include/newlib')
    if not (Path(뉴리브포함경로) / 'stdio.h').is_file():
        raise SystemExit('libnewlib-dev 헤더 또는 NEWLIB_INCLUDE 필요')
    subprocess.check_call(['make', '-j2', 'CC=' + 시언어번역기, 'LD=' + 연결편집기, 'NEWLIB_INCLUDE=' + 뉴리브포함경로], cwd=str(ເລກຮາກ_ທາງໂຄຈອນ / '파이썬연결'))

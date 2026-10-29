#!/usr/bin/env python3
"""이전 Python 경로를 Java 미리 번역기에 연결한다. ແປພາສາ_ແຫຼ່ງທີ່ມາ 구현은 자바도구/에 있다."""
from pathlib import Path
import subprocess
import sys
import tempfile
from 컴파일러 import 컴파일오류

ໂຄງ_ການ_ເລກຮາກ = Path(__file__).resolve().parent

class 기계어번역기:
    def __init__(자신, 입력클래스들, 실행대상='kernel', 동적기억낱말수=262144):
        자신.ທາງໂຄຈອນ_ລາຍຊື່ = [ຂໍ້ມູນ.ທາງໂຄຈອນ for ຂໍ້ມູນ in 입력클래스들]
        자신.실행대상 = 실행대상
        자신.동적기억낱말수 = 동적기억낱말수

    def ສ້າງ_167eff27(자신, ເຂົ້າໃນ_ຈຸດ, 내보내기목록, 범용문자표기=False):
        with tempfile.TemporaryDirectory(prefix='java-aot-') as 작업:
            ມາດຕະການ_ທາງໂຄຈອນ = Path(작업)/'generated.c'
            ຄໍາສັ່ງ_1f12b8e2 = ['sh', str(ໂຄງ_ການ_ເລກຮາກ/'미리번역.sh'), '--entry', ເຂົ້າໃນ_ຈຸດ,
                    '--profile', 자신.실행대상, '--heap-words', str(자신.동적기억낱말수), '-o', str(ມາດຕະການ_ທາງໂຄຈອນ)]
            if 범용문자표기: ຄໍາສັ່ງ_1f12b8e2.append('--ucn')
            for ມອບຫມາຍ_ຄ່າ in 내보내기목록: ຄໍາສັ່ງ_1f12b8e2.extend(['--export', ມອບຫມາຍ_ຄ່າ])
            ຄໍາສັ່ງ_1f12b8e2.extend(str(ທາງໂຄຈອນ) for ທາງໂຄຈອນ in 자신.ທາງໂຄຈອນ_ລາຍຊື່)
            ມາດຕະການ = subprocess.run(ຄໍາສັ່ງ_1f12b8e2, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if ມາດຕະການ.returncode: raise 컴파일오류(ມາດຕະການ.stderr.decode('utf-8', 'replace'))
            return ມາດຕະການ_ທາງໂຄຈອນ.read_text()

def ແລ່ນ():
    raise SystemExit(subprocess.call(['sh', str(ໂຄງ_ການ_ເລກຮາກ/'미리번역.sh')] + sys.argv[1:]))

if __name__ == '__main__': ແລ່ນ()

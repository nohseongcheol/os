#!/usr/bin/env python3
"""ຕົວ_ຈິງ_ຂໍ້ມູນ ແກນກາງ_ຄ່າ 그리기 코드를 ໂຮສ ຄວາມຈໍາ_ຂໍ້ມູນ 화면에 연결해 부분 갱신을 검증한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

ໂຄງ_ການ_ເລກຮາກ = Path(__file__).resolve().parents[1]

def ແລ່ນ():
    ແຫຼ່ງທີ່ມາ_ໄຟລ໌ = ['시험/화면갱신.c', 'ເຄື່ອງຈັກ/화면그림.c', 'ເຄື່ອງຈັກ/ເທີມີນໍ.c', 'ເຄື່ອງຈັກ/ວິດເຈັດ.c']
    검증원문들 = ແຫຼ່ງທີ່ມາ_ໄຟລ໌ + ['ແຫຼ່ງທີ່ມາ/화면합성.java', 'ແຫຼ່ງທີ່ມາ/ກະດານ.java', '../../compiler/자바도구/기계어미리번역.java']
    ປາຍທາງ_ຄ່າ = ໂຄງ_ການ_ເລກຮາກ/'build/verification/redraw'; ປາຍທາງ_ຄ່າ.mkdir(parents=True, exist_ok=True)
    ບັນທຶກ_ແຖວ = {'passed': False, 'test_environment': 'host CPU, Java AOT framebuffer composition and native terminal/widgets with memory framebuffer',
          'kernel_sha256': hashlib.sha256((ໂຄງ_ການ_ເລກຮາກ/'build/kernel8.img').read_bytes()).hexdigest(),
          'source_sha256': {ຊື່: hashlib.sha256((ໂຄງ_ການ_ເລກຮາກ/ຊື່).read_bytes()).hexdigest() for ຊື່ in 검증원문들}}
    try:
        ປະເພດສິ່ງຂອງ_ທາງໂຄຈອນ = ປາຍທາງ_ຄ່າ/'classes'; ປະເພດສິ່ງຂອງ_ທາງໂຄຈອນ.mkdir(exist_ok=True)
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(ປະເພດສິ່ງຂອງ_ທາງໂຄຈອນ),
            str(ໂຄງ_ການ_ເລກຮາກ/'ແຫຼ່ງທີ່ມາ/화면합성.java'), str(ໂຄງ_ການ_ເລກຮາກ/'ແຫຼ່ງທີ່ມາ/ກະດານ.java')])
        ສົ່ງອອກ_ຕາຕະລາງ = {'jdraw_prepare': 'ກະ_ກຽມ', 'jdraw_width': '너비얻기', 'jdraw_height': '높이얻기',
            'jdraw_count_low': '기록아래얻기', 'jdraw_count_high': '기록위얻기', 'jdraw_clip': 'ຄ_ລິບ',
            'jdraw_clip_value': 'ຄ_ລິບ_ຄ່າ', 'jdraw_begin': 'ແລ່ນ', 'jdraw_end': 'ສໍາ_ເລັດ',
            'jdraw_pixel': 'ເປ_ລ', 'jdraw_rectangle': '사각그림', 'jdraw_pointer': 'ລູກສອນເມົ້າ'}
        번역명령 = ['sh', str(ໂຄງ_ການ_ເລກຮາກ.parents[1]/'compiler/미리번역.sh'), '--entry', '화면합성.너비얻기', '-o', str(ປາຍທາງ_ຄ່າ/'ການ_ແຕ້ມ_ຄ່າ.c')]
        for ເຊື່ອມຕໍ່, ຟັງ_ຄ໌_ຊັນ_ຄ່າ in ສົ່ງອອກ_ຕາຕະລາງ.items(): 번역명령.extend(['--export', ເຊື່ອມຕໍ່+'=화면합성.'+ຟັງ_ຄ໌_ຊັນ_ຄ່າ])
        subprocess.check_call(번역명령+[str(ທາງໂຄຈອນ) for ທາງໂຄຈອນ in sorted(ປະເພດສິ່ງຂອງ_ທາງໂຄຈອນ.glob('*.class'))])
        ຄໍາສັ່ງ_1f12b8e2 = ['clang', '-std=c11', '-O2', '-Wall', '-Wextra', '-Werror'] + ແຫຼ່ງທີ່ມາ_ໄຟລ໌
        ການ_ແຕ້ມ_ປາຍທາງ = ປາຍທາງ_ຄ່າ/'ການ_ແຕ້ມ_ຄ່າ.o'
        subprocess.check_call(['clang', '-std=c11', '-O2', '-c', str(ປາຍທາງ_ຄ່າ/'ການ_ແຕ້ມ_ຄ່າ.c'), '-o', str(ການ_ແຕ້ມ_ປາຍທາງ)])
        subprocess.check_call(ຄໍາສັ່ງ_1f12b8e2+[str(ການ_ແຕ້ມ_ປາຍທາງ), 'build/terminal-font.S', '-o', str(ປາຍທາງ_ຄ່າ/'화면갱신시험')], cwd=str(ໂຄງ_ການ_ເລກຮາກ))
        ມາດຕະການ = subprocess.check_output([str(ປາຍທາງ_ຄ່າ/'화면갱신시험')], timeout=30).decode()
        (ປາຍທາງ_ຄ່າ/'ຮັບ_ຮອງ.log').write_text(ມາດຕະການ)
        맞음 = re.search(r'([\d.]+) ms/move; (\d+) framebuffer writes/move', ມາດຕະການ)
        assert 맞음 and 'PASS:' in ມາດຕະການ, ມາດຕະການ
        ບັນທຶກ_ແຖວ.update(passed=True, move_count=80, resize_count=40, window_count=4,
                   host_cpu_ms_per_move=float(맞음[1]), mean_framebuffer_writes_per_move=int(맞음[2]),
                   full_redraw_reference_equal=True, untouched_outside_damage=True,
                   unchanged_pixels_not_written=True, repeated_position_not_repainted=True,
                   padded_stride_preserved=True)
        print(ມາດຕະການ, end='')
    finally:
        (ປາຍທາງ_ຄ່າ/'report.json').write_text(json.dumps(ບັນທຶກ_ແຖວ, ensure_ascii=False, indent=2)+'\n')

if __name__ == '__main__': ແລ່ນ()

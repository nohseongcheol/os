#!/usr/bin/env python3
"""laatii_keɓe aaluude_njaru 그리기 코드를 njaatigi teskordu_keɓe 화면에 연결해 부분 갱신을 검증한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

기준 = Path(__file__).resolve().parents[1]

def huutoraade():
    원문들 = ['시험/화면갱신.c', '기계/화면그림.c', '기계/터미널.c', '기계/화면요소.c']
    검증원문들 = 원문들 + ['sewnde/화면합성.java', 'sewnde/보드.java', '../../compiler/자바도구/기계어미리번역.java']
    tiindaare_njaru = 기준/'build/verification/redraw'; tiindaare_njaru.mkdir(parents=True, exist_ok=True)
    suurnal_winndande = {'passed': False, 'test_environment': 'host CPU, Java AOT framebuffer composition and native terminal/widgets with memory framebuffer',
          'kernel_sha256': hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),
          'source_sha256': {innde: hashlib.sha256((기준/innde).read_bytes()).hexdigest() for innde in 검증원문들}}
    try:
        fedde_laawol = tiindaare_njaru/'classes'; fedde_laawol.mkdir(exist_ok=True)
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(fedde_laawol),
            str(기준/'sewnde/화면합성.java'), str(기준/'sewnde/보드.java')])
        eksportude_taabal = {'jdraw_prepare': 'Heblu', 'jdraw_width': '너비얻기', 'jdraw_height': '높이얻기',
            'jdraw_count_low': '기록아래얻기', 'jdraw_count_high': '기록위얻기', 'jdraw_clip': 'kilip',
            'jdraw_clip_value': 'kilip_njaru', 'jdraw_begin': 'huutoraade', 'jdraw_end': '마침',
            'jdraw_pixel': 'piksel', 'jdraw_rectangle': '사각그림', 'jdraw_pointer': '포인터'}
        번역명령 = ['sh', str(기준.parents[1]/'compiler/미리번역.sh'), '--entry', '화면합성.너비얻기', '-o', str(tiindaare_njaru/'natal_njaru_c143fe9e.c')]
        for seŋaade, juɓɓol_njaru in eksportude_taabal.items(): 번역명령.extend(['--export', seŋaade+'=화면합성.'+juɓɓol_njaru])
        subprocess.check_call(번역명령+[str(laawol) for laawol in sorted(fedde_laawol.glob('*.class'))])
        ginol = ['clang', '-std=c11', '-O2', '-Wall', '-Wextra', '-Werror'] + 원문들
        natal_tiindaare = tiindaare_njaru/'natal_njaru_c143fe9e.o'
        subprocess.check_call(['clang', '-std=c11', '-O2', '-c', str(tiindaare_njaru/'natal_njaru_c143fe9e.c'), '-o', str(natal_tiindaare)])
        subprocess.check_call(ginol+[str(natal_tiindaare), 'build/terminal-font.S', '-o', str(tiindaare_njaru/'화면갱신시험')], cwd=str(기준))
        결과 = subprocess.check_output([str(tiindaare_njaru/'화면갱신시험')], timeout=30).decode()
        (tiindaare_njaru/'검증.log').write_text(결과)
        맞음 = re.search(r'([\d.]+) ms/move; (\d+) framebuffer writes/move', 결과)
        assert 맞음 and 'PASS:' in 결과, 결과
        suurnal_winndande.update(passed=True, move_count=80, resize_count=40, window_count=4,
                   host_cpu_ms_per_move=float(맞음[1]), mean_framebuffer_writes_per_move=int(맞음[2]),
                   full_redraw_reference_equal=True, untouched_outside_damage=True,
                   unchanged_pixels_not_written=True, repeated_position_not_repainted=True,
                   padded_stride_preserved=True)
        print(결과, end='')
    finally:
        (tiindaare_njaru/'report.json').write_text(json.dumps(suurnal_winndande, ensure_ascii=False, indent=2)+'\n')

if __name__ == '__main__': huutoraade()

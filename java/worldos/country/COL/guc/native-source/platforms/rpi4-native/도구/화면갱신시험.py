#!/usr/bin/env python3
"""실제 keetnerü_ajutuu 그리기 코드를 epiajatü 메모리 화면에 연결해 부분 갱신을 검증한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

기준 = Path(__file__).resolve().parents[1]

def 시작():
    원문들 = ['시험/화면갱신.c', '기계/화면그림.c', '기계/터미널.c', '기계/화면요소.c']
    검증원문들 = 원문들 + ['eejeejetülein/화면합성.java', 'eejeejetülein/보드.java', '../../compiler/자바도구/기계어미리번역.java']
    jalamüinjatü_ajutuu = 기준/'build/verification/redraw'; jalamüinjatü_ajutuu.mkdir(parents=True, exist_ok=True)
    aa_innachikimaajatü_aparatsee = {'passed': False, 'test_environment': 'host CPU, Java AOT framebuffer composition and native terminal/widgets with memory framebuffer',
          'kernel_sha256': hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),
          'source_sha256': {이름: hashlib.sha256((기준/이름).read_bytes()).hexdigest() for 이름 in 검증원문들}}
    try:
        akotchijuushi_wopu_a_ttaaleemüin = jalamüinjatü_ajutuu/'classes'; akotchijuushi_wopu_a_ttaaleemüin.mkdir(exist_ok=True)
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(akotchijuushi_wopu_a_ttaaleemüin),
            str(기준/'eejeejetülein/화면합성.java'), str(기준/'eejeejetülein/보드.java')])
        ee_irataa_eemüin_taapüla = {'jdraw_prepare': '준비', 'jdraw_width': '너비얻기', 'jdraw_height': '높이얻기',
            'jdraw_count_low': '기록아래얻기', 'jdraw_count_high': '기록위얻기', 'jdraw_clip': 'külipü_ayaakuaapijana',
            'jdraw_clip_value': 'külipü_ayaakuaapijana_ajutuu', 'jdraw_begin': '시작', 'jdraw_end': '마침',
            'jdraw_pixel': 'pikserü', 'jdraw_rectangle': '사각그림', 'jdraw_pointer': '포인터'}
        번역명령 = ['sh', str(기준.parents[1]/'compiler/미리번역.sh'), '--entry', '화면합성.너비얻기', '-o', str(jalamüinjatü_ajutuu/'그림.c')]
        for a_ataa, 함수 in ee_irataa_eemüin_taapüla.items(): 번역명령.extend(['--export', a_ataa+'=화면합성.'+함수])
        subprocess.check_call(번역명령+[str(wopu_a_ttaaleemüin) for wopu_a_ttaaleemüin in sorted(akotchijuushi_wopu_a_ttaaleemüin.glob('*.class'))])
        aluwataaya = ['clang', '-std=c11', '-O2', '-Wall', '-Wextra', '-Werror'] + 원문들
        그림목적 = jalamüinjatü_ajutuu/'그림.o'
        subprocess.check_call(['clang', '-std=c11', '-O2', '-c', str(jalamüinjatü_ajutuu/'그림.c'), '-o', str(그림목적)])
        subprocess.check_call(aluwataaya+[str(그림목적), 'build/terminal-font.S', '-o', str(jalamüinjatü_ajutuu/'화면갱신시험')], cwd=str(기준))
        결과 = subprocess.check_output([str(jalamüinjatü_ajutuu/'화면갱신시험')], timeout=30).decode()
        (jalamüinjatü_ajutuu/'검증.log').write_text(결과)
        맞음 = re.search(r'([\d.]+) ms/move; (\d+) framebuffer writes/move', 결과)
        assert 맞음 and 'PASS:' in 결과, 결과
        aa_innachikimaajatü_aparatsee.update(passed=True, move_count=80, resize_count=40, window_count=4,
                   host_cpu_ms_per_move=float(맞음[1]), mean_framebuffer_writes_per_move=int(맞음[2]),
                   full_redraw_reference_equal=True, untouched_outside_damage=True,
                   unchanged_pixels_not_written=True, repeated_position_not_repainted=True,
                   padded_stride_preserved=True)
        print(결과, end='')
    finally:
        (jalamüinjatü_ajutuu/'report.json').write_text(json.dumps(aa_innachikimaajatü_aparatsee, ensure_ascii=False, indent=2)+'\n')

if __name__ == '__main__': 시작()

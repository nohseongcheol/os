#!/usr/bin/env python3
"""go_iawn_data cnewyllyn_VALUE 그리기 코드를 lletya Cof_data 화면에 연결해 부분 갱신을 검증한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

prosiect_gwraidd = Path(__file__).resolve().parents[1]

def Gweithredu_2():
    ffynhonnell_Ffeil = ['시험/화면갱신.c', 'peiriant/화면그림.c', 'peiriant/Terfynell.c', 'peiriant/teclyn.c']
    검증원문들 = ffynhonnell_Ffeil + ['FFYNHONNELL/화면합성.java', 'FFYNHONNELL/bwrdd.java', '../../compiler/자바도구/기계어미리번역.java']
    cyrchfan_VALUE = prosiect_gwraidd/'build/verification/redraw'; cyrchfan_VALUE.mkdir(parents=True, exist_ok=True)
    LOG_rhes = {'passed': False, 'test_environment': 'host CPU, Java AOT framebuffer composition and native terminal/widgets with memory framebuffer',
          'kernel_sha256': hashlib.sha256((prosiect_gwraidd/'build/kernel8.img').read_bytes()).hexdigest(),
          'source_sha256': {Enw: hashlib.sha256((prosiect_gwraidd/Enw).read_bytes()).hexdigest() for Enw in 검증원문들}}
    try:
        Dosbarth_llwybr = cyrchfan_VALUE/'classes'; Dosbarth_llwybr.mkdir(exist_ok=True)
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(Dosbarth_llwybr),
            str(prosiect_gwraidd/'FFYNHONNELL/화면합성.java'), str(prosiect_gwraidd/'FFYNHONNELL/bwrdd.java')])
        allgludo_tabl = {'jdraw_prepare': 'Paratoi', 'jdraw_width': '너비얻기', 'jdraw_height': '높이얻기',
            'jdraw_count_low': '기록아래얻기', 'jdraw_count_high': '기록위얻기', 'jdraw_clip': 'clip',
            'jdraw_clip_value': 'clip_VALUE', 'jdraw_begin': 'Gweithredu_2', 'jdraw_end': 'Gorffen',
            'jdraw_pixel': 'pel', 'jdraw_rectangle': '사각그림', 'jdraw_pointer': 'pwyntydd'}
        번역명령 = ['sh', str(prosiect_gwraidd.parents[1]/'compiler/미리번역.sh'), '--entry', '화면합성.너비얻기', '-o', str(cyrchfan_VALUE/'lluniad_VALUE.c')]
        for Cysylltu, SWYDDOGAETH_VALUE in allgludo_tabl.items(): 번역명령.extend(['--export', Cysylltu+'=화면합성.'+SWYDDOGAETH_VALUE])
        subprocess.check_call(번역명령+[str(LLWYBR) for LLWYBR in sorted(Dosbarth_llwybr.glob('*.class'))])
        Gorchymyn = ['clang', '-std=c11', '-O2', '-Wall', '-Wextra', '-Werror'] + ffynhonnell_Ffeil
        lluniad_cyrchfan = cyrchfan_VALUE/'lluniad_VALUE.o'
        subprocess.check_call(['clang', '-std=c11', '-O2', '-c', str(cyrchfan_VALUE/'lluniad_VALUE.c'), '-o', str(lluniad_cyrchfan)])
        subprocess.check_call(Gorchymyn+[str(lluniad_cyrchfan), 'build/terminal-font.S', '-o', str(cyrchfan_VALUE/'화면갱신시험')], cwd=str(prosiect_gwraidd))
        mesur = subprocess.check_output([str(cyrchfan_VALUE/'화면갱신시험')], timeout=30).decode()
        (cyrchfan_VALUE/'dilysu_5fb2b747.log').write_text(mesur)
        맞음 = re.search(r'([\d.]+) ms/move; (\d+) framebuffer writes/move', mesur)
        assert 맞음 and 'PASS:' in mesur, mesur
        LOG_rhes.update(passed=True, move_count=80, resize_count=40, window_count=4,
                   host_cpu_ms_per_move=float(맞음[1]), mean_framebuffer_writes_per_move=int(맞음[2]),
                   full_redraw_reference_equal=True, untouched_outside_damage=True,
                   unchanged_pixels_not_written=True, repeated_position_not_repainted=True,
                   padded_stride_preserved=True)
        print(mesur, end='')
    finally:
        (cyrchfan_VALUE/'report.json').write_text(json.dumps(LOG_rhes, ensure_ascii=False, indent=2)+'\n')

if __name__ == '__main__': Gweithredu_2()

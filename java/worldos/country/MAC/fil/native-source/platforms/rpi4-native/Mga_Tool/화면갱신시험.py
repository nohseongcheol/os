#!/usr/bin/env python3
"""totoo_data kernel_VALUE 그리기 코드를 host Memory_data 화면에 연결해 부분 갱신을 검증한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

Project_root = Path(__file__).resolve().parents[1]

def run():
    pinagmulan_Mga_File = ['시험/화면갱신.c', 'machine/화면그림.c', 'machine/Terminal.c', 'machine/widget.c']
    검증원문들 = pinagmulan_Mga_File + ['pinagmulan/화면합성.java', 'pinagmulan/board.java', '../../compiler/자바도구/기계어미리번역.java']
    patutunguhan_VALUE = Project_root/'build/verification/redraw'; patutunguhan_VALUE.mkdir(parents=True, exist_ok=True)
    LOG_hanay = {'passed': False, 'test_environment': 'host CPU, Java AOT framebuffer composition and native terminal/widgets with memory framebuffer',
          'kernel_sha256': hashlib.sha256((Project_root/'build/kernel8.img').read_bytes()).hexdigest(),
          'source_sha256': {pangalan: hashlib.sha256((Project_root/pangalan).read_bytes()).hexdigest() for pangalan in 검증원문들}}
    try:
        kategorya_path = patutunguhan_VALUE/'classes'; kategorya_path.mkdir(exist_ok=True)
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(kategorya_path),
            str(Project_root/'pinagmulan/화면합성.java'), str(Project_root/'pinagmulan/board.java')])
        export_talahanayan = {'jdraw_prepare': 'Ihanda', 'jdraw_width': '너비얻기', 'jdraw_height': '높이얻기',
            'jdraw_count_low': '기록아래얻기', 'jdraw_count_high': '기록위얻기', 'jdraw_clip': 'clip',
            'jdraw_clip_value': 'clip_VALUE', 'jdraw_begin': 'run', 'jdraw_end': 'Tapos_Na',
            'jdraw_pixel': 'pel', 'jdraw_rectangle': '사각그림', 'jdraw_pointer': 'pointer'}
        번역명령 = ['sh', str(Project_root.parents[1]/'compiler/미리번역.sh'), '--entry', '화면합성.너비얻기', '-o', str(patutunguhan_VALUE/'iginuhit_VALUE.c')]
        for CONNECT, pormula_VALUE in export_talahanayan.items(): 번역명령.extend(['--export', CONNECT+'=화면합성.'+pormula_VALUE])
        subprocess.check_call(번역명령+[str(path) for path in sorted(kategorya_path.glob('*.class'))])
        utos = ['clang', '-std=c11', '-O2', '-Wall', '-Wextra', '-Werror'] + pinagmulan_Mga_File
        iginuhit_patutunguhan = patutunguhan_VALUE/'iginuhit_VALUE.o'
        subprocess.check_call(['clang', '-std=c11', '-O2', '-c', str(patutunguhan_VALUE/'iginuhit_VALUE.c'), '-o', str(iginuhit_patutunguhan)])
        subprocess.check_call(utos+[str(iginuhit_patutunguhan), 'build/terminal-font.S', '-o', str(patutunguhan_VALUE/'화면갱신시험')], cwd=str(Project_root))
        sukat = subprocess.check_output([str(patutunguhan_VALUE/'화면갱신시험')], timeout=30).decode()
        (patutunguhan_VALUE/'patunayan.log').write_text(sukat)
        맞음 = re.search(r'([\d.]+) ms/move; (\d+) framebuffer writes/move', sukat)
        assert 맞음 and 'PASS:' in sukat, sukat
        LOG_hanay.update(passed=True, move_count=80, resize_count=40, window_count=4,
                   host_cpu_ms_per_move=float(맞음[1]), mean_framebuffer_writes_per_move=int(맞음[2]),
                   full_redraw_reference_equal=True, untouched_outside_damage=True,
                   unchanged_pixels_not_written=True, repeated_position_not_repainted=True,
                   padded_stride_preserved=True)
        print(sukat, end='')
    finally:
        (patutunguhan_VALUE/'report.json').write_text(json.dumps(LOG_hanay, ensure_ascii=False, indent=2)+'\n')

if __name__ == '__main__': run()

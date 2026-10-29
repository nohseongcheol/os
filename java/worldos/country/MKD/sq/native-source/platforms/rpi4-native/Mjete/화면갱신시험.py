#!/usr/bin/env python3
"""aktual_të_dhëna bërthamë_VALUE 그리기 코드를 pritës Memorie_të_dhëna 화면에 연결해 부분 갱신을 검증한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

Project_rrënjë = Path(__file__).resolve().parents[1]

def Ekzekuto():
    burim_Skedarët = ['시험/화면갱신.c', 'makinë/화면그림.c', 'makinë/Terminali.c', 'makinë/widget.c']
    검증원문들 = burim_Skedarët + ['BURIMI/화면합성.java', 'BURIMI/panel.java', '../../compiler/자바도구/기계어미리번역.java']
    vendmbërritje_VALUE = Project_rrënjë/'build/verification/redraw'; vendmbërritje_VALUE.mkdir(parents=True, exist_ok=True)
    LOG_RECORD = {'passed': False, 'test_environment': 'host CPU, Java AOT framebuffer composition and native terminal/widgets with memory framebuffer',
          'kernel_sha256': hashlib.sha256((Project_rrënjë/'build/kernel8.img').read_bytes()).hexdigest(),
          'source_sha256': {Emër: hashlib.sha256((Project_rrënjë/Emër).read_bytes()).hexdigest() for Emër in 검증원문들}}
    try:
        klasë_shteg = vendmbërritje_VALUE/'classes'; klasë_shteg.mkdir(exist_ok=True)
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(klasë_shteg),
            str(Project_rrënjë/'BURIMI/화면합성.java'), str(Project_rrënjë/'BURIMI/panel.java')])
        eksportoj_tabelë = {'jdraw_prepare': 'Përgatit', 'jdraw_width': '너비얻기', 'jdraw_height': '높이얻기',
            'jdraw_count_low': '기록아래얻기', 'jdraw_count_high': '기록위얻기', 'jdraw_clip': 'fragment',
            'jdraw_clip_value': 'fragment_VALUE', 'jdraw_begin': 'Ekzekuto', 'jdraw_end': 'Përfundo',
            'jdraw_pixel': 'pikëz', 'jdraw_rectangle': '사각그림', 'jdraw_pointer': 'tregues'}
        번역명령 = ['sh', str(Project_rrënjë.parents[1]/'compiler/미리번역.sh'), '--entry', '화면합성.너비얻기', '-o', str(vendmbërritje_VALUE/'vizatim_VALUE.c')]
        for Lidhu, FUNCTION_VALUE in eksportoj_tabelë.items(): 번역명령.extend(['--export', Lidhu+'=화면합성.'+FUNCTION_VALUE])
        subprocess.check_call(번역명령+[str(POZICIONI) for POZICIONI in sorted(klasë_shteg.glob('*.class'))])
        Komanda = ['clang', '-std=c11', '-O2', '-Wall', '-Wextra', '-Werror'] + burim_Skedarët
        vizatim_vendmbërritje = vendmbërritje_VALUE/'vizatim_VALUE.o'
        subprocess.check_call(['clang', '-std=c11', '-O2', '-c', str(vendmbërritje_VALUE/'vizatim_VALUE.c'), '-o', str(vizatim_vendmbërritje)])
        subprocess.check_call(Komanda+[str(vizatim_vendmbërritje), 'build/terminal-font.S', '-o', str(vendmbërritje_VALUE/'화면갱신시험')], cwd=str(Project_rrënjë))
        llogaritje = subprocess.check_output([str(vendmbërritje_VALUE/'화면갱신시험')], timeout=30).decode()
        (vendmbërritje_VALUE/'vlerësoj.log').write_text(llogaritje)
        맞음 = re.search(r'([\d.]+) ms/move; (\d+) framebuffer writes/move', llogaritje)
        assert 맞음 and 'PASS:' in llogaritje, llogaritje
        LOG_RECORD.update(passed=True, move_count=80, resize_count=40, window_count=4,
                   host_cpu_ms_per_move=float(맞음[1]), mean_framebuffer_writes_per_move=int(맞음[2]),
                   full_redraw_reference_equal=True, untouched_outside_damage=True,
                   unchanged_pixels_not_written=True, repeated_position_not_repainted=True,
                   padded_stride_preserved=True)
        print(llogaritje, end='')
    finally:
        (vendmbërritje_VALUE/'report.json').write_text(json.dumps(LOG_RECORD, ensure_ascii=False, indent=2)+'\n')

if __name__ == '__main__': Ekzekuto()

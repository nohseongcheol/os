#!/usr/bin/env python3
"""attwali_data kernel_VALUE 그리기 코드를 host Memorja_data 화면에 연결해 부분 갱신을 검증한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

pprojetta_għerq = Path(__file__).resolve().parents[1]

def serje():
    sors_Fajls = ['시험/화면갱신.c', 'kompjuter/화면그림.c', 'kompjuter/Terminal.c', 'kompjuter/widget.c']
    검증원문들 = sors_Fajls + ['sors/화면합성.java', 'sors/bord.java', '../../compiler/자바도구/기계어미리번역.java']
    destinazzjoni_VALUE = pprojetta_għerq/'build/verification/redraw'; destinazzjoni_VALUE.mkdir(parents=True, exist_ok=True)
    LOG_RECORD = {'passed': False, 'test_environment': 'host CPU, Java AOT framebuffer composition and native terminal/widgets with memory framebuffer',
          'kernel_sha256': hashlib.sha256((pprojetta_għerq/'build/kernel8.img').read_bytes()).hexdigest(),
          'source_sha256': {isem: hashlib.sha256((pprojetta_għerq/isem).read_bytes()).hexdigest() for isem in 검증원문들}}
    try:
        klassi_mogħdija = destinazzjoni_VALUE/'classes'; klassi_mogħdija.mkdir(exist_ok=True)
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(klassi_mogħdija),
            str(pprojetta_għerq/'sors/화면합성.java'), str(pprojetta_għerq/'sors/bord.java')])
        esporta_tabella = {'jdraw_prepare': 'Ħejji', 'jdraw_width': '너비얻기', 'jdraw_height': '높이얻기',
            'jdraw_count_low': '기록아래얻기', 'jdraw_count_high': '기록위얻기', 'jdraw_clip': 'klipp',
            'jdraw_clip_value': 'klipp_VALUE', 'jdraw_begin': 'serje', 'jdraw_end': 'Tmiem',
            'jdraw_pixel': 'pel', 'jdraw_rectangle': '사각그림', 'jdraw_pointer': 'pointer'}
        번역명령 = ['sh', str(pprojetta_għerq.parents[1]/'compiler/미리번역.sh'), '--entry', '화면합성.너비얻기', '-o', str(destinazzjoni_VALUE/'tpinġija_VALUE.c')]
        for AQBAD, FUNCTION_VALUE in esporta_tabella.items(): 번역명령.extend(['--export', AQBAD+'=화면합성.'+FUNCTION_VALUE])
        subprocess.check_call(번역명령+[str(mogħdija) for mogħdija in sorted(klassi_mogħdija.glob('*.class'))])
        kmand = ['clang', '-std=c11', '-O2', '-Wall', '-Wextra', '-Werror'] + sors_Fajls
        tpinġija_destinazzjoni = destinazzjoni_VALUE/'tpinġija_VALUE.o'
        subprocess.check_call(['clang', '-std=c11', '-O2', '-c', str(destinazzjoni_VALUE/'tpinġija_VALUE.c'), '-o', str(tpinġija_destinazzjoni)])
        subprocess.check_call(kmand+[str(tpinġija_destinazzjoni), 'build/terminal-font.S', '-o', str(destinazzjoni_VALUE/'화면갱신시험')], cwd=str(pprojetta_għerq))
        miżura = subprocess.check_output([str(destinazzjoni_VALUE/'화면갱신시험')], timeout=30).decode()
        (destinazzjoni_VALUE/'vvalida.log').write_text(miżura)
        맞음 = re.search(r'([\d.]+) ms/move; (\d+) framebuffer writes/move', miżura)
        assert 맞음 and 'PASS:' in miżura, miżura
        LOG_RECORD.update(passed=True, move_count=80, resize_count=40, window_count=4,
                   host_cpu_ms_per_move=float(맞음[1]), mean_framebuffer_writes_per_move=int(맞음[2]),
                   full_redraw_reference_equal=True, untouched_outside_damage=True,
                   unchanged_pixels_not_written=True, repeated_position_not_repainted=True,
                   padded_stride_preserved=True)
        print(miżura, end='')
    finally:
        (destinazzjoni_VALUE/'report.json').write_text(json.dumps(LOG_RECORD, ensure_ascii=False, indent=2)+'\n')

if __name__ == '__main__': serje()

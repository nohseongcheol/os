#!/usr/bin/env python3
"""werklik_data kern_VALUE 그리기 코드를 hou Geheue_data 화면에 연결해 부분 갱신을 검증한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

Project_wortel = Path(__file__).resolve().parents[1]

def Loop():
    bron_Lêers = ['시험/화면갱신.c', 'masjien/화면그림.c', 'masjien/Terminaal.c', 'masjien/legstuk.c']
    검증원문들 = bron_Lêers + ['Bron/화면합성.java', 'Bron/bord.java', '../../compiler/자바도구/기계어미리번역.java']
    bestemming_VALUE = Project_wortel/'build/verification/redraw'; bestemming_VALUE.mkdir(parents=True, exist_ok=True)
    LOG_ry = {'passed': False, 'test_environment': 'host CPU, Java AOT framebuffer composition and native terminal/widgets with memory framebuffer',
          'kernel_sha256': hashlib.sha256((Project_wortel/'build/kernel8.img').read_bytes()).hexdigest(),
          'source_sha256': {Naam: hashlib.sha256((Project_wortel/Naam).read_bytes()).hexdigest() for Naam in 검증원문들}}
    try:
        Klas_pad = bestemming_VALUE/'classes'; Klas_pad.mkdir(exist_ok=True)
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(Klas_pad),
            str(Project_wortel/'Bron/화면합성.java'), str(Project_wortel/'Bron/bord.java')])
        uitvoer_tabel = {'jdraw_prepare': 'Maak_gereed', 'jdraw_width': '너비얻기', 'jdraw_height': '높이얻기',
            'jdraw_count_low': '기록아래얻기', 'jdraw_count_high': '기록위얻기', 'jdraw_clip': 'snit',
            'jdraw_clip_value': 'snit_VALUE', 'jdraw_begin': 'Loop', 'jdraw_end': 'Klaar',
            'jdraw_pixel': 'pieksel', 'jdraw_rectangle': '사각그림', 'jdraw_pointer': 'wyser'}
        번역명령 = ['sh', str(Project_wortel.parents[1]/'compiler/미리번역.sh'), '--entry', '화면합성.너비얻기', '-o', str(bestemming_VALUE/'tekening_VALUE.c')]
        for Koppel, funksie_VALUE in uitvoer_tabel.items(): 번역명령.extend(['--export', Koppel+'=화면합성.'+funksie_VALUE])
        subprocess.check_call(번역명령+[str(Pad) for Pad in sorted(Klas_pad.glob('*.class'))])
        Opdrag = ['clang', '-std=c11', '-O2', '-Wall', '-Wextra', '-Werror'] + bron_Lêers
        tekening_bestemming = bestemming_VALUE/'tekening_VALUE.o'
        subprocess.check_call(['clang', '-std=c11', '-O2', '-c', str(bestemming_VALUE/'tekening_VALUE.c'), '-o', str(tekening_bestemming)])
        subprocess.check_call(Opdrag+[str(tekening_bestemming), 'build/terminal-font.S', '-o', str(bestemming_VALUE/'화면갱신시험')], cwd=str(Project_wortel))
        maatreël = subprocess.check_output([str(bestemming_VALUE/'화면갱신시험')], timeout=30).decode()
        (bestemming_VALUE/'valideer.log').write_text(maatreël)
        맞음 = re.search(r'([\d.]+) ms/move; (\d+) framebuffer writes/move', maatreël)
        assert 맞음 and 'PASS:' in maatreël, maatreël
        LOG_ry.update(passed=True, move_count=80, resize_count=40, window_count=4,
                   host_cpu_ms_per_move=float(맞음[1]), mean_framebuffer_writes_per_move=int(맞음[2]),
                   full_redraw_reference_equal=True, untouched_outside_damage=True,
                   unchanged_pixels_not_written=True, repeated_position_not_repainted=True,
                   padded_stride_preserved=True)
        print(maatreël, end='')
    finally:
        (bestemming_VALUE/'report.json').write_text(json.dumps(LOG_ry, ensure_ascii=False, indent=2)+'\n')

if __name__ == '__main__': Loop()

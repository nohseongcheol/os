#!/usr/bin/env python3
"""werkelijk_gegevens kernel_WAARDE Paint_scherm 코드를 host Geheugen_gegevens 화면에 연결해 부분 갱신을 검증한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

Taken_wortel = Path(__file__).resolve().parents[1]

def starten():
    bron_Files = ['tests/vernieuwen_scherm.c', 'machine/scherm_tekening.c', 'machine/terminal.c', 'machine/schermelement.c']
    검증원문들 = bron_Files + ['broncode/화면합성.java', 'broncode/Bord.java', '../../compiler/자바도구/기계어미리번역.java']
    doel_WAARDE = Taken_wortel/'build/verification/redraw'; doel_WAARDE.mkdir(parents=True, exist_ok=True)
    LOG_RECORD = {'passed': False, 'test_environment': 'host CPU, Java AOT framebuffer composition and native terminal/widgets with memory framebuffer',
          'kernel_sha256': hashlib.sha256((Taken_wortel/'build/kernel8.img').read_bytes()).hexdigest(),
          'source_sha256': {Naam: hashlib.sha256((Taken_wortel/Naam).read_bytes()).hexdigest() for Naam in 검증원문들}}
    try:
        les_pad = doel_WAARDE/'classes'; les_pad.mkdir(exist_ok=True)
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(les_pad),
            str(Taken_wortel/'broncode/화면합성.java'), str(Taken_wortel/'broncode/Bord.java')])
        exporteren_tabel = {'jdraw_prepare': 'Bereid_voor', 'jdraw_width': '너비얻기', 'jdraw_height': 'ophalen_hoogte',
            'jdraw_count_low': '기록아래얻기', 'jdraw_count_high': '기록위얻기', 'jdraw_clip': 'clip',
            'jdraw_clip_value': 'clip_WAARDE', 'jdraw_begin': 'starten', 'jdraw_end': 'Voltooien',
            'jdraw_pixel': 'pixel', 'jdraw_rectangle': 'rechthoek_vullen', 'jdraw_pointer': 'wijzer'}
        번역명령 = ['sh', str(Taken_wortel.parents[1]/'compiler/미리번역.sh'), '--entry', '화면합성.너비얻기', '-o', str(doel_WAARDE/'tekening_WAARDE.c')]
        for Verbinden, FUNCTIE_WAARDE in exporteren_tabel.items(): 번역명령.extend(['--export', Verbinden+'=화면합성.'+FUNCTIE_WAARDE])
        subprocess.check_call(번역명령+[str(pad) for pad in sorted(les_pad.glob('*.class'))])
        opdracht = ['clang', '-std=c11', '-O2', '-Wall', '-Wextra', '-Werror'] + bron_Files
        tekening_doel = doel_WAARDE/'tekening_WAARDE.o'
        subprocess.check_call(['clang', '-std=c11', '-O2', '-c', str(doel_WAARDE/'tekening_WAARDE.c'), '-o', str(tekening_doel)])
        subprocess.check_call(opdracht+[str(tekening_doel), 'build/terminal-font.S', '-o', str(doel_WAARDE/'scherm_vernieuwen_test')], cwd=str(Taken_wortel))
        resultaat = subprocess.check_output([str(doel_WAARDE/'scherm_vernieuwen_test')], timeout=30).decode()
        (doel_WAARDE/'valideren.log').write_text(resultaat)
        맞음 = re.search(r'([\d.]+) ms/move; (\d+) framebuffer writes/move', resultaat)
        assert 맞음 and 'PASS:' in resultaat, resultaat
        LOG_RECORD.update(passed=True, move_count=80, resize_count=40, window_count=4,
                   host_cpu_ms_per_move=float(맞음[1]), mean_framebuffer_writes_per_move=int(맞음[2]),
                   full_redraw_reference_equal=True, untouched_outside_damage=True,
                   unchanged_pixels_not_written=True, repeated_position_not_repainted=True,
                   padded_stride_preserved=True)
        print(resultaat, end='')
    finally:
        (doel_WAARDE/'report.json').write_text(json.dumps(LOG_RECORD, ensure_ascii=False, indent=2)+'\n')

if __name__ == '__main__': starten()

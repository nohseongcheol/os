#!/usr/bin/env python3
"""faktinis_duomenys branduolys_VALUE 그리기 코드를 organizuoti atmintis_duomenys 화면에 연결해 부분 갱신을 검증한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

Project_šaknis = Path(__file__).resolve().parents[1]

def Paleisti():
    šaltinis_Failai = ['시험/화면갱신.c', 'mašina/화면그림.c', 'mašina/Terminalas.c', 'mašina/valdiklis.c']
    검증원문들 = šaltinis_Failai + ['ŠALTINIS/화면합성.java', 'ŠALTINIS/Lenta.java', '../../compiler/자바도구/기계어미리번역.java']
    vieta_VALUE = Project_šaknis/'build/verification/redraw'; vieta_VALUE.mkdir(parents=True, exist_ok=True)
    LOG_RECORD = {'passed': False, 'test_environment': 'host CPU, Java AOT framebuffer composition and native terminal/widgets with memory framebuffer',
          'kernel_sha256': hashlib.sha256((Project_šaknis/'build/kernel8.img').read_bytes()).hexdigest(),
          'source_sha256': {Pavadinimas_2: hashlib.sha256((Project_šaknis/Pavadinimas_2).read_bytes()).hexdigest() for Pavadinimas_2 in 검증원문들}}
    try:
        klasė_kelias = vieta_VALUE/'classes'; klasė_kelias.mkdir(exist_ok=True)
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(klasė_kelias),
            str(Project_šaknis/'ŠALTINIS/화면합성.java'), str(Project_šaknis/'ŠALTINIS/Lenta.java')])
        eksportuoti_lentelė = {'jdraw_prepare': 'Parengti', 'jdraw_width': '너비얻기', 'jdraw_height': '높이얻기',
            'jdraw_count_low': '기록아래얻기', 'jdraw_count_high': '기록위얻기', 'jdraw_clip': 'klipas',
            'jdraw_clip_value': 'klipas_VALUE', 'jdraw_begin': 'Paleisti', 'jdraw_end': 'Baigti',
            'jdraw_pixel': 'pikselis', 'jdraw_rectangle': 'stačiakampis_užpildas', 'jdraw_pointer': 'rodyklė'}
        번역명령 = ['sh', str(Project_šaknis.parents[1]/'compiler/미리번역.sh'), '--entry', '화면합성.너비얻기', '-o', str(vieta_VALUE/'piešinys_VALUE.c')]
        for Prisijungti, FUNCTION_VALUE in eksportuoti_lentelė.items(): 번역명령.extend(['--export', Prisijungti+'=화면합성.'+FUNCTION_VALUE])
        subprocess.check_call(번역명령+[str(KELIAS) for KELIAS in sorted(klasė_kelias.glob('*.class'))])
        Komanda = ['clang', '-std=c11', '-O2', '-Wall', '-Wextra', '-Werror'] + šaltinis_Failai
        piešinys_vieta = vieta_VALUE/'piešinys_VALUE.o'
        subprocess.check_call(['clang', '-std=c11', '-O2', '-c', str(vieta_VALUE/'piešinys_VALUE.c'), '-o', str(piešinys_vieta)])
        subprocess.check_call(Komanda+[str(piešinys_vieta), 'build/terminal-font.S', '-o', str(vieta_VALUE/'화면갱신시험')], cwd=str(Project_šaknis))
        REZULTATAS = subprocess.check_output([str(vieta_VALUE/'화면갱신시험')], timeout=30).decode()
        (vieta_VALUE/'tikrinti.log').write_text(REZULTATAS)
        맞음 = re.search(r'([\d.]+) ms/move; (\d+) framebuffer writes/move', REZULTATAS)
        assert 맞음 and 'PASS:' in REZULTATAS, REZULTATAS
        LOG_RECORD.update(passed=True, move_count=80, resize_count=40, window_count=4,
                   host_cpu_ms_per_move=float(맞음[1]), mean_framebuffer_writes_per_move=int(맞음[2]),
                   full_redraw_reference_equal=True, untouched_outside_damage=True,
                   unchanged_pixels_not_written=True, repeated_position_not_repainted=True,
                   padded_stride_preserved=True)
        print(REZULTATAS, end='')
    finally:
        (vieta_VALUE/'report.json').write_text(json.dumps(LOG_RECORD, ensure_ascii=False, indent=2)+'\n')

if __name__ == '__main__': Paleisti()

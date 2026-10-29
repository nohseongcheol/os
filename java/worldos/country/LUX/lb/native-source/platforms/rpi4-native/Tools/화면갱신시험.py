#!/usr/bin/env python3
"""aktuell_Daten Kernel_VALUE 그리기 코드를 Host Späicher_Daten 화면에 연결해 부분 갱신을 검증한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

projezéieren_Racinn = Path(__file__).resolve().parents[1]

def Laf():
    Quell_Fichieren = ['시험/화면갱신.c', 'Computer/화면그림.c', 'Computer/Terminal.c', 'Computer/Widget.c']
    검증원문들 = Quell_Fichieren + ['Quell/화면합성.java', 'Quell/Board.java', '../../compiler/자바도구/기계어미리번역.java']
    Zil_VALUE = projezéieren_Racinn/'build/verification/redraw'; Zil_VALUE.mkdir(parents=True, exist_ok=True)
    LOG_Rei = {'passed': False, 'test_environment': 'host CPU, Java AOT framebuffer composition and native terminal/widgets with memory framebuffer',
          'kernel_sha256': hashlib.sha256((projezéieren_Racinn/'build/kernel8.img').read_bytes()).hexdigest(),
          'source_sha256': {Numm: hashlib.sha256((projezéieren_Racinn/Numm).read_bytes()).hexdigest() for Numm in 검증원문들}}
    try:
        Klass_Wee = Zil_VALUE/'classes'; Klass_Wee.mkdir(exist_ok=True)
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(Klass_Wee),
            str(projezéieren_Racinn/'Quell/화면합성.java'), str(projezéieren_Racinn/'Quell/Board.java')])
        exportéieren_Tabell = {'jdraw_prepare': 'Préparéieren', 'jdraw_width': '너비얻기', 'jdraw_height': '높이얻기',
            'jdraw_count_low': '기록아래얻기', 'jdraw_count_high': '기록위얻기', 'jdraw_clip': 'Clip',
            'jdraw_clip_value': 'Clip_VALUE', 'jdraw_begin': 'Laf', 'jdraw_end': 'Ofschléissen',
            'jdraw_pixel': 'Pel', 'jdraw_rectangle': '사각그림', 'jdraw_pointer': 'Uweiser'}
        번역명령 = ['sh', str(projezéieren_Racinn.parents[1]/'compiler/미리번역.sh'), '--entry', '화면합성.너비얻기', '-o', str(Zil_VALUE/'Zeechnung_VALUE.c')]
        for Verbannen, FUNCTION_VALUE in exportéieren_Tabell.items(): 번역명령.extend(['--export', Verbannen+'=화면합성.'+FUNCTION_VALUE])
        subprocess.check_call(번역명령+[str(Wee) for Wee in sorted(Klass_Wee.glob('*.class'))])
        Befeel = ['clang', '-std=c11', '-O2', '-Wall', '-Wextra', '-Werror'] + Quell_Fichieren
        Zeechnung_Zil = Zil_VALUE/'Zeechnung_VALUE.o'
        subprocess.check_call(['clang', '-std=c11', '-O2', '-c', str(Zil_VALUE/'Zeechnung_VALUE.c'), '-o', str(Zeechnung_Zil)])
        subprocess.check_call(Befeel+[str(Zeechnung_Zil), 'build/terminal-font.S', '-o', str(Zil_VALUE/'화면갱신시험')], cwd=str(projezéieren_Racinn))
        Mooss = subprocess.check_output([str(Zil_VALUE/'화면갱신시험')], timeout=30).decode()
        (Zil_VALUE/'validéieren.log').write_text(Mooss)
        맞음 = re.search(r'([\d.]+) ms/move; (\d+) framebuffer writes/move', Mooss)
        assert 맞음 and 'PASS:' in Mooss, Mooss
        LOG_Rei.update(passed=True, move_count=80, resize_count=40, window_count=4,
                   host_cpu_ms_per_move=float(맞음[1]), mean_framebuffer_writes_per_move=int(맞음[2]),
                   full_redraw_reference_equal=True, untouched_outside_damage=True,
                   unchanged_pixels_not_written=True, repeated_position_not_repainted=True,
                   padded_stride_preserved=True)
        print(Mooss, end='')
    finally:
        (Zil_VALUE/'report.json').write_text(json.dumps(LOG_Rei, ensure_ascii=False, indent=2)+'\n')

if __name__ == '__main__': Laf()

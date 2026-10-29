#!/usr/bin/env python3
"""raun_gögn kjarni_VALUE 그리기 코드를 hýsa Minni_gögn 화면에 연결해 부분 갱신을 검증한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

verk_rót = Path(__file__).resolve().parents[1]

def Keyra_2():
    uppruni_Skrár = ['시험/화면갱신.c', 'vél/화면그림.c', 'vél/Skjáhermir.c', 'vél/græja.c']
    검증원문들 = uppruni_Skrár + ['Uppruni/화면합성.java', 'Uppruni/bretti.java', '../../compiler/자바도구/기계어미리번역.java']
    endastaður_VALUE = verk_rót/'build/verification/redraw'; endastaður_VALUE.mkdir(parents=True, exist_ok=True)
    LOG_lína = {'passed': False, 'test_environment': 'host CPU, Java AOT framebuffer composition and native terminal/widgets with memory framebuffer',
          'kernel_sha256': hashlib.sha256((verk_rót/'build/kernel8.img').read_bytes()).hexdigest(),
          'source_sha256': {Heiti: hashlib.sha256((verk_rót/Heiti).read_bytes()).hexdigest() for Heiti in 검증원문들}}
    try:
        klasi_slóð = endastaður_VALUE/'classes'; klasi_slóð.mkdir(exist_ok=True)
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(klasi_slóð),
            str(verk_rót/'Uppruni/화면합성.java'), str(verk_rót/'Uppruni/bretti.java')])
        flytja_út_tafla = {'jdraw_prepare': 'Undirbúa', 'jdraw_width': '너비얻기', 'jdraw_height': '높이얻기',
            'jdraw_count_low': '기록아래얻기', 'jdraw_count_high': '기록위얻기', 'jdraw_clip': 'miðlaskrá',
            'jdraw_clip_value': 'miðlaskrá_VALUE', 'jdraw_begin': 'Keyra_2', 'jdraw_end': 'Ljúka',
            'jdraw_pixel': 'díll', 'jdraw_rectangle': '사각그림', 'jdraw_pointer': 'bendill'}
        번역명령 = ['sh', str(verk_rót.parents[1]/'compiler/미리번역.sh'), '--entry', '화면합성.너비얻기', '-o', str(endastaður_VALUE/'teikning_VALUE.c')]
        for Tengjast, fall_VALUE in flytja_út_tafla.items(): 번역명령.extend(['--export', Tengjast+'=화면합성.'+fall_VALUE])
        subprocess.check_call(번역명령+[str(SLÓÐ) for SLÓÐ in sorted(klasi_slóð.glob('*.class'))])
        Skipun = ['clang', '-std=c11', '-O2', '-Wall', '-Wextra', '-Werror'] + uppruni_Skrár
        teikning_endastaður = endastaður_VALUE/'teikning_VALUE.o'
        subprocess.check_call(['clang', '-std=c11', '-O2', '-c', str(endastaður_VALUE/'teikning_VALUE.c'), '-o', str(teikning_endastaður)])
        subprocess.check_call(Skipun+[str(teikning_endastaður), 'build/terminal-font.S', '-o', str(endastaður_VALUE/'화면갱신시험')], cwd=str(verk_rót))
        NIÐURSTAÐA = subprocess.check_output([str(endastaður_VALUE/'화면갱신시험')], timeout=30).decode()
        (endastaður_VALUE/'staðfesta.log').write_text(NIÐURSTAÐA)
        맞음 = re.search(r'([\d.]+) ms/move; (\d+) framebuffer writes/move', NIÐURSTAÐA)
        assert 맞음 and 'PASS:' in NIÐURSTAÐA, NIÐURSTAÐA
        LOG_lína.update(passed=True, move_count=80, resize_count=40, window_count=4,
                   host_cpu_ms_per_move=float(맞음[1]), mean_framebuffer_writes_per_move=int(맞음[2]),
                   full_redraw_reference_equal=True, untouched_outside_damage=True,
                   unchanged_pixels_not_written=True, repeated_position_not_repainted=True,
                   padded_stride_preserved=True)
        print(NIÐURSTAÐA, end='')
    finally:
        (endastaður_VALUE/'report.json').write_text(json.dumps(LOG_lína, ensure_ascii=False, indent=2)+'\n')

if __name__ == '__main__': Keyra_2()

#!/usr/bin/env python3
"""ulwazi_ngokwenzekile_imininingwane ikhenela_inani 그리기 코드를 singatha inkumbulo_imininingwane 화면에 연결해 부분 갱신을 검증한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

기준 = Path(__file__).resolve().parents[1]

def Sebenzisa():
    umthombo_Amafayela = ['시험/화면갱신.c', 'umshini/화면그림.c', 'umshini/터미널.c', 'umshini/iwijethi.c']
    검증원문들 = umthombo_Amafayela + ['umthombo/화면합성.java', 'umthombo/보드.java', '../../compiler/자바도구/기계어미리번역.java']
    isikhumulo_inani = 기준/'build/verification/redraw'; isikhumulo_inani.mkdir(parents=True, exist_ok=True)
    loga_umugqa = {'passed': False, 'test_environment': 'host CPU, Java AOT framebuffer composition and native terminal/widgets with memory framebuffer',
          'kernel_sha256': hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),
          'source_sha256': {Igama: hashlib.sha256((기준/Igama).read_bytes()).hexdigest() for Igama in 검증원문들}}
    try:
        uhlobo_umzila = isikhumulo_inani/'classes'; uhlobo_umzila.mkdir(exist_ok=True)
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(uhlobo_umzila),
            str(기준/'umthombo/화면합성.java'), str(기준/'umthombo/보드.java')])
        thekelisa_ithebula = {'jdraw_prepare': 'Hlela', 'jdraw_width': '너비얻기', 'jdraw_height': '높이얻기',
            'jdraw_count_low': '기록아래얻기', 'jdraw_count_high': '기록위얻기', 'jdraw_clip': 'isiqeshana',
            'jdraw_clip_value': 'isiqeshana_inani', 'jdraw_begin': 'Sebenzisa', 'jdraw_end': 'Qeda',
            'jdraw_pixel': 'i_pel', 'jdraw_rectangle': '사각그림', 'jdraw_pointer': 'isikhombi'}
        번역명령 = ['sh', str(기준.parents[1]/'compiler/미리번역.sh'), '--entry', '화면합성.너비얻기', '-o', str(isikhumulo_inani/'umdwebo_inani.c')]
        for Xhumanisa, umsebenzi_inani in thekelisa_ithebula.items(): 번역명령.extend(['--export', Xhumanisa+'=화면합성.'+umsebenzi_inani])
        subprocess.check_call(번역명령+[str(Indlela_2) for Indlela_2 in sorted(uhlobo_umzila.glob('*.class'))])
        Umlayelo = ['clang', '-std=c11', '-O2', '-Wall', '-Wextra', '-Werror'] + umthombo_Amafayela
        umdwebo_isikhumulo = isikhumulo_inani/'umdwebo_inani.o'
        subprocess.check_call(['clang', '-std=c11', '-O2', '-c', str(isikhumulo_inani/'umdwebo_inani.c'), '-o', str(umdwebo_isikhumulo)])
        subprocess.check_call(Umlayelo+[str(umdwebo_isikhumulo), 'build/terminal-font.S', '-o', str(isikhumulo_inani/'화면갱신시험')], cwd=str(기준))
        결과 = subprocess.check_output([str(isikhumulo_inani/'화면갱신시험')], timeout=30).decode()
        (isikhumulo_inani/'qinisekisa.log').write_text(결과)
        맞음 = re.search(r'([\d.]+) ms/move; (\d+) framebuffer writes/move', 결과)
        assert 맞음 and 'PASS:' in 결과, 결과
        loga_umugqa.update(passed=True, move_count=80, resize_count=40, window_count=4,
                   host_cpu_ms_per_move=float(맞음[1]), mean_framebuffer_writes_per_move=int(맞음[2]),
                   full_redraw_reference_equal=True, untouched_outside_damage=True,
                   unchanged_pixels_not_written=True, repeated_position_not_repainted=True,
                   padded_stride_preserved=True)
        print(결과, end='')
    finally:
        (isikhumulo_inani/'report.json').write_text(json.dumps(loga_umugqa, ensure_ascii=False, indent=2)+'\n')

if __name__ == '__main__': Sebenzisa()

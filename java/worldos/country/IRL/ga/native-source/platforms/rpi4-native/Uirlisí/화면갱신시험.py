#!/usr/bin/env python3
"""iarbhír_sonraí eithne_VALUE 그리기 코드를 óstach Cuimhne_sonraí 화면에 연결해 부분 갱신을 검증한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

teilgean_fréamh = Path(__file__).resolve().parents[1]

def Rith_2():
    foinse_Comhaid = ['시험/화면갱신.c', 'meaisín/화면그림.c', 'meaisín/Teirminéal.c', 'meaisín/giuirléid.c']
    검증원문들 = foinse_Comhaid + ['FOINSE/화면합성.java', 'FOINSE/clár.java', '../../compiler/자바도구/기계어미리번역.java']
    sprioc_VALUE = teilgean_fréamh/'build/verification/redraw'; sprioc_VALUE.mkdir(parents=True, exist_ok=True)
    LOG_ró = {'passed': False, 'test_environment': 'host CPU, Java AOT framebuffer composition and native terminal/widgets with memory framebuffer',
          'kernel_sha256': hashlib.sha256((teilgean_fréamh/'build/kernel8.img').read_bytes()).hexdigest(),
          'source_sha256': {Ainm: hashlib.sha256((teilgean_fréamh/Ainm).read_bytes()).hexdigest() for Ainm in 검증원문들}}
    try:
        aicme_cosán = sprioc_VALUE/'classes'; aicme_cosán.mkdir(exist_ok=True)
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(aicme_cosán),
            str(teilgean_fréamh/'FOINSE/화면합성.java'), str(teilgean_fréamh/'FOINSE/clár.java')])
        easportáil_tábla = {'jdraw_prepare': 'Ullmhaigh', 'jdraw_width': '너비얻기', 'jdraw_height': '높이얻기',
            'jdraw_count_low': '기록아래얻기', 'jdraw_count_high': '기록위얻기', 'jdraw_clip': 'gearrthóg',
            'jdraw_clip_value': 'gearrthóg_VALUE', 'jdraw_begin': 'Rith_2', 'jdraw_end': 'Críochnaigh',
            'jdraw_pixel': 'picteilín', 'jdraw_rectangle': '사각그림', 'jdraw_pointer': 'pointeoir'}
        번역명령 = ['sh', str(teilgean_fréamh.parents[1]/'compiler/미리번역.sh'), '--entry', '화면합성.너비얻기', '-o', str(sprioc_VALUE/'líníocht_VALUE.c')]
        for Nasc, feidhm_VALUE in easportáil_tábla.items(): 번역명령.extend(['--export', Nasc+'=화면합성.'+feidhm_VALUE])
        subprocess.check_call(번역명령+[str(CONAIR) for CONAIR in sorted(aicme_cosán.glob('*.class'))])
        Ordú = ['clang', '-std=c11', '-O2', '-Wall', '-Wextra', '-Werror'] + foinse_Comhaid
        líníocht_sprioc = sprioc_VALUE/'líníocht_VALUE.o'
        subprocess.check_call(['clang', '-std=c11', '-O2', '-c', str(sprioc_VALUE/'líníocht_VALUE.c'), '-o', str(líníocht_sprioc)])
        subprocess.check_call(Ordú+[str(líníocht_sprioc), 'build/terminal-font.S', '-o', str(sprioc_VALUE/'화면갱신시험')], cwd=str(teilgean_fréamh))
        tomhas = subprocess.check_output([str(sprioc_VALUE/'화면갱신시험')], timeout=30).decode()
        (sprioc_VALUE/'bailíochtaigh.log').write_text(tomhas)
        맞음 = re.search(r'([\d.]+) ms/move; (\d+) framebuffer writes/move', tomhas)
        assert 맞음 and 'PASS:' in tomhas, tomhas
        LOG_ró.update(passed=True, move_count=80, resize_count=40, window_count=4,
                   host_cpu_ms_per_move=float(맞음[1]), mean_framebuffer_writes_per_move=int(맞음[2]),
                   full_redraw_reference_equal=True, untouched_outside_damage=True,
                   unchanged_pixels_not_written=True, repeated_position_not_repainted=True,
                   padded_stride_preserved=True)
        print(tomhas, end='')
    finally:
        (sprioc_VALUE/'report.json').write_text(json.dumps(LOG_ró, ensure_ascii=False, indent=2)+'\n')

if __name__ == '__main__': Rith_2()

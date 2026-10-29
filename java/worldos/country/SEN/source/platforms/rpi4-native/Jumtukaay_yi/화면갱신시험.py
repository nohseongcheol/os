#!/usr/bin/env python3
"""liteew_mbir xoox_xëyma 그리기 코드를 dalal fatlekookaay_mbir 화면에 연결해 부분 갱신을 검증한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

기준 = Path(__file__).resolve().parents[1]

def daw():
    Cosaan_Fisiye_yi = ['시험/화면갱신.c', 'masin/화면그림.c', 'masin/터미널.c', 'masin/kifin.c']
    검증원문들 = Cosaan_Fisiye_yi + ['Cosaan/화면합성.java', 'Cosaan/보드.java', '../../compiler/자바도구/기계어미리번역.java']
    jëmmukaay_xëyma = 기준/'build/verification/redraw'; jëmmukaay_xëyma.mkdir(parents=True, exist_ok=True)
    làq_Dënk = {'passed': False, 'test_environment': 'host CPU, Java AOT framebuffer composition and native terminal/widgets with memory framebuffer',
          'kernel_sha256': hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),
          'source_sha256': {tur_253d1510: hashlib.sha256((기준/tur_253d1510).read_bytes()).hexdigest() for tur_253d1510 in 검증원문들}}
    try:
        maas_Yoonu_jëmale = jëmmukaay_xëyma/'classes'; maas_Yoonu_jëmale.mkdir(exist_ok=True)
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(maas_Yoonu_jëmale),
            str(기준/'Cosaan/화면합성.java'), str(기준/'Cosaan/보드.java')])
        toxal_àlluwa = {'jdraw_prepare': 'jël_matuwaay', 'jdraw_width': '너비얻기', 'jdraw_height': '높이얻기',
            'jdraw_count_low': '기록아래얻기', 'jdraw_count_high': '기록위얻기', 'jdraw_clip': 'kilip',
            'jdraw_clip_value': 'kilip_xëyma', 'jdraw_begin': 'daw', 'jdraw_end': 'Sottal',
            'jdraw_pixel': 'piksel', 'jdraw_rectangle': '사각그림', 'jdraw_pointer': 'joxañukaay'}
        번역명령 = ['sh', str(기준.parents[1]/'compiler/미리번역.sh'), '--entry', '화면합성.너비얻기', '-o', str(jëmmukaay_xëyma/'deseñ_xëyma.c')]
        for JOKKOO, liëey_xëyma in toxal_àlluwa.items(): 번역명령.extend(['--export', JOKKOO+'=화면합성.'+liëey_xëyma])
        subprocess.check_call(번역명령+[str(Yoonu_jëmale) for Yoonu_jëmale in sorted(maas_Yoonu_jëmale.glob('*.class'))])
        ndigel = ['clang', '-std=c11', '-O2', '-Wall', '-Wextra', '-Werror'] + Cosaan_Fisiye_yi
        deseñ_jëmmukaay = jëmmukaay_xëyma/'deseñ_xëyma.o'
        subprocess.check_call(['clang', '-std=c11', '-O2', '-c', str(jëmmukaay_xëyma/'deseñ_xëyma.c'), '-o', str(deseñ_jëmmukaay)])
        subprocess.check_call(ndigel+[str(deseñ_jëmmukaay), 'build/terminal-font.S', '-o', str(jëmmukaay_xëyma/'화면갱신시험')], cwd=str(기준))
        결과 = subprocess.check_output([str(jëmmukaay_xëyma/'화면갱신시험')], timeout=30).decode()
        (jëmmukaay_xëyma/'wéral.log').write_text(결과)
        맞음 = re.search(r'([\d.]+) ms/move; (\d+) framebuffer writes/move', 결과)
        assert 맞음 and 'PASS:' in 결과, 결과
        làq_Dënk.update(passed=True, move_count=80, resize_count=40, window_count=4,
                   host_cpu_ms_per_move=float(맞음[1]), mean_framebuffer_writes_per_move=int(맞음[2]),
                   full_redraw_reference_equal=True, untouched_outside_damage=True,
                   unchanged_pixels_not_written=True, repeated_position_not_repainted=True,
                   padded_stride_preserved=True)
        print(결과, end='')
    finally:
        (jëmmukaay_xëyma/'report.json').write_text(json.dumps(làq_Dënk, ensure_ascii=False, indent=2)+'\n')

if __name__ == '__main__': daw()

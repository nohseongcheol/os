#!/usr/bin/env python3
"""kgonthe_data khenele_boleng 그리기 코드를 go_nea_ditirelo memori_data 화면에 연결해 부분 갱신을 검증한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

기준 = Path(__file__).resolve().parents[1]

def Diriša():
    mohlodi_Difaele = ['시험/화면갱신.c', 'motšhene/화면그림.c', 'motšhene/터미널.c', 'motšhene/witšete.c']
    검증원문들 = mohlodi_Difaele + ['mohlodi/화면합성.java', 'mohlodi/보드.java', '../../compiler/자바도구/기계어미리번역.java']
    boyo_boleng = 기준/'build/verification/redraw'; boyo_boleng.mkdir(parents=True, exist_ok=True)
    pego_rei = {'passed': False, 'test_environment': 'host CPU, Java AOT framebuffer composition and native terminal/widgets with memory framebuffer',
          'kernel_sha256': hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),
          'source_sha256': {Leina: hashlib.sha256((기준/Leina).read_bytes()).hexdigest() for Leina in 검증원문들}}
    try:
        legoro_tsela = boyo_boleng/'classes'; legoro_tsela.mkdir(exist_ok=True)
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(legoro_tsela),
            str(기준/'mohlodi/화면합성.java'), str(기준/'mohlodi/보드.java')])
        Iša_tafola = {'jdraw_prepare': 'Lokišetša', 'jdraw_width': '너비얻기', 'jdraw_height': '높이얻기',
            'jdraw_count_low': '기록아래얻기', 'jdraw_count_high': '기록위얻기', 'jdraw_clip': 'setsopolwa',
            'jdraw_clip_value': 'setsopolwa_boleng', 'jdraw_begin': 'Diriša', 'jdraw_end': 'Fetša',
            'jdraw_pixel': 'phele', 'jdraw_rectangle': '사각그림', 'jdraw_pointer': 'sešupi'}
        번역명령 = ['sh', str(기준.parents[1]/'compiler/미리번역.sh'), '--entry', '화면합성.너비얻기', '-o', str(boyo_boleng/'sethalwa_boleng.c')]
        for Ikgokaganye, TIRO_boleng in Iša_tafola.items(): 번역명령.extend(['--export', Ikgokaganye+'=화면합성.'+TIRO_boleng])
        subprocess.check_call(번역명령+[str(Tsejana) for Tsejana in sorted(legoro_tsela.glob('*.class'))])
        Taelo = ['clang', '-std=c11', '-O2', '-Wall', '-Wextra', '-Werror'] + mohlodi_Difaele
        sethalwa_boyo = boyo_boleng/'sethalwa_boleng.o'
        subprocess.check_call(['clang', '-std=c11', '-O2', '-c', str(boyo_boleng/'sethalwa_boleng.c'), '-o', str(sethalwa_boyo)])
        subprocess.check_call(Taelo+[str(sethalwa_boyo), 'build/terminal-font.S', '-o', str(boyo_boleng/'화면갱신시험')], cwd=str(기준))
        결과 = subprocess.check_output([str(boyo_boleng/'화면갱신시험')], timeout=30).decode()
        (boyo_boleng/'kgonthiša_5fb2b747.log').write_text(결과)
        맞음 = re.search(r'([\d.]+) ms/move; (\d+) framebuffer writes/move', 결과)
        assert 맞음 and 'PASS:' in 결과, 결과
        pego_rei.update(passed=True, move_count=80, resize_count=40, window_count=4,
                   host_cpu_ms_per_move=float(맞음[1]), mean_framebuffer_writes_per_move=int(맞음[2]),
                   full_redraw_reference_equal=True, untouched_outside_damage=True,
                   unchanged_pixels_not_written=True, repeated_position_not_repainted=True,
                   padded_stride_preserved=True)
        print(결과, end='')
    finally:
        (boyo_boleng/'report.json').write_text(json.dumps(pego_rei, ensure_ascii=False, indent=2)+'\n')

if __name__ == '__main__': Diriša()

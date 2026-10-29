#!/usr/bin/env python3
"""tota_tshedimosetso Khenele_Boleng 그리기 코드를 pinagare memori_tshedimosetso 화면에 연결해 부분 갱신을 검증한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

기준 = Path(__file__).resolve().parents[1]

def dirisa():
    Motswedi_Difaele = ['시험/화면갱신.c', 'motšhine/화면그림.c', 'motšhine/터미널.c', 'motšhine/wijete.c']
    검증원문들 = Motswedi_Difaele + ['Motswedi/화면합성.java', 'Motswedi/보드.java', '../../compiler/자바도구/기계어미리번역.java']
    bogorogelo_Boleng = 기준/'build/verification/redraw'; bogorogelo_Boleng.mkdir(parents=True, exist_ok=True)
    rekota_mola = {'passed': False, 'test_environment': 'host CPU, Java AOT framebuffer composition and native terminal/widgets with memory framebuffer',
          'kernel_sha256': hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),
          'source_sha256': {leina: hashlib.sha256((기준/leina).read_bytes()).hexdigest() for leina in 검증원문들}}
    try:
        mofuta_tsela = bogorogelo_Boleng/'classes'; mofuta_tsela.mkdir(exist_ok=True)
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(mofuta_tsela),
            str(기준/'Motswedi/화면합성.java'), str(기준/'Motswedi/보드.java')])
        romelantle_lenaneothalo = {'jdraw_prepare': 'Baakanya', 'jdraw_width': '너비얻기', 'jdraw_height': '높이얻기',
            'jdraw_count_low': '기록아래얻기', 'jdraw_count_high': '기록위얻기', 'jdraw_clip': 'faelekhutshwe_ya_media',
            'jdraw_clip_value': 'faelekhutshwe_ya_media_Boleng', 'jdraw_begin': 'dirisa', 'jdraw_end': 'Fetsa',
            'jdraw_pixel': 'phele', 'jdraw_rectangle': '사각그림', 'jdraw_pointer': 'sesupi'}
        번역명령 = ['sh', str(기준.parents[1]/'compiler/미리번역.sh'), '--entry', '화면합성.너비얻기', '-o', str(bogorogelo_Boleng/'sethalo_Boleng.c')]
        for Golaganya, TIRISO_Boleng in romelantle_lenaneothalo.items(): 번역명령.extend(['--export', Golaganya+'=화면합성.'+TIRISO_Boleng])
        subprocess.check_call(번역명령+[str(tsela) for tsela in sorted(mofuta_tsela.glob('*.class'))])
        Taelo = ['clang', '-std=c11', '-O2', '-Wall', '-Wextra', '-Werror'] + Motswedi_Difaele
        sethalo_bogorogelo = bogorogelo_Boleng/'sethalo_Boleng.o'
        subprocess.check_call(['clang', '-std=c11', '-O2', '-c', str(bogorogelo_Boleng/'sethalo_Boleng.c'), '-o', str(sethalo_bogorogelo)])
        subprocess.check_call(Taelo+[str(sethalo_bogorogelo), 'build/terminal-font.S', '-o', str(bogorogelo_Boleng/'화면갱신시험')], cwd=str(기준))
        결과 = subprocess.check_output([str(bogorogelo_Boleng/'화면갱신시험')], timeout=30).decode()
        (bogorogelo_Boleng/'netefatsa_5fb2b747.log').write_text(결과)
        맞음 = re.search(r'([\d.]+) ms/move; (\d+) framebuffer writes/move', 결과)
        assert 맞음 and 'PASS:' in 결과, 결과
        rekota_mola.update(passed=True, move_count=80, resize_count=40, window_count=4,
                   host_cpu_ms_per_move=float(맞음[1]), mean_framebuffer_writes_per_move=int(맞음[2]),
                   full_redraw_reference_equal=True, untouched_outside_damage=True,
                   unchanged_pixels_not_written=True, repeated_position_not_repainted=True,
                   padded_stride_preserved=True)
        print(결과, end='')
    finally:
        (bogorogelo_Boleng/'report.json').write_text(json.dumps(rekota_mola, ensure_ascii=False, indent=2)+'\n')

if __name__ == '__main__': dirisa()

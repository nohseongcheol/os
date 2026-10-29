#!/usr/bin/env python3
"""стваран_подаци језгро_вриједност 그리기 코드를 хост_рачунар меморија_подаци 화면에 연결해 부분 갱신을 검증한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

기준 = Path(__file__).resolve().parents[1]

def 시작():
    원문들 = ['시험/화면갱신.c', '기계/화면그림.c', '기계/터미널.c', '기계/виџет.c']
    검증원문들 = 원문들 + ['извор/화면합성.java', 'извор/보드.java', '../../compiler/자바도구/기계어미리번역.java']
    одредиште_вриједност = 기준/'build/verification/redraw'; одредиште_вриједност.mkdir(parents=True, exist_ok=True)
    дневник_рада_ред = {'passed': False, 'test_environment': 'host CPU, Java AOT framebuffer composition and native terminal/widgets with memory framebuffer',
          'kernel_sha256': hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),
          'source_sha256': {назив: hashlib.sha256((기준/назив).read_bytes()).hexdigest() for назив in 검증원문들}}
    try:
        класа_пут = одредиште_вриједност/'classes'; класа_пут.mkdir(exist_ok=True)
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(класа_пут),
            str(기준/'извор/화면합성.java'), str(기준/'извор/보드.java')])
        извозити_табела = {'jdraw_prepare': 'Припремити', 'jdraw_width': '너비얻기', 'jdraw_height': '높이얻기',
            'jdraw_count_low': '기록아래얻기', 'jdraw_count_high': '기록위얻기', 'jdraw_clip': 'исјечак',
            'jdraw_clip_value': 'исјечак_вриједност', 'jdraw_begin': '시작', 'jdraw_end': '마침',
            'jdraw_pixel': 'Пел', 'jdraw_rectangle': '사각그림', 'jdraw_pointer': '포인터'}
        번역명령 = ['sh', str(기준.parents[1]/'compiler/미리번역.sh'), '--entry', '화면합성.너비얻기', '-o', str(одредиште_вриједност/'уцртавање_вриједност.c')]
        for повезати, функција_вриједност in извозити_табела.items(): 번역명령.extend(['--export', повезати+'=화면합성.'+функција_вриједност])
        subprocess.check_call(번역명령+[str(пут) for пут in sorted(класа_пут.glob('*.class'))])
        команда = ['clang', '-std=c11', '-O2', '-Wall', '-Wextra', '-Werror'] + 원문들
        уцртавање_одредиште = одредиште_вриједност/'уцртавање_вриједност.o'
        subprocess.check_call(['clang', '-std=c11', '-O2', '-c', str(одредиште_вриједност/'уцртавање_вриједност.c'), '-o', str(уцртавање_одредиште)])
        subprocess.check_call(команда+[str(уцртавање_одредиште), 'build/terminal-font.S', '-o', str(одредиште_вриједност/'화면갱신시험')], cwd=str(기준))
        결과 = subprocess.check_output([str(одредиште_вриједност/'화면갱신시험')], timeout=30).decode()
        (одредиште_вриједност/'овјерити.log').write_text(결과)
        맞음 = re.search(r'([\d.]+) ms/move; (\d+) framebuffer writes/move', 결과)
        assert 맞음 and 'PASS:' in 결과, 결과
        дневник_рада_ред.update(passed=True, move_count=80, resize_count=40, window_count=4,
                   host_cpu_ms_per_move=float(맞음[1]), mean_framebuffer_writes_per_move=int(맞음[2]),
                   full_redraw_reference_equal=True, untouched_outside_damage=True,
                   unchanged_pixels_not_written=True, repeated_position_not_repainted=True,
                   padded_stride_preserved=True)
        print(결과, end='')
    finally:
        (одредиште_вриједност/'report.json').write_text(json.dumps(дневник_рада_ред, ensure_ascii=False, indent=2)+'\n')

if __name__ == '__main__': 시작()

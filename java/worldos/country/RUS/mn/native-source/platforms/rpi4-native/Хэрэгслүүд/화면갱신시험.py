#!/usr/bin/env python3
"""бодит_өгөгдөл кернел_утга 그리기 코드를 хост санах_ой_өгөгдөл 화면에 연결해 부분 갱신을 검증한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

기준 = Path(__file__).resolve().parents[1]

def Ажиллуулах():
    эх_Файлууд = ['시험/화면갱신.c', 'компьютер/화면그림.c', 'компьютер/Терминал.c', 'компьютер/виджэт.c']
    검증원문들 = эх_Файлууд + ['ЭХ/화면합성.java', 'ЭХ/보드.java', '../../compiler/자바도구/기계어미리번역.java']
    товлосон_газар_утга = 기준/'build/verification/redraw'; товлосон_газар_утга.mkdir(parents=True, exist_ok=True)
    бичих_мөр_6e8b375a = {'passed': False, 'test_environment': 'host CPU, Java AOT framebuffer composition and native terminal/widgets with memory framebuffer',
          'kernel_sha256': hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),
          'source_sha256': {Нэр: hashlib.sha256((기준/Нэр).read_bytes()).hexdigest() for Нэр in 검증원문들}}
    try:
        класс_зам = товлосон_газар_утга/'classes'; класс_зам.mkdir(exist_ok=True)
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(класс_зам),
            str(기준/'ЭХ/화면합성.java'), str(기준/'ЭХ/보드.java')])
        экспортлох_хүснэгт = {'jdraw_prepare': 'Бэлтгэх', 'jdraw_width': '너비얻기', 'jdraw_height': '높이얻기',
            'jdraw_count_low': '기록아래얻기', 'jdraw_count_high': '기록위얻기', 'jdraw_clip': 'клип',
            'jdraw_clip_value': 'клип_утга', 'jdraw_begin': 'Ажиллуулах', 'jdraw_end': 'Дуусгах',
            'jdraw_pixel': 'нягтрал', 'jdraw_rectangle': '사각그림', 'jdraw_pointer': 'заагч'}
        번역명령 = ['sh', str(기준.parents[1]/'compiler/미리번역.sh'), '--entry', '화면합성.너비얻기', '-o', str(товлосон_газар_утга/'зураг_утга_c143fe9e.c')]
        for Холбох, ФУНКЦ_утга in экспортлох_хүснэгт.items(): 번역명령.extend(['--export', Холбох+'=화면합성.'+ФУНКЦ_утга])
        subprocess.check_call(번역명령+[str(ЗАМ) for ЗАМ in sorted(класс_зам.glob('*.class'))])
        Тушаал = ['clang', '-std=c11', '-O2', '-Wall', '-Wextra', '-Werror'] + эх_Файлууд
        зураг_товлосон_газар = товлосон_газар_утга/'зураг_утга_c143fe9e.o'
        subprocess.check_call(['clang', '-std=c11', '-O2', '-c', str(товлосон_газар_утга/'зураг_утга_c143fe9e.c'), '-o', str(зураг_товлосон_газар)])
        subprocess.check_call(Тушаал+[str(зураг_товлосон_газар), 'build/terminal-font.S', '-o', str(товлосон_газар_утга/'화면갱신시험')], cwd=str(기준))
        결과 = subprocess.check_output([str(товлосон_газар_утга/'화면갱신시험')], timeout=30).decode()
        (товлосон_газар_утга/'баталгаажуулах.log').write_text(결과)
        맞음 = re.search(r'([\d.]+) ms/move; (\d+) framebuffer writes/move', 결과)
        assert 맞음 and 'PASS:' in 결과, 결과
        бичих_мөр_6e8b375a.update(passed=True, move_count=80, resize_count=40, window_count=4,
                   host_cpu_ms_per_move=float(맞음[1]), mean_framebuffer_writes_per_move=int(맞음[2]),
                   full_redraw_reference_equal=True, untouched_outside_damage=True,
                   unchanged_pixels_not_written=True, repeated_position_not_repainted=True,
                   padded_stride_preserved=True)
        print(결과, end='')
    finally:
        (товлосон_газар_утга/'report.json').write_text(json.dumps(бичих_мөр_6e8b375a, ensure_ascii=False, indent=2)+'\n')

if __name__ == '__main__': Ажиллуулах()

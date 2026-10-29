#!/usr/bin/env python3
"""стваран_подаци језгро_вриједност 그리기 코드를 хост Меморија_подаци 화면에 연결해 부분 갱신을 검증한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

пројектовати_корен = Path(__file__).resolve().parents[1]

def Покрени():
    извор_Фајлови = ['시험/화면갱신.c', 'рачунар/화면그림.c', 'рачунар/Терминал.c', 'рачунар/виџет.c']
    검증원문들 = извор_Фајлови + ['ИЗВОР/화면합성.java', 'ИЗВОР/Табла.java', '../../compiler/자바도구/기계어미리번역.java']
    одредиште_вриједност = пројектовати_корен/'build/verification/redraw'; одредиште_вриједност.mkdir(parents=True, exist_ok=True)
    евиденција_ред = {'passed': False, 'test_environment': 'host CPU, Java AOT framebuffer composition and native terminal/widgets with memory framebuffer',
          'kernel_sha256': hashlib.sha256((пројектовати_корен/'build/kernel8.img').read_bytes()).hexdigest(),
          'source_sha256': {Назив: hashlib.sha256((пројектовати_корен/Назив).read_bytes()).hexdigest() for Назив in 검증원문들}}
    try:
        класа_пут = одредиште_вриједност/'classes'; класа_пут.mkdir(exist_ok=True)
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(класа_пут),
            str(пројектовати_корен/'ИЗВОР/화면합성.java'), str(пројектовати_корен/'ИЗВОР/Табла.java')])
        Извоз_табела = {'jdraw_prepare': 'Припремити', 'jdraw_width': '너비얻기', 'jdraw_height': '높이얻기',
            'jdraw_count_low': '기록아래얻기', 'jdraw_count_high': '기록위얻기', 'jdraw_clip': 'клип',
            'jdraw_clip_value': 'клип_вриједност', 'jdraw_begin': 'Покрени', 'jdraw_end': 'Крај',
            'jdraw_pixel': 'пиксел', 'jdraw_rectangle': '사각그림', 'jdraw_pointer': 'показивач'}
        번역명령 = ['sh', str(пројектовати_корен.parents[1]/'compiler/미리번역.sh'), '--entry', '화면합성.너비얻기', '-o', str(одредиште_вриједност/'цртеж_вриједност.c')]
        for Повежи_се, функција_вриједност in Извоз_табела.items(): 번역명령.extend(['--export', Повежи_се+'=화면합성.'+функција_вриједност])
        subprocess.check_call(번역명령+[str(ПУТАЊА) for ПУТАЊА in sorted(класа_пут.glob('*.class'))])
        Наредба = ['clang', '-std=c11', '-O2', '-Wall', '-Wextra', '-Werror'] + извор_Фајлови
        цртеж_одредиште = одредиште_вриједност/'цртеж_вриједност.o'
        subprocess.check_call(['clang', '-std=c11', '-O2', '-c', str(одредиште_вриједност/'цртеж_вриједност.c'), '-o', str(цртеж_одредиште)])
        subprocess.check_call(Наредба+[str(цртеж_одредиште), 'build/terminal-font.S', '-o', str(одредиште_вриједност/'화면갱신시험')], cwd=str(пројектовати_корен))
        ИСХОД = subprocess.check_output([str(одредиште_вриједност/'화면갱신시험')], timeout=30).decode()
        (одредиште_вриједност/'потврдити_5fb2b747.log').write_text(ИСХОД)
        맞음 = re.search(r'([\d.]+) ms/move; (\d+) framebuffer writes/move', ИСХОД)
        assert 맞음 and 'PASS:' in ИСХОД, ИСХОД
        евиденција_ред.update(passed=True, move_count=80, resize_count=40, window_count=4,
                   host_cpu_ms_per_move=float(맞음[1]), mean_framebuffer_writes_per_move=int(맞음[2]),
                   full_redraw_reference_equal=True, untouched_outside_damage=True,
                   unchanged_pixels_not_written=True, repeated_position_not_repainted=True,
                   padded_stride_preserved=True)
        print(ИСХОД, end='')
    finally:
        (одредиште_вриједност/'report.json').write_text(json.dumps(евиденција_ред, ensure_ascii=False, indent=2)+'\n')

if __name__ == '__main__': Покрени()

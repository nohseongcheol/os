#!/usr/bin/env python3
"""реален_податоци јадро_VALUE 그리기 코드를 вдоми Меморија_податоци 화면에 연결해 부분 갱신을 검증한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

Project_корен = Path(__file__).resolve().parents[1]

def Изврши_2():
    извор_Датотеки = ['시험/화면갱신.c', 'машина/화면그림.c', 'машина/Терминал.c', 'машина/графичка_контрола.c']
    검증원문들 = извор_Датотеки + ['ИЗВОР/화면합성.java', 'ИЗВОР/табла.java', '../../compiler/자바도구/기계어미리번역.java']
    одредиште_VALUE = Project_корен/'build/verification/redraw'; одредиште_VALUE.mkdir(parents=True, exist_ok=True)
    LOG_ред = {'passed': False, 'test_environment': 'host CPU, Java AOT framebuffer composition and native terminal/widgets with memory framebuffer',
          'kernel_sha256': hashlib.sha256((Project_корен/'build/kernel8.img').read_bytes()).hexdigest(),
          'source_sha256': {Име: hashlib.sha256((Project_корен/Име).read_bytes()).hexdigest() for Име in 검증원문들}}
    try:
        класа_патека = одредиште_VALUE/'classes'; класа_патека.mkdir(exist_ok=True)
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(класа_патека),
            str(Project_корен/'ИЗВОР/화면합성.java'), str(Project_корен/'ИЗВОР/табла.java')])
        извези_табела = {'jdraw_prepare': 'Подготви', 'jdraw_width': '너비얻기', 'jdraw_height': '높이얻기',
            'jdraw_count_low': '기록아래얻기', 'jdraw_count_high': '기록위얻기', 'jdraw_clip': 'клип',
            'jdraw_clip_value': 'клип_VALUE', 'jdraw_begin': 'Изврши_2', 'jdraw_end': 'Крај',
            'jdraw_pixel': 'пиксел', 'jdraw_rectangle': '사각그림', 'jdraw_pointer': 'покажувач'}
        번역명령 = ['sh', str(Project_корен.parents[1]/'compiler/미리번역.sh'), '--entry', '화면합성.너비얻기', '-o', str(одредиште_VALUE/'цртеж_VALUE.c')]
        for Врзи_се, ФУНКЦИЈА_VALUE in извези_табела.items(): 번역명령.extend(['--export', Врзи_се+'=화면합성.'+ФУНКЦИЈА_VALUE])
        subprocess.check_call(번역명령+[str(ПАТЕКА) for ПАТЕКА in sorted(класа_патека.glob('*.class'))])
        Команда = ['clang', '-std=c11', '-O2', '-Wall', '-Wextra', '-Werror'] + извор_Датотеки
        цртеж_одредиште = одредиште_VALUE/'цртеж_VALUE.o'
        subprocess.check_call(['clang', '-std=c11', '-O2', '-c', str(одредиште_VALUE/'цртеж_VALUE.c'), '-o', str(цртеж_одредиште)])
        subprocess.check_call(Команда+[str(цртеж_одредиште), 'build/terminal-font.S', '-o', str(одредиште_VALUE/'화면갱신시험')], cwd=str(Project_корен))
        мерка = subprocess.check_output([str(одредиште_VALUE/'화면갱신시험')], timeout=30).decode()
        (одредиште_VALUE/'потврди.log').write_text(мерка)
        맞음 = re.search(r'([\d.]+) ms/move; (\d+) framebuffer writes/move', мерка)
        assert 맞음 and 'PASS:' in мерка, мерка
        LOG_ред.update(passed=True, move_count=80, resize_count=40, window_count=4,
                   host_cpu_ms_per_move=float(맞음[1]), mean_framebuffer_writes_per_move=int(맞음[2]),
                   full_redraw_reference_equal=True, untouched_outside_damage=True,
                   unchanged_pixels_not_written=True, repeated_position_not_repainted=True,
                   padded_stride_preserved=True)
        print(мерка, end='')
    finally:
        (одредиште_VALUE/'report.json').write_text(json.dumps(LOG_ред, ensure_ascii=False, indent=2)+'\n')

if __name__ == '__main__': Изврши_2()

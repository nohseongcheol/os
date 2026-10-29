#!/usr/bin/env python3
"""фактычны_дадзеныя ядро_значэнне 그리기 코드를 вузел памяць_дадзеныя 화면에 연결해 부분 갱신을 검증한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

기준 = Path(__file__).resolve().parents[1]

def Выканаць():
    крыніца_Файлы = ['시험/화면갱신.c', 'камп_ютар/화면그림.c', 'камп_ютар/Тэрмінал.c', 'камп_ютар/віджэт.c']
    검증원문들 = крыніца_Файлы + ['КРЫНІЦА/화면합성.java', 'КРЫНІЦА/보드.java', '../../compiler/자바도구/기계어미리번역.java']
    прызначэнне_значэнне_a0fbc067 = 기준/'build/verification/redraw'; прызначэнне_значэнне_a0fbc067.mkdir(parents=True, exist_ok=True)
    журнал_запіс = {'passed': False, 'test_environment': 'host CPU, Java AOT framebuffer composition and native terminal/widgets with memory framebuffer',
          'kernel_sha256': hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),
          'source_sha256': {Назва: hashlib.sha256((기준/Назва).read_bytes()).hexdigest() for Назва in 검증원문들}}
    try:
        клас_шлях = прызначэнне_значэнне_a0fbc067/'classes'; клас_шлях.mkdir(exist_ok=True)
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(клас_шлях),
            str(기준/'КРЫНІЦА/화면합성.java'), str(기준/'КРЫНІЦА/보드.java')])
        экспартаваць_табліца = {'jdraw_prepare': 'Падрыхтаваць', 'jdraw_width': '너비얻기', 'jdraw_height': '높이얻기',
            'jdraw_count_low': '기록아래얻기', 'jdraw_count_high': '기록위얻기', 'jdraw_clip': 'кліп',
            'jdraw_clip_value': 'кліп_значэнне', 'jdraw_begin': 'Выканаць', 'jdraw_end': 'Гатова',
            'jdraw_pixel': 'пэл', 'jdraw_rectangle': '사각그림', 'jdraw_pointer': 'указальнік'}
        번역명령 = ['sh', str(기준.parents[1]/'compiler/미리번역.sh'), '--entry', '화면합성.너비얻기', '-o', str(прызначэнне_значэнне_a0fbc067/'рукапісная_графіка_значэнне.c')]
        for Злучыцца, функцыя_значэнне in экспартаваць_табліца.items(): 번역명령.extend(['--export', Злучыцца+'=화면합성.'+функцыя_значэнне])
        subprocess.check_call(번역명령+[str(ШЛЯХ) for ШЛЯХ in sorted(клас_шлях.glob('*.class'))])
        Загад = ['clang', '-std=c11', '-O2', '-Wall', '-Wextra', '-Werror'] + крыніца_Файлы
        рукапісная_графіка_прызначэнне = прызначэнне_значэнне_a0fbc067/'рукапісная_графіка_значэнне.o'
        subprocess.check_call(['clang', '-std=c11', '-O2', '-c', str(прызначэнне_значэнне_a0fbc067/'рукапісная_графіка_значэнне.c'), '-o', str(рукапісная_графіка_прызначэнне)])
        subprocess.check_call(Загад+[str(рукапісная_графіка_прызначэнне), 'build/terminal-font.S', '-o', str(прызначэнне_значэнне_a0fbc067/'화면갱신시험')], cwd=str(기준))
        결과 = subprocess.check_output([str(прызначэнне_значэнне_a0fbc067/'화면갱신시험')], timeout=30).decode()
        (прызначэнне_значэнне_a0fbc067/'праверыць_5fb2b747.log').write_text(결과)
        맞음 = re.search(r'([\d.]+) ms/move; (\d+) framebuffer writes/move', 결과)
        assert 맞음 and 'PASS:' in 결과, 결과
        журнал_запіс.update(passed=True, move_count=80, resize_count=40, window_count=4,
                   host_cpu_ms_per_move=float(맞음[1]), mean_framebuffer_writes_per_move=int(맞음[2]),
                   full_redraw_reference_equal=True, untouched_outside_damage=True,
                   unchanged_pixels_not_written=True, repeated_position_not_repainted=True,
                   padded_stride_preserved=True)
        print(결과, end='')
    finally:
        (прызначэнне_значэнне_a0fbc067/'report.json').write_text(json.dumps(журнал_запіс, ensure_ascii=False, indent=2)+'\n')

if __name__ == '__main__': Выканаць()

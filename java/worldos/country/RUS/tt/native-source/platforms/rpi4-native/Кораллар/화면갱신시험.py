#!/usr/bin/env python3
"""фактик_мәгълүмат төш_VALUE 그리기 코드를 хост Хәтер_мәгълүмат 화면에 연결해 부분 갱신을 검증한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

экранга_җибәрү_тамыр = Path(__file__).resolve().parents[1]

def эшләтү():
    чыганак_Файллар = ['시험/화면갱신.c', 'машина/화면그림.c', 'машина/Терминал.c', 'машина/виджет.c']
    검증원문들 = чыганак_Файллар + ['чыганак/화면합성.java', 'чыганак/такта.java', '../../compiler/자바도구/기계어미리번역.java']
    күчерү_урыны_VALUE = экранга_җибәрү_тамыр/'build/verification/redraw'; күчерү_урыны_VALUE.mkdir(parents=True, exist_ok=True)
    LOG_юл = {'passed': False, 'test_environment': 'host CPU, Java AOT framebuffer composition and native terminal/widgets with memory framebuffer',
          'kernel_sha256': hashlib.sha256((экранга_җибәрү_тамыр/'build/kernel8.img').read_bytes()).hexdigest(),
          'source_sha256': {исем: hashlib.sha256((экранга_җибәрү_тамыр/исем).read_bytes()).hexdigest() for исем in 검증원문들}}
    try:
        класс_юл = күчерү_урыны_VALUE/'classes'; класс_юл.mkdir(exist_ok=True)
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(класс_юл),
            str(экранга_җибәрү_тамыр/'чыганак/화면합성.java'), str(экранга_җибәрү_тамыр/'чыганак/такта.java')])
        экспортлау_таблица = {'jdraw_prepare': 'Әзерләү', 'jdraw_width': '너비얻기', 'jdraw_height': '높이얻기',
            'jdraw_count_low': '기록아래얻기', 'jdraw_count_high': '기록위얻기', 'jdraw_clip': 'клип',
            'jdraw_clip_value': 'клип_VALUE', 'jdraw_begin': 'эшләтү', 'jdraw_end': 'Әзер',
            'jdraw_pixel': 'нокта', 'jdraw_rectangle': '사각그림', 'jdraw_pointer': 'күрсәткеч'}
        번역명령 = ['sh', str(экранга_җибәрү_тамыр.parents[1]/'compiler/미리번역.sh'), '--entry', '화면합성.너비얻기', '-o', str(күчерү_урыны_VALUE/'сызым_VALUE.c')]
        for ялгау, ФУНКЦИЯ_VALUE in экспортлау_таблица.items(): 번역명령.extend(['--export', ялгау+'=화면합성.'+ФУНКЦИЯ_VALUE])
        subprocess.check_call(번역명령+[str(Yul) for Yul in sorted(класс_юл.glob('*.class'))])
        команда = ['clang', '-std=c11', '-O2', '-Wall', '-Wextra', '-Werror'] + чыганак_Файллар
        сызым_күчерү_урыны = күчерү_урыны_VALUE/'сызым_VALUE.o'
        subprocess.check_call(['clang', '-std=c11', '-O2', '-c', str(күчерү_урыны_VALUE/'сызым_VALUE.c'), '-o', str(сызым_күчерү_урыны)])
        subprocess.check_call(команда+[str(сызым_күчерү_урыны), 'build/terminal-font.S', '-o', str(күчерү_урыны_VALUE/'화면갱신시험')], cwd=str(экранга_җибәрү_тамыр))
        үлчәм = subprocess.check_output([str(күчерү_урыны_VALUE/'화면갱신시험')], timeout=30).decode()
        (күчерү_урыны_VALUE/'тикшерү.log').write_text(үлчәм)
        맞음 = re.search(r'([\d.]+) ms/move; (\d+) framebuffer writes/move', үлчәм)
        assert 맞음 and 'PASS:' in үлчәм, үлчәм
        LOG_юл.update(passed=True, move_count=80, resize_count=40, window_count=4,
                   host_cpu_ms_per_move=float(맞음[1]), mean_framebuffer_writes_per_move=int(맞음[2]),
                   full_redraw_reference_equal=True, untouched_outside_damage=True,
                   unchanged_pixels_not_written=True, repeated_position_not_repainted=True,
                   padded_stride_preserved=True)
        print(үлчәм, end='')
    finally:
        (күчерү_урыны_VALUE/'report.json').write_text(json.dumps(LOG_юл, ensure_ascii=False, indent=2)+'\n')

if __name__ == '__main__': эшләтү()

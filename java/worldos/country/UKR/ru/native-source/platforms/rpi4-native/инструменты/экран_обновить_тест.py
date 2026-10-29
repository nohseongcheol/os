#!/usr/bin/env python3
"""фактический_данные ядро_ЗНАЧЕН Paint_экран 코드를 узел Память_данные 화면에 연결해 부분 갱신을 검증한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

задача_корень = Path(__file__).resolve().parents[1]

def запустить():
    источник_Файлы = ['испытания/обновить_экран.c', 'компьютер_5eb260fa/экран_рисунок.c', 'компьютер_5eb260fa/терминал.c', 'компьютер_5eb260fa/элемент_экрана.c']
    검증원문들 = источник_Файлы + ['исходныйКод/КомпозицияЭкрана.java', 'исходныйКод/Доска.java', '../../compiler/СредстваJava/ПредварительныйКомпилятор.java']
    цель_ЗНАЧЕН = задача_корень/'build/verification/redraw'; цель_ЗНАЧЕН.mkdir(parents=True, exist_ok=True)
    LOG_ЗАПИСЬ = {'passed': False, 'test_environment': 'host CPU, Java AOT framebuffer composition and native terminal/widgets with memory framebuffer',
          'kernel_sha256': hashlib.sha256((задача_корень/'build/kernel8.img').read_bytes()).hexdigest(),
          'source_sha256': {Название: hashlib.sha256((задача_корень/Название).read_bytes()).hexdigest() for Название in 검증원문들}}
    try:
        Класс_путь = цель_ЗНАЧЕН/'classes'; Класс_путь.mkdir(exist_ok=True)
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(Класс_путь),
            str(задача_корень/'исходныйКод/КомпозицияЭкрана.java'), str(задача_корень/'исходныйКод/Доска.java')])
        экспортировать_таблица = {'jdraw_prepare': 'Подготовить', 'jdraw_width': '너비얻기', 'jdraw_height': '높이얻기',
            'jdraw_count_low': '기록아래얻기', 'jdraw_count_high': '기록위얻기', 'jdraw_clip': 'клип',
            'jdraw_clip_value': 'клип_ЗНАЧЕН', 'jdraw_begin': 'запустить', 'jdraw_end': 'Готово',
            'jdraw_pixel': 'пиксель', 'jdraw_rectangle': 'прямоугольник_залить', 'jdraw_pointer': 'указатель'}
        번역명령 = ['sh', str(задача_корень.parents[1]/'compiler/미리번역.sh'), '--entry', 'КомпозицияЭкрана.너비얻기', '-o', str(цель_ЗНАЧЕН/'рисунок_ЗНАЧЕН.c')]
        for Подключить, ФУНКЦИЯ_ЗНАЧЕН in экспортировать_таблица.items(): 번역명령.extend(['--export', Подключить+'=КомпозицияЭкрана.'+ФУНКЦИЯ_ЗНАЧЕН])
        subprocess.check_call(번역명령+[str(путь) for путь in sorted(Класс_путь.glob('*.class'))])
        команда = ['clang', '-std=c11', '-O2', '-Wall', '-Wextra', '-Werror'] + источник_Файлы
        рисунок_цель = цель_ЗНАЧЕН/'рисунок_ЗНАЧЕН.o'
        subprocess.check_call(['clang', '-std=c11', '-O2', '-c', str(цель_ЗНАЧЕН/'рисунок_ЗНАЧЕН.c'), '-o', str(рисунок_цель)])
        subprocess.check_call(команда+[str(рисунок_цель), 'build/terminal-font.S', '-o', str(цель_ЗНАЧЕН/'экран_обновить_тест')], cwd=str(задача_корень))
        результат = subprocess.check_output([str(цель_ЗНАЧЕН/'экран_обновить_тест')], timeout=30).decode()
        (цель_ЗНАЧЕН/'проверить.log').write_text(результат)
        맞음 = re.search(r'([\d.]+) ms/move; (\d+) framebuffer writes/move', результат)
        assert 맞음 and 'PASS:' in результат, результат
        LOG_ЗАПИСЬ.update(passed=True, move_count=80, resize_count=40, window_count=4,
                   host_cpu_ms_per_move=float(맞음[1]), mean_framebuffer_writes_per_move=int(맞음[2]),
                   full_redraw_reference_equal=True, untouched_outside_damage=True,
                   unchanged_pixels_not_written=True, repeated_position_not_repainted=True,
                   padded_stride_preserved=True)
        print(результат, end='')
    finally:
        (цель_ЗНАЧЕН/'report.json').write_text(json.dumps(LOG_ЗАПИСЬ, ensure_ascii=False, indent=2)+'\n')

if __name__ == '__main__': запустить()

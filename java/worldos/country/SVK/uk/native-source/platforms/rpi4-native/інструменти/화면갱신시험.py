#!/usr/bin/env python3
"""фактично_дані ядро_значення 그리기 코드를 хост Пам_ять_дані 화면에 연결해 부분 갱신을 검증한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

Дії_корінь = Path(__file__).resolve().parents[1]

def запустити():
    джерело_Файли = ['випробування/화면갱신.c', 'комп_ютер/화면그림.c', 'комп_ютер/термінал.c', 'комп_ютер/елемент_екрана.c']
    검증원문들 = джерело_Файли + ['вихіднийКод/화면합성.java', 'вихіднийКод/Дошка.java', '../../compiler/자바도구/기계어미리번역.java']
    місце_значення = Дії_корінь/'build/verification/redraw'; місце_значення.mkdir(parents=True, exist_ok=True)
    журнал_запис = {'passed': False, 'test_environment': 'host CPU, Java AOT framebuffer composition and native terminal/widgets with memory framebuffer',
          'kernel_sha256': hashlib.sha256((Дії_корінь/'build/kernel8.img').read_bytes()).hexdigest(),
          'source_sha256': {Назва: hashlib.sha256((Дії_корінь/Назва).read_bytes()).hexdigest() for Назва in 검증원문들}}
    try:
        Клас_шлях = місце_значення/'classes'; Клас_шлях.mkdir(exist_ok=True)
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(Клас_шлях),
            str(Дії_корінь/'вихіднийКод/화면합성.java'), str(Дії_корінь/'вихіднийКод/Дошка.java')])
        експортувати_таблиця = {'jdraw_prepare': 'Готувати', 'jdraw_width': '너비얻기', 'jdraw_height': '높이얻기',
            'jdraw_count_low': '기록아래얻기', 'jdraw_count_high': '기록위얻기', 'jdraw_clip': 'кліп',
            'jdraw_clip_value': 'кліп_значення', 'jdraw_begin': 'запустити', 'jdraw_end': 'Готово',
            'jdraw_pixel': 'елемент_зображення', 'jdraw_rectangle': 'прямокутник_заливка', 'jdraw_pointer': 'курсор'}
        번역명령 = ['sh', str(Дії_корінь.parents[1]/'compiler/미리번역.sh'), '--entry', '화면합성.너비얻기', '-o', str(місце_значення/'малювання_значення.c')]
        for З_єднання, функція_значення in експортувати_таблиця.items(): 번역명령.extend(['--export', З_єднання+'=화면합성.'+функція_значення])
        subprocess.check_call(번역명령+[str(шлях) for шлях in sorted(Клас_шлях.glob('*.class'))])
        команда = ['clang', '-std=c11', '-O2', '-Wall', '-Wextra', '-Werror'] + джерело_Файли
        малювання_місце = місце_значення/'малювання_значення.o'
        subprocess.check_call(['clang', '-std=c11', '-O2', '-c', str(місце_значення/'малювання_значення.c'), '-o', str(малювання_місце)])
        subprocess.check_call(команда+[str(малювання_місце), 'build/terminal-font.S', '-o', str(місце_значення/'화면갱신시험')], cwd=str(Дії_корінь))
        результат = subprocess.check_output([str(місце_значення/'화면갱신시험')], timeout=30).decode()
        (місце_значення/'затвердити.log').write_text(результат)
        맞음 = re.search(r'([\d.]+) ms/move; (\d+) framebuffer writes/move', результат)
        assert 맞음 and 'PASS:' in результат, результат
        журнал_запис.update(passed=True, move_count=80, resize_count=40, window_count=4,
                   host_cpu_ms_per_move=float(맞음[1]), mean_framebuffer_writes_per_move=int(맞음[2]),
                   full_redraw_reference_equal=True, untouched_outside_damage=True,
                   unchanged_pixels_not_written=True, repeated_position_not_repainted=True,
                   padded_stride_preserved=True)
        print(результат, end='')
    finally:
        (місце_значення/'report.json').write_text(json.dumps(журнал_запис, ensure_ascii=False, indent=2)+'\n')

if __name__ == '__main__': запустити()

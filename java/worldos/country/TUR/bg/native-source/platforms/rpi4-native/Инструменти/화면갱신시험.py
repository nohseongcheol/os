#!/usr/bin/env python3
"""действителен_данни ядро_стойност 그리기 코드를 хост Памет_данни 화면에 연결해 부분 갱신을 검증한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

проект_корен = Path(__file__).resolve().parents[1]

def Стартиране():
    източник_Файлове = ['시험/화면갱신.c', 'машина/화면그림.c', 'машина/Терминал.c', 'машина/изпълним_модул.c']
    검증원문들 = източник_Файлове + ['ИЗТОЧНИК/화면합성.java', 'ИЗТОЧНИК/Табло.java', '../../compiler/자바도구/기계어미리번역.java']
    местоназначение_стойност = проект_корен/'build/verification/redraw'; местоназначение_стойност.mkdir(parents=True, exist_ok=True)
    регистрирам_запис = {'passed': False, 'test_environment': 'host CPU, Java AOT framebuffer composition and native terminal/widgets with memory framebuffer',
          'kernel_sha256': hashlib.sha256((проект_корен/'build/kernel8.img').read_bytes()).hexdigest(),
          'source_sha256': {Име: hashlib.sha256((проект_корен/Име).read_bytes()).hexdigest() for Име in 검증원문들}}
    try:
        Клас_път = местоназначение_стойност/'classes'; Клас_път.mkdir(exist_ok=True)
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(Клас_път),
            str(проект_корен/'ИЗТОЧНИК/화면합성.java'), str(проект_корен/'ИЗТОЧНИК/Табло.java')])
        експортирам_таблица = {'jdraw_prepare': 'Подготвяне', 'jdraw_width': '너비얻기', 'jdraw_height': '높이얻기',
            'jdraw_count_low': '기록아래얻기', 'jdraw_count_high': '기록위얻기', 'jdraw_clip': 'клип',
            'jdraw_clip_value': 'клип_стойност', 'jdraw_begin': 'Стартиране', 'jdraw_end': 'Готово',
            'jdraw_pixel': 'пиксел', 'jdraw_rectangle': 'правоъгълник_запълване', 'jdraw_pointer': 'показалец'}
        번역명령 = ['sh', str(проект_корен.parents[1]/'compiler/미리번역.sh'), '--entry', '화면합성.너비얻기', '-o', str(местоназначение_стойност/'чертеж_стойност.c')]
        for Свързване, функция_стойност in експортирам_таблица.items(): 번역명령.extend(['--export', Свързване+'=화면합성.'+функция_стойност])
        subprocess.check_call(번역명령+[str(ПЪТ) for ПЪТ in sorted(Клас_път.glob('*.class'))])
        Команда = ['clang', '-std=c11', '-O2', '-Wall', '-Wextra', '-Werror'] + източник_Файлове
        чертеж_местоназначение = местоназначение_стойност/'чертеж_стойност.o'
        subprocess.check_call(['clang', '-std=c11', '-O2', '-c', str(местоназначение_стойност/'чертеж_стойност.c'), '-o', str(чертеж_местоназначение)])
        subprocess.check_call(Команда+[str(чертеж_местоназначение), 'build/terminal-font.S', '-o', str(местоназначение_стойност/'화면갱신시험')], cwd=str(проект_корен))
        РЕЗУЛТАТ = subprocess.check_output([str(местоназначение_стойност/'화면갱신시험')], timeout=30).decode()
        (местоназначение_стойност/'проверка.log').write_text(РЕЗУЛТАТ)
        맞음 = re.search(r'([\d.]+) ms/move; (\d+) framebuffer writes/move', РЕЗУЛТАТ)
        assert 맞음 and 'PASS:' in РЕЗУЛТАТ, РЕЗУЛТАТ
        регистрирам_запис.update(passed=True, move_count=80, resize_count=40, window_count=4,
                   host_cpu_ms_per_move=float(맞음[1]), mean_framebuffer_writes_per_move=int(맞음[2]),
                   full_redraw_reference_equal=True, untouched_outside_damage=True,
                   unchanged_pixels_not_written=True, repeated_position_not_repainted=True,
                   padded_stride_preserved=True)
        print(РЕЗУЛТАТ, end='')
    finally:
        (местоназначение_стойност/'report.json').write_text(json.dumps(регистрирам_запис, ensure_ascii=False, indent=2)+'\n')

if __name__ == '__main__': Стартиране()

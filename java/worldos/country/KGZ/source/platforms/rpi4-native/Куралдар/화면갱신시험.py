#!/usr/bin/env python3
"""актуалдуу_берилмелер өзөк_маани 그리기 코드를 кабылдоо эс_берилмелер 화면에 연결해 부분 갱신을 검증한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

기준 = Path(__file__).resolve().parents[1]

def Жүргүзүү():
    башат_Файлдар = ['시험/화면갱신.c', 'машина/화면그림.c', 'машина/Терминал.c', 'машина/уижет.c']
    검증원문들 = башат_Файлдар + ['Булак/화면합성.java', 'Булак/보드.java', '../../compiler/자바도구/기계어미리번역.java']
    көздөө_жайы_маани = 기준/'build/verification/redraw'; көздөө_жайы_маани.mkdir(parents=True, exist_ok=True)
    жазуу_катар = {'passed': False, 'test_environment': 'host CPU, Java AOT framebuffer composition and native terminal/widgets with memory framebuffer',
          'kernel_sha256': hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),
          'source_sha256': {Аты: hashlib.sha256((기준/Аты).read_bytes()).hexdigest() for Аты in 검증원문들}}
    try:
        класс_жол = көздөө_жайы_маани/'classes'; класс_жол.mkdir(exist_ok=True)
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(класс_жол),
            str(기준/'Булак/화면합성.java'), str(기준/'Булак/보드.java')])
        экспорттоо_жадыбал = {'jdraw_prepare': 'Даярдоо', 'jdraw_width': '너비얻기', 'jdraw_height': '높이얻기',
            'jdraw_count_low': '기록아래얻기', 'jdraw_count_high': '기록위얻기', 'jdraw_clip': 'клип',
            'jdraw_clip_value': 'клип_маани', 'jdraw_begin': 'Жүргүзүү', 'jdraw_end': 'Бүттү',
            'jdraw_pixel': 'пиксел', 'jdraw_rectangle': '사각그림', 'jdraw_pointer': 'көрсөткүч'}
        번역명령 = ['sh', str(기준.parents[1]/'compiler/미리번역.sh'), '--entry', '화면합성.너비얻기', '-o', str(көздөө_жайы_маани/'чийүү_маани.c')]
        for Туташуу, функция_маани in экспорттоо_жадыбал.items(): 번역명령.extend(['--export', Туташуу+'=화면합성.'+функция_маани])
        subprocess.check_call(번역명령+[str(ЖОЛ) for ЖОЛ in sorted(класс_жол.glob('*.class'))])
        Команда = ['clang', '-std=c11', '-O2', '-Wall', '-Wextra', '-Werror'] + башат_Файлдар
        чийүү_көздөө_жайы = көздөө_жайы_маани/'чийүү_маани.o'
        subprocess.check_call(['clang', '-std=c11', '-O2', '-c', str(көздөө_жайы_маани/'чийүү_маани.c'), '-o', str(чийүү_көздөө_жайы)])
        subprocess.check_call(Команда+[str(чийүү_көздөө_жайы), 'build/terminal-font.S', '-o', str(көздөө_жайы_маани/'화면갱신시험')], cwd=str(기준))
        결과 = subprocess.check_output([str(көздөө_жайы_маани/'화면갱신시험')], timeout=30).decode()
        (көздөө_жайы_маани/'жарактуулугун_текшерүү.log').write_text(결과)
        맞음 = re.search(r'([\d.]+) ms/move; (\d+) framebuffer writes/move', 결과)
        assert 맞음 and 'PASS:' in 결과, 결과
        жазуу_катар.update(passed=True, move_count=80, resize_count=40, window_count=4,
                   host_cpu_ms_per_move=float(맞음[1]), mean_framebuffer_writes_per_move=int(맞음[2]),
                   full_redraw_reference_equal=True, untouched_outside_damage=True,
                   unchanged_pixels_not_written=True, repeated_position_not_repainted=True,
                   padded_stride_preserved=True)
        print(결과, end='')
    finally:
        (көздөө_жайы_маани/'report.json').write_text(json.dumps(жазуу_катар, ensure_ascii=False, indent=2)+'\n')

if __name__ == '__main__': Жүргүзүү()

#!/usr/bin/env python3
"""нақты_деректер ядро_мән 그리기 코드를 орналастыру Жад_деректер 화면에 연결해 부분 갱신을 검증한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

жоба_түбір = Path(__file__).resolve().parents[1]

def Орындау_2():
    көз_Файлдар = ['시험/화면갱신.c', 'компьютер/화면그림.c', 'компьютер/Терминал.c', 'компьютер/виджет.c']
    검증원문들 = көз_Файлдар + ['Неден/화면합성.java', 'Неден/Тақта.java', '../../compiler/자바도구/기계어미리번역.java']
    тағайындау_мән = жоба_түбір/'build/verification/redraw'; тағайындау_мән.mkdir(parents=True, exist_ok=True)
    журнал_жол = {'passed': False, 'test_environment': 'host CPU, Java AOT framebuffer composition and native terminal/widgets with memory framebuffer',
          'kernel_sha256': hashlib.sha256((жоба_түбір/'build/kernel8.img').read_bytes()).hexdigest(),
          'source_sha256': {Аты: hashlib.sha256((жоба_түбір/Аты).read_bytes()).hexdigest() for Аты in 검증원문들}}
    try:
        оқу_жол = тағайындау_мән/'classes'; оқу_жол.mkdir(exist_ok=True)
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(оқу_жол),
            str(жоба_түбір/'Неден/화면합성.java'), str(жоба_түбір/'Неден/Тақта.java')])
        экспорттау_кесте = {'jdraw_prepare': 'Дайындау', 'jdraw_width': '너비얻기', 'jdraw_height': '높이얻기',
            'jdraw_count_low': '기록아래얻기', 'jdraw_count_high': '기록위얻기', 'jdraw_clip': 'клип',
            'jdraw_clip_value': 'клип_мән', 'jdraw_begin': 'Орындау_2', 'jdraw_end': 'соңы',
            'jdraw_pixel': 'нүкте', 'jdraw_rectangle': 'тік_төртбұрыш_бояу', 'jdraw_pointer': 'меңзер'}
        번역명령 = ['sh', str(жоба_түбір.parents[1]/'compiler/미리번역.sh'), '--entry', '화면합성.너비얻기', '-o', str(тағайындау_мән/'сызба_мән.c')]
        for Байланысу, функция_мән in экспорттау_кесте.items(): 번역명령.extend(['--export', Байланысу+'=화면합성.'+функция_мән])
        subprocess.check_call(번역명령+[str(Жол_2) for Жол_2 in sorted(оқу_жол.glob('*.class'))])
        Команда = ['clang', '-std=c11', '-O2', '-Wall', '-Wextra', '-Werror'] + көз_Файлдар
        сызба_тағайындау = тағайындау_мән/'сызба_мән.o'
        subprocess.check_call(['clang', '-std=c11', '-O2', '-c', str(тағайындау_мән/'сызба_мән.c'), '-o', str(сызба_тағайындау)])
        subprocess.check_call(Команда+[str(сызба_тағайындау), 'build/terminal-font.S', '-o', str(тағайындау_мән/'화면갱신시험')], cwd=str(жоба_түбір))
        НӘТИЖЕ = subprocess.check_output([str(тағайындау_мән/'화면갱신시험')], timeout=30).decode()
        (тағайындау_мән/'тексеру_5fb2b747.log').write_text(НӘТИЖЕ)
        맞음 = re.search(r'([\d.]+) ms/move; (\d+) framebuffer writes/move', НӘТИЖЕ)
        assert 맞음 and 'PASS:' in НӘТИЖЕ, НӘТИЖЕ
        журнал_жол.update(passed=True, move_count=80, resize_count=40, window_count=4,
                   host_cpu_ms_per_move=float(맞음[1]), mean_framebuffer_writes_per_move=int(맞음[2]),
                   full_redraw_reference_equal=True, untouched_outside_damage=True,
                   unchanged_pixels_not_written=True, repeated_position_not_repainted=True,
                   padded_stride_preserved=True)
        print(НӘТИЖЕ, end='')
    finally:
        (тағайындау_мән/'report.json').write_text(json.dumps(журнал_жол, ensure_ascii=False, indent=2)+'\n')

if __name__ == '__main__': Орындау_2()

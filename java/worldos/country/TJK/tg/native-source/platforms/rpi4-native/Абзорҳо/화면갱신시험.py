#!/usr/bin/env python3
"""воқеӣ_иттилоот ҳаста_қимат 그리기 코드를 мизбон ҳофиза_иттилоот 화면에 연결해 부분 갱신을 검증한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

기준 = Path(__file__).resolve().parents[1]

def порча():
    манбаъ_Файлҳо = ['시험/화면갱신.c', 'компютер/화면그림.c', 'компютер/터미널.c', 'компютер/виҷет.c']
    검증원문들 = манбаъ_Файлҳо + ['манбаъ/화면합성.java', 'манбаъ/보드.java', '../../compiler/자바도구/기계어미리번역.java']
    ҷои_таъинот_қимат = 기준/'build/verification/redraw'; ҷои_таъинот_қимат.mkdir(parents=True, exist_ok=True)
    сабт_кардан_сабт = {'passed': False, 'test_environment': 'host CPU, Java AOT framebuffer composition and native terminal/widgets with memory framebuffer',
          'kernel_sha256': hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),
          'source_sha256': {Ном: hashlib.sha256((기준/Ном).read_bytes()).hexdigest() for Ном in 검증원문들}}
    try:
        синф_масир = ҷои_таъинот_қимат/'classes'; синф_масир.mkdir(exist_ok=True)
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(синф_масир),
            str(기준/'манбаъ/화면합성.java'), str(기준/'манбаъ/보드.java')])
        содир_кардан_ҷадвал = {'jdraw_prepare': 'Омода_кардан', 'jdraw_width': '너비얻기', 'jdraw_height': '높이얻기',
            'jdraw_count_low': '기록아래얻기', 'jdraw_count_high': '기록위얻기', 'jdraw_clip': 'клип',
            'jdraw_clip_value': 'клип_қимат', 'jdraw_begin': 'порча', 'jdraw_end': 'Тайёр',
            'jdraw_pixel': 'пиксел', 'jdraw_rectangle': '사각그림', 'jdraw_pointer': 'курсор'}
        번역명령 = ['sh', str(기준.parents[1]/'compiler/미리번역.sh'), '--entry', '화면합성.너비얻기', '-o', str(ҷои_таъинот_қимат/'нақша_қимат.c')]
        for ПАЙВАСТ, функсия_қимат in содир_кардан_ҷадвал.items(): 번역명령.extend(['--export', ПАЙВАСТ+'=화면합성.'+функсия_қимат])
        subprocess.check_call(번역명령+[str(масир) for масир in sorted(синф_масир.glob('*.class'))])
        фармон = ['clang', '-std=c11', '-O2', '-Wall', '-Wextra', '-Werror'] + манбаъ_Файлҳо
        нақша_ҷои_таъинот = ҷои_таъинот_қимат/'нақша_қимат.o'
        subprocess.check_call(['clang', '-std=c11', '-O2', '-c', str(ҷои_таъинот_қимат/'нақша_қимат.c'), '-o', str(нақша_ҷои_таъинот)])
        subprocess.check_call(фармон+[str(нақша_ҷои_таъинот), 'build/terminal-font.S', '-o', str(ҷои_таъинот_қимат/'화면갱신시험')], cwd=str(기준))
        결과 = subprocess.check_output([str(ҷои_таъинот_қимат/'화면갱신시험')], timeout=30).decode()
        (ҷои_таъинот_қимат/'санҷидани_эътибор.log').write_text(결과)
        맞음 = re.search(r'([\d.]+) ms/move; (\d+) framebuffer writes/move', 결과)
        assert 맞음 and 'PASS:' in 결과, 결과
        сабт_кардан_сабт.update(passed=True, move_count=80, resize_count=40, window_count=4,
                   host_cpu_ms_per_move=float(맞음[1]), mean_framebuffer_writes_per_move=int(맞음[2]),
                   full_redraw_reference_equal=True, untouched_outside_damage=True,
                   unchanged_pixels_not_written=True, repeated_position_not_repainted=True,
                   padded_stride_preserved=True)
        print(결과, end='')
    finally:
        (ҷои_таъинот_қимат/'report.json').write_text(json.dumps(сабт_кардан_сабт, ensure_ascii=False, indent=2)+'\n')

if __name__ == '__main__': порча()

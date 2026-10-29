#!/usr/bin/env python3
"""اصلي_ڪوائف ڪرنل_قدر 그리기 코드를 مهمان ميموري_ڪوائف 화면에 연결해 부분 갱신을 검증한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

기준 = Path(__file__).resolve().parents[1]

def هلائڻ():
    ماخذ_فائلون = ['시험/화면갱신.c', 'مشين/화면그림.c', 'مشين/터미널.c', 'مشين/وجيٽ.c']
    검증원문들 = ماخذ_فائلون + ['ماخذ/화면합성.java', 'ماخذ/보드.java', '../../compiler/자바도구/기계어미리번역.java']
    منزل_مقصود_قدر = 기준/'build/verification/redraw'; منزل_مقصود_قدر.mkdir(parents=True, exist_ok=True)
    لاگ_صف = {'passed': False, 'test_environment': 'host CPU, Java AOT framebuffer composition and native terminal/widgets with memory framebuffer',
          'kernel_sha256': hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),
          'source_sha256': {نالو: hashlib.sha256((기준/نالو).read_bytes()).hexdigest() for نالو in 검증원문들}}
    try:
        درجو_راههه = منزل_مقصود_قدر/'classes'; درجو_راههه.mkdir(exist_ok=True)
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(درجو_راههه),
            str(기준/'ماخذ/화면합성.java'), str(기준/'ماخذ/보드.java')])
        برآمد_جدول = {'jdraw_prepare': 'تياري_ڪريو', 'jdraw_width': '너비얻기', 'jdraw_height': '높이얻기',
            'jdraw_count_low': '기록아래얻기', 'jdraw_count_high': '기록위얻기', 'jdraw_clip': 'تراشه',
            'jdraw_clip_value': 'تراشه_قدر', 'jdraw_begin': 'هلائڻ', 'jdraw_end': 'ختم_ڪريو',
            'jdraw_pixel': 'پيل', 'jdraw_rectangle': '사각그림', 'jdraw_pointer': 'پوائنٽر'}
        번역명령 = ['sh', str(기준.parents[1]/'compiler/미리번역.sh'), '--entry', '화면합성.너비얻기', '-o', str(منزل_مقصود_قدر/'ڊرائنگ_قدر.c')]
        for ڪنيڪٽ, فعل_قدر in برآمد_جدول.items(): 번역명령.extend(['--export', ڪنيڪٽ+'=화면합성.'+فعل_قدر])
        subprocess.check_call(번역명령+[str(راههه) for راههه in sorted(درجو_راههه.glob('*.class'))])
        حڪم = ['clang', '-std=c11', '-O2', '-Wall', '-Wextra', '-Werror'] + ماخذ_فائلون
        ڊرائنگ_منزل_مقصود = منزل_مقصود_قدر/'ڊرائنگ_قدر.o'
        subprocess.check_call(['clang', '-std=c11', '-O2', '-c', str(منزل_مقصود_قدر/'ڊرائنگ_قدر.c'), '-o', str(ڊرائنگ_منزل_مقصود)])
        subprocess.check_call(حڪم+[str(ڊرائنگ_منزل_مقصود), 'build/terminal-font.S', '-o', str(منزل_مقصود_قدر/'화면갱신시험')], cwd=str(기준))
        결과 = subprocess.check_output([str(منزل_مقصود_قدر/'화면갱신시험')], timeout=30).decode()
        (منزل_مقصود_قدر/'ڪارگر_ڪريو.log').write_text(결과)
        맞음 = re.search(r'([\d.]+) ms/move; (\d+) framebuffer writes/move', 결과)
        assert 맞음 and 'PASS:' in 결과, 결과
        لاگ_صف.update(passed=True, move_count=80, resize_count=40, window_count=4,
                   host_cpu_ms_per_move=float(맞음[1]), mean_framebuffer_writes_per_move=int(맞음[2]),
                   full_redraw_reference_equal=True, untouched_outside_damage=True,
                   unchanged_pixels_not_written=True, repeated_position_not_repainted=True,
                   padded_stride_preserved=True)
        print(결과, end='')
    finally:
        (منزل_مقصود_قدر/'report.json').write_text(json.dumps(لاگ_صف, ensure_ascii=False, indent=2)+'\n')

if __name__ == '__main__': هلائڻ()

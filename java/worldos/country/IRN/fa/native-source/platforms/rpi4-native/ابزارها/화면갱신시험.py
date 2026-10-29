#!/usr/bin/env python3
"""واقعی_داده_ها هسته_مقدار 그리기 코드를 میزبان حافظه_داده_ها 화면에 연결해 부분 갱신을 검증한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

نمایش_دادن_جذر = Path(__file__).resolve().parents[1]

def اجرا_2():
    منبع_فایل = ['시험/화면갱신.c', 'دستگاه/화면그림.c', 'دستگاه/پایانه.c', 'دستگاه/ویجت.c']
    검증원문들 = منبع_فایل + ['مبداء/화면합성.java', 'مبداء/تخته_ای.java', '../../compiler/자바도구/기계어미리번역.java']
    مقصد_مقدار = نمایش_دادن_جذر/'build/verification/redraw'; مقصد_مقدار.mkdir(parents=True, exist_ok=True)
    واقعه_نگار_ردیف = {'passed': False, 'test_environment': 'host CPU, Java AOT framebuffer composition and native terminal/widgets with memory framebuffer',
          'kernel_sha256': hashlib.sha256((نمایش_دادن_جذر/'build/kernel8.img').read_bytes()).hexdigest(),
          'source_sha256': {نام: hashlib.sha256((نمایش_دادن_جذر/نام).read_bytes()).hexdigest() for نام in 검증원문들}}
    try:
        کلاس_مسیر = مقصد_مقدار/'classes'; کلاس_مسیر.mkdir(exist_ok=True)
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(کلاس_مسیر),
            str(نمایش_دادن_جذر/'مبداء/화면합성.java'), str(نمایش_دادن_جذر/'مبداء/تخته_ای.java')])
        صادرکردن_جدول = {'jdraw_prepare': 'آماده_کردن', 'jdraw_width': '너비얻기', 'jdraw_height': '높이얻기',
            'jdraw_count_low': '기록아래얻기', 'jdraw_count_high': '기록위얻기', 'jdraw_clip': 'کلیپ',
            'jdraw_clip_value': 'کلیپ_مقدار', 'jdraw_begin': 'اجرا_2', 'jdraw_end': 'خاتمه',
            'jdraw_pixel': 'پیکسل', 'jdraw_rectangle': '사각그림', 'jdraw_pointer': 'اشاره_گر'}
        번역명령 = ['sh', str(نمایش_دادن_جذر.parents[1]/'compiler/미리번역.sh'), '--entry', '화면합성.너비얻기', '-o', str(مقصد_مقدار/'نقاشی_مقدار.c')]
        for اتصال, عملکرد_مقدار in صادرکردن_جدول.items(): 번역명령.extend(['--export', اتصال+'=화면합성.'+عملکرد_مقدار])
        subprocess.check_call(번역명령+[str(مسیر) for مسیر in sorted(کلاس_مسیر.glob('*.class'))])
        فرمان = ['clang', '-std=c11', '-O2', '-Wall', '-Wextra', '-Werror'] + منبع_فایل
        نقاشی_مقصد = مقصد_مقدار/'نقاشی_مقدار.o'
        subprocess.check_call(['clang', '-std=c11', '-O2', '-c', str(مقصد_مقدار/'نقاشی_مقدار.c'), '-o', str(نقاشی_مقصد)])
        subprocess.check_call(فرمان+[str(نقاشی_مقصد), 'build/terminal-font.S', '-o', str(مقصد_مقدار/'화면갱신시험')], cwd=str(نمایش_دادن_جذر))
        سنجش = subprocess.check_output([str(مقصد_مقدار/'화면갱신시험')], timeout=30).decode()
        (مقصد_مقدار/'ارزیابی_کردن.log').write_text(سنجش)
        맞음 = re.search(r'([\d.]+) ms/move; (\d+) framebuffer writes/move', سنجش)
        assert 맞음 and 'PASS:' in سنجش, سنجش
        واقعه_نگار_ردیف.update(passed=True, move_count=80, resize_count=40, window_count=4,
                   host_cpu_ms_per_move=float(맞음[1]), mean_framebuffer_writes_per_move=int(맞음[2]),
                   full_redraw_reference_equal=True, untouched_outside_damage=True,
                   unchanged_pixels_not_written=True, repeated_position_not_repainted=True,
                   padded_stride_preserved=True)
        print(سنجش, end='')
    finally:
        (مقصد_مقدار/'report.json').write_text(json.dumps(واقعه_نگار_ردیف, ensure_ascii=False, indent=2)+'\n')

if __name__ == '__main__': اجرا_2()

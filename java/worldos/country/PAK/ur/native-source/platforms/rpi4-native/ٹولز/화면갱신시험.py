#!/usr/bin/env python3
"""اصل_کوائف کرنیل_قدر 그리기 코드를 میزبان میموری_کوائف 화면에 연결해 부분 갱신을 검증한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

عکس_ڈالنا_روٹ = Path(__file__).resolve().parents[1]

def چلائیں():
    ماخذ_فائلیں = ['시험/화면갱신.c', 'مشین/화면그림.c', 'مشین/حکم_کی_تشریح_کرنے_والا.c', 'مشین/ویجٹ.c']
    검증원문들 = ماخذ_فائلیں + ['ماخذ_فائل/화면합성.java', 'ماخذ_فائل/بورڈ.java', '../../compiler/자바도구/기계어미리번역.java']
    منزل_مقصود_قدر = عکس_ڈالنا_روٹ/'build/verification/redraw'; منزل_مقصود_قدر.mkdir(parents=True, exist_ok=True)
    لاگ_صف = {'passed': False, 'test_environment': 'host CPU, Java AOT framebuffer composition and native terminal/widgets with memory framebuffer',
          'kernel_sha256': hashlib.sha256((عکس_ڈالنا_روٹ/'build/kernel8.img').read_bytes()).hexdigest(),
          'source_sha256': {نام: hashlib.sha256((عکس_ڈالنا_روٹ/نام).read_bytes()).hexdigest() for نام in 검증원문들}}
    try:
        صنف_راہ = منزل_مقصود_قدر/'classes'; صنف_راہ.mkdir(exist_ok=True)
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(صنف_راہ),
            str(عکس_ڈالنا_روٹ/'ماخذ_فائل/화면합성.java'), str(عکس_ڈالنا_روٹ/'ماخذ_فائل/بورڈ.java')])
        برآمد_کریں_جدول = {'jdraw_prepare': 'تیار_کریں', 'jdraw_width': '너비얻기', 'jdraw_height': '높이얻기',
            'jdraw_count_low': '기록아래얻기', 'jdraw_count_high': '기록위얻기', 'jdraw_clip': 'تراشہ',
            'jdraw_clip_value': 'تراشہ_قدر', 'jdraw_begin': 'چلائیں', 'jdraw_end': 'تکمیل',
            'jdraw_pixel': 'پکسل', 'jdraw_rectangle': '사각그림', 'jdraw_pointer': 'پوائنٹر'}
        번역명령 = ['sh', str(عکس_ڈالنا_روٹ.parents[1]/'compiler/미리번역.sh'), '--entry', '화면합성.너비얻기', '-o', str(منزل_مقصود_قدر/'ڈرائنگ_قدر.c')]
        for متصل_ہوں, فعل_قدر in برآمد_کریں_جدول.items(): 번역명령.extend(['--export', متصل_ہوں+'=화면합성.'+فعل_قدر])
        subprocess.check_call(번역명령+[str(راستہ_2) for راستہ_2 in sorted(صنف_راہ.glob('*.class'))])
        حکم = ['clang', '-std=c11', '-O2', '-Wall', '-Wextra', '-Werror'] + ماخذ_فائلیں
        ڈرائنگ_منزل_مقصود = منزل_مقصود_قدر/'ڈرائنگ_قدر.o'
        subprocess.check_call(['clang', '-std=c11', '-O2', '-c', str(منزل_مقصود_قدر/'ڈرائنگ_قدر.c'), '-o', str(ڈرائنگ_منزل_مقصود)])
        subprocess.check_call(حکم+[str(ڈرائنگ_منزل_مقصود), 'build/terminal-font.S', '-o', str(منزل_مقصود_قدر/'화면갱신시험')], cwd=str(عکس_ڈالنا_روٹ))
        پیمائش = subprocess.check_output([str(منزل_مقصود_قدر/'화면갱신시험')], timeout=30).decode()
        (منزل_مقصود_قدر/'جواز_دہی_کریں.log').write_text(پیمائش)
        맞음 = re.search(r'([\d.]+) ms/move; (\d+) framebuffer writes/move', پیمائش)
        assert 맞음 and 'PASS:' in پیمائش, پیمائش
        لاگ_صف.update(passed=True, move_count=80, resize_count=40, window_count=4,
                   host_cpu_ms_per_move=float(맞음[1]), mean_framebuffer_writes_per_move=int(맞음[2]),
                   full_redraw_reference_equal=True, untouched_outside_damage=True,
                   unchanged_pixels_not_written=True, repeated_position_not_repainted=True,
                   padded_stride_preserved=True)
        print(پیمائش, end='')
    finally:
        (منزل_مقصود_قدر/'report.json').write_text(json.dumps(لاگ_صف, ensure_ascii=False, indent=2)+'\n')

if __name__ == '__main__': چلائیں()

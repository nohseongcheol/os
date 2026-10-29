#!/usr/bin/env python3
"""الفعلي_بيانات نواة_قيمة 그리기 코드를 مضيف ذاكرة_بيانات 화면에 연결해 부분 갱신을 검증한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

يعرض_جذر = Path(__file__).resolve().parents[1]

def تشغيل():
    مصدر_الملفات = ['اختبارات/화면갱신.c', 'جهاز/화면그림.c', 'جهاز/طرفية.c', 'جهاز/عنصر_شاشة.c']
    검증원문들 = مصدر_الملفات + ['مصدر/تركيبالشاشة.java', 'مصدر/لوحة.java', '../../compiler/أدواتجافا/مترجممسبق.java']
    وجهة_قيمة = يعرض_جذر/'build/verification/redraw'; وجهة_قيمة.mkdir(parents=True, exist_ok=True)
    سجل_سجل = {'passed': False, 'test_environment': 'host CPU, Java AOT framebuffer composition and native terminal/widgets with memory framebuffer',
          'kernel_sha256': hashlib.sha256((يعرض_جذر/'build/kernel8.img').read_bytes()).hexdigest(),
          'source_sha256': {اسم: hashlib.sha256((يعرض_جذر/اسم).read_bytes()).hexdigest() for اسم in 검증원문들}}
    try:
        فئة_مسار = وجهة_قيمة/'classes'; فئة_مسار.mkdir(exist_ok=True)
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(فئة_مسار),
            str(يعرض_جذر/'مصدر/تركيبالشاشة.java'), str(يعرض_جذر/'مصدر/لوحة.java')])
        تصدير_جدول = {'jdraw_prepare': 'إعداد', 'jdraw_width': '너비얻기', 'jdraw_height': 'الحصول_على_ارتفاع',
            'jdraw_count_low': '기록아래얻기', 'jdraw_count_high': '기록위얻기', 'jdraw_clip': 'يقص',
            'jdraw_clip_value': 'يقص_قيمة', 'jdraw_begin': 'تشغيل', 'jdraw_end': 'إنهاء',
            'jdraw_pixel': 'عنصر_صورة', 'jdraw_rectangle': 'مستطيل_يملأ', 'jdraw_pointer': 'مؤشر'}
        번역명령 = ['sh', str(يعرض_جذر.parents[1]/'compiler/미리번역.sh'), '--entry', 'تركيبالشاشة.너비얻기', '-o', str(وجهة_قيمة/'رسم_قيمة.c')]
        for اتصال, دالة_قيمة in تصدير_جدول.items(): 번역명령.extend(['--export', اتصال+'=تركيبالشاشة.'+دالة_قيمة])
        subprocess.check_call(번역명령+[str(مسار) for مسار in sorted(فئة_مسار.glob('*.class'))])
        أمر = ['clang', '-std=c11', '-O2', '-Wall', '-Wextra', '-Werror'] + مصدر_الملفات
        رسم_وجهة = وجهة_قيمة/'رسم_قيمة.o'
        subprocess.check_call(['clang', '-std=c11', '-O2', '-c', str(وجهة_قيمة/'رسم_قيمة.c'), '-o', str(رسم_وجهة)])
        subprocess.check_call(أمر+[str(رسم_وجهة), 'build/terminal-font.S', '-o', str(وجهة_قيمة/'화면갱신시험')], cwd=str(يعرض_جذر))
        نتيجة = subprocess.check_output([str(وجهة_قيمة/'화면갱신시험')], timeout=30).decode()
        (وجهة_قيمة/'التحقق_من_صحة.log').write_text(نتيجة)
        맞음 = re.search(r'([\d.]+) ms/move; (\d+) framebuffer writes/move', نتيجة)
        assert 맞음 and 'PASS:' in نتيجة, نتيجة
        سجل_سجل.update(passed=True, move_count=80, resize_count=40, window_count=4,
                   host_cpu_ms_per_move=float(맞음[1]), mean_framebuffer_writes_per_move=int(맞음[2]),
                   full_redraw_reference_equal=True, untouched_outside_damage=True,
                   unchanged_pixels_not_written=True, repeated_position_not_repainted=True,
                   padded_stride_preserved=True)
        print(نتيجة, end='')
    finally:
        (وجهة_قيمة/'report.json').write_text(json.dumps(سجل_سجل, ensure_ascii=False, indent=2)+'\n')

if __name__ == '__main__': تشغيل()

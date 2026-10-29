#!/usr/bin/env python3
"""ڕاستەکی_دەیتا کوورەک_نرخ 그리기 코드를 جێدەر بیرگە_دەیتا 화면에 연결해 부분 갱신을 검증한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

기준 = Path(__file__).resolve().parents[1]

def ڕادان():
    ژێدەر_فایله_کان = ['시험/화면갱신.c', 'مەکینه/화면그림.c', 'مەکینه/터미널.c', 'مەکینه/ویدجێت.c']
    검증원문들 = ژێدەر_فایله_کان + ['ژێدەر/화면합성.java', 'ژێدەر/보드.java', '../../compiler/자바도구/기계어미리번역.java']
    جێمەبەست_نرخ = 기준/'build/verification/redraw'; جێمەبەست_نرخ.mkdir(parents=True, exist_ok=True)
    تۆمار_ڕزن = {'passed': False, 'test_environment': 'host CPU, Java AOT framebuffer composition and native terminal/widgets with memory framebuffer',
          'kernel_sha256': hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),
          'source_sha256': {ناو: hashlib.sha256((기준/ناو).read_bytes()).hexdigest() for ناو in 검증원문들}}
    try:
        کلاس_گوزەر = جێمەبەست_نرخ/'classes'; کلاس_گوزەر.mkdir(exist_ok=True)
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(کلاس_گوزەر),
            str(기준/'ژێدەر/화면합성.java'), str(기준/'ژێدەر/보드.java')])
        دەرهێنان_خشتە = {'jdraw_prepare': 'ئامادە_کردن_9ce364fc', 'jdraw_width': '너비얻기', 'jdraw_height': '높이얻기',
            'jdraw_count_low': '기록아래얻기', 'jdraw_count_high': '기록위얻기', 'jdraw_clip': 'کلیپ',
            'jdraw_clip_value': 'کلیپ_نرخ', 'jdraw_begin': 'ڕادان', 'jdraw_end': 'تەواو',
            'jdraw_pixel': 'پێڵ', 'jdraw_rectangle': '사각그림', 'jdraw_pointer': 'نیشاندەر'}
        번역명령 = ['sh', str(기준.parents[1]/'compiler/미리번역.sh'), '--entry', '화면합성.너비얻기', '-o', str(جێمەبەست_نرخ/'نگار_نرخ.c')]
        for لكاندن, کردار_نرخ in دەرهێنان_خشتە.items(): 번역명령.extend(['--export', لكاندن+'=화면합성.'+کردار_نرخ])
        subprocess.check_call(번역명령+[str(گوزەر) for گوزەر in sorted(کلاس_گوزەر.glob('*.class'))])
        فەرمان = ['clang', '-std=c11', '-O2', '-Wall', '-Wextra', '-Werror'] + ژێدەر_فایله_کان
        نگار_جێمەبەست = جێمەبەست_نرخ/'نگار_نرخ.o'
        subprocess.check_call(['clang', '-std=c11', '-O2', '-c', str(جێمەبەست_نرخ/'نگار_نرخ.c'), '-o', str(نگار_جێمەبەست)])
        subprocess.check_call(فەرمان+[str(نگار_جێمەبەست), 'build/terminal-font.S', '-o', str(جێمەبەست_نرخ/'화면갱신시험')], cwd=str(기준))
        결과 = subprocess.check_output([str(جێمەبەست_نرخ/'화면갱신시험')], timeout=30).decode()
        (جێمەبەست_نرخ/'ڕەوایی.log').write_text(결과)
        맞음 = re.search(r'([\d.]+) ms/move; (\d+) framebuffer writes/move', 결과)
        assert 맞음 and 'PASS:' in 결과, 결과
        تۆمار_ڕزن.update(passed=True, move_count=80, resize_count=40, window_count=4,
                   host_cpu_ms_per_move=float(맞음[1]), mean_framebuffer_writes_per_move=int(맞음[2]),
                   full_redraw_reference_equal=True, untouched_outside_damage=True,
                   unchanged_pixels_not_written=True, repeated_position_not_repainted=True,
                   padded_stride_preserved=True)
        print(결과, end='')
    finally:
        (جێمەبەست_نرخ/'report.json').write_text(json.dumps(تۆمار_ڕزن, ensure_ascii=False, indent=2)+'\n')

if __name__ == '__main__': ڕادان()

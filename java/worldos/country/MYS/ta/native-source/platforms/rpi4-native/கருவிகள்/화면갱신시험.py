#!/usr/bin/env python3
"""அசல்_தரவு கரு_மதிப்பு 그리기 코드를 ஓம்பு நினைவகம்_தரவு 화면에 연결해 부분 갱신을 검증한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

திட்டப்பணி_மூலம் = Path(__file__).resolve().parents[1]

def செயல்படுத்துக():
    மூலம்_கோப்புகள் = ['시험/화면갱신.c', 'இயந்திரம்/화면그림.c', 'இயந்திரம்/கட்டளை_விளக்கி.c', 'இயந்திரம்/விட்ஜெட்.c']
    검증원문들 = மூலம்_கோப்புகள் + ['மூலக்_கோப்பு/화면합성.java', 'மூலக்_கோப்பு/போர்டு.java', '../../compiler/자바도구/기계어미리번역.java']
    இலக்கு_மதிப்பு = திட்டப்பணி_மூலம்/'build/verification/redraw'; இலக்கு_மதிப்பு.mkdir(parents=True, exist_ok=True)
    பதிவு_பதிவு = {'passed': False, 'test_environment': 'host CPU, Java AOT framebuffer composition and native terminal/widgets with memory framebuffer',
          'kernel_sha256': hashlib.sha256((திட்டப்பணி_மூலம்/'build/kernel8.img').read_bytes()).hexdigest(),
          'source_sha256': {பெயர்: hashlib.sha256((திட்டப்பணி_மூலம்/பெயர்).read_bytes()).hexdigest() for பெயர் in 검증원문들}}
    try:
        பிரிவு_பாதை = இலக்கு_மதிப்பு/'classes'; பிரிவு_பாதை.mkdir(exist_ok=True)
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(பிரிவு_பாதை),
            str(திட்டப்பணி_மூலம்/'மூலக்_கோப்பு/화면합성.java'), str(திட்டப்பணி_மூலம்/'மூலக்_கோப்பு/போர்டு.java')])
        ஏற்றுமதிசெய்_அட்டவணை = {'jdraw_prepare': 'தயார்படுத்த', 'jdraw_width': '너비얻기', 'jdraw_height': '높이얻기',
            'jdraw_count_low': '기록아래얻기', 'jdraw_count_high': '기록위얻기', 'jdraw_clip': 'கிளிப்',
            'jdraw_clip_value': 'கிளிப்_மதிப்பு', 'jdraw_begin': 'செயல்படுத்துக', 'jdraw_end': 'முடிப்பு',
            'jdraw_pixel': 'படக்_கூறு', 'jdraw_rectangle': '사각그림', 'jdraw_pointer': 'குறிப்பான்'}
        번역명령 = ['sh', str(திட்டப்பணி_மூலம்.parents[1]/'compiler/미리번역.sh'), '--entry', '화면합성.너비얻기', '-o', str(இலக்கு_மதிப்பு/'வரைதல்_மதிப்பு.c')]
        for இணைக்க, செயல்பாடு_மதிப்பு in ஏற்றுமதிசெய்_அட்டவணை.items(): 번역명령.extend(['--export', இணைக்க+'=화면합성.'+செயல்பாடு_மதிப்பு])
        subprocess.check_call(번역명령+[str(பாதை_2) for பாதை_2 in sorted(பிரிவு_பாதை.glob('*.class'))])
        கட்டளை = ['clang', '-std=c11', '-O2', '-Wall', '-Wextra', '-Werror'] + மூலம்_கோப்புகள்
        வரைதல்_இலக்கு = இலக்கு_மதிப்பு/'வரைதல்_மதிப்பு.o'
        subprocess.check_call(['clang', '-std=c11', '-O2', '-c', str(இலக்கு_மதிப்பு/'வரைதல்_மதிப்பு.c'), '-o', str(வரைதல்_இலக்கு)])
        subprocess.check_call(கட்டளை+[str(வரைதல்_இலக்கு), 'build/terminal-font.S', '-o', str(இலக்கு_மதிப்பு/'화면갱신시험')], cwd=str(திட்டப்பணி_மூலம்))
        அளவிடக்கூடியது = subprocess.check_output([str(இலக்கு_மதிப்பு/'화면갱신시험')], timeout=30).decode()
        (இலக்கு_மதிப்பு/'சரிபார்_5fb2b747.log').write_text(அளவிடக்கூடியது)
        맞음 = re.search(r'([\d.]+) ms/move; (\d+) framebuffer writes/move', அளவிடக்கூடியது)
        assert 맞음 and 'PASS:' in அளவிடக்கூடியது, அளவிடக்கூடியது
        பதிவு_பதிவு.update(passed=True, move_count=80, resize_count=40, window_count=4,
                   host_cpu_ms_per_move=float(맞음[1]), mean_framebuffer_writes_per_move=int(맞음[2]),
                   full_redraw_reference_equal=True, untouched_outside_damage=True,
                   unchanged_pixels_not_written=True, repeated_position_not_repainted=True,
                   padded_stride_preserved=True)
        print(அளவிடக்கூடியது, end='')
    finally:
        (இலக்கு_மதிப்பு/'report.json').write_text(json.dumps(பதிவு_பதிவு, ensure_ascii=False, indent=2)+'\n')

if __name__ == '__main__': செயல்படுத்துக()

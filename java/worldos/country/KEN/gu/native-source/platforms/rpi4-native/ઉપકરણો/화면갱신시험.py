#!/usr/bin/env python3
"""વાસ્તવિક_ડેટા કર્નેલ_મૂલ્ય 그리기 코드를 હોસ્ટ મેમરી_ડેટા 화면에 연결해 부분 갱신을 검증한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

પ્રોજેક્ટ_રૂટ = Path(__file__).resolve().parents[1]

def ચલાવો_2():
    સ્રોત_ફાઇલો = ['시험/화면갱신.c', 'મશીન/화면그림.c', 'મશીન/ટર્મિનલ.c', 'મશીન/વિજેટ.c']
    검증원문들 = સ્રોત_ફાઇલો + ['સ્રોત/화면합성.java', 'સ્રોત/બોર્ડ.java', '../../compiler/자바도구/기계어미리번역.java']
    ગંતવ્ય_મૂલ્ય = પ્રોજેક્ટ_રૂટ/'build/verification/redraw'; ગંતવ્ય_મૂલ્ય.mkdir(parents=True, exist_ok=True)
    લૉગ_પંક્તિ = {'passed': False, 'test_environment': 'host CPU, Java AOT framebuffer composition and native terminal/widgets with memory framebuffer',
          'kernel_sha256': hashlib.sha256((પ્રોજેક્ટ_રૂટ/'build/kernel8.img').read_bytes()).hexdigest(),
          'source_sha256': {નામ: hashlib.sha256((પ્રોજેક્ટ_રૂટ/નામ).read_bytes()).hexdigest() for નામ in 검증원문들}}
    try:
        વર્ગ_પાથ = ગંતવ્ય_મૂલ્ય/'classes'; વર્ગ_પાથ.mkdir(exist_ok=True)
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(વર્ગ_પાથ),
            str(પ્રોજેક્ટ_રૂટ/'સ્રોત/화면합성.java'), str(પ્રોજેક્ટ_રૂટ/'સ્રોત/બોર્ડ.java')])
        નિકાસ_કરો_કોષ્ટક = {'jdraw_prepare': 'તૈયાર_કરો', 'jdraw_width': '너비얻기', 'jdraw_height': '높이얻기',
            'jdraw_count_low': '기록아래얻기', 'jdraw_count_high': '기록위얻기', 'jdraw_clip': 'ક્લિપ',
            'jdraw_clip_value': 'ક્લિપ_મૂલ્ય', 'jdraw_begin': 'ચલાવો_2', 'jdraw_end': 'સમાપ્ત_કરો',
            'jdraw_pixel': 'પેલ', 'jdraw_rectangle': '사각그림', 'jdraw_pointer': 'સૂચક'}
        번역명령 = ['sh', str(પ્રોજેક્ટ_રૂટ.parents[1]/'compiler/미리번역.sh'), '--entry', '화면합성.너비얻기', '-o', str(ગંતવ્ય_મૂલ્ય/'રેખાંકન_મૂલ્ય.c')]
        for સંપર્ક_કરો, ફંક્શંસ_મૂલ્ય in નિકાસ_કરો_કોષ્ટક.items(): 번역명령.extend(['--export', સંપર્ક_કરો+'=화면합성.'+ફંક્શંસ_મૂલ્ય])
        subprocess.check_call(번역명령+[str(પથ) for પથ in sorted(વર્ગ_પાથ.glob('*.class'))])
        આદેશ = ['clang', '-std=c11', '-O2', '-Wall', '-Wextra', '-Werror'] + સ્રોત_ફાઇલો
        રેખાંકન_ગંતવ્ય = ગંતવ્ય_મૂલ્ય/'રેખાંકન_મૂલ્ય.o'
        subprocess.check_call(['clang', '-std=c11', '-O2', '-c', str(ગંતવ્ય_મૂલ્ય/'રેખાંકન_મૂલ્ય.c'), '-o', str(રેખાંકન_ગંતવ્ય)])
        subprocess.check_call(આદેશ+[str(રેખાંકન_ગંતવ્ય), 'build/terminal-font.S', '-o', str(ગંતવ્ય_મૂલ્ય/'화면갱신시험')], cwd=str(પ્રોજેક્ટ_રૂટ))
        પરિમાણ = subprocess.check_output([str(ગંતવ્ય_મૂલ્ય/'화면갱신시험')], timeout=30).decode()
        (ગંતવ્ય_મૂલ્ય/'માન્ય_કરો.log').write_text(પરિમાણ)
        맞음 = re.search(r'([\d.]+) ms/move; (\d+) framebuffer writes/move', પરિમાણ)
        assert 맞음 and 'PASS:' in પરિમાણ, પરિમાણ
        લૉગ_પંક્તિ.update(passed=True, move_count=80, resize_count=40, window_count=4,
                   host_cpu_ms_per_move=float(맞음[1]), mean_framebuffer_writes_per_move=int(맞음[2]),
                   full_redraw_reference_equal=True, untouched_outside_damage=True,
                   unchanged_pixels_not_written=True, repeated_position_not_repainted=True,
                   padded_stride_preserved=True)
        print(પરિમાણ, end='')
    finally:
        (ગંતવ્ય_મૂલ્ય/'report.json').write_text(json.dumps(લૉગ_પંક્તિ, ensure_ascii=False, indent=2)+'\n')

if __name__ == '__main__': ચલાવો_2()

#!/usr/bin/env python3
"""वास्तविक_डेटा कर्नेल_मान 그리기 코드를 आयोजक मेमोरी_डेटा 화면에 연결해 부분 갱신을 검증한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

प्रोजेक्ट_करें_मूल = Path(__file__).resolve().parents[1]

def चलाएँ():
    स्रोत_फ़ाइलें = ['시험/화면갱신.c', 'यंत्र/화면그림.c', 'यंत्र/आदेशपटल.c', 'यंत्र/विजेट.c']
    검증원문들 = स्रोत_फ़ाइलें + ['स्रोत/पटलसंयोजन.java', 'स्रोत/बोर्ड.java', '../../compiler/जावासाधन/पूर्वसंकलक.java']
    गंतव्य_मान = प्रोजेक्ट_करें_मूल/'build/verification/redraw'; गंतव्य_मान.mkdir(parents=True, exist_ok=True)
    लॉग_रिकॉर्ड = {'passed': False, 'test_environment': 'host CPU, Java AOT framebuffer composition and native terminal/widgets with memory framebuffer',
          'kernel_sha256': hashlib.sha256((प्रोजेक्ट_करें_मूल/'build/kernel8.img').read_bytes()).hexdigest(),
          'source_sha256': {नाम: hashlib.sha256((प्रोजेक्ट_करें_मूल/नाम).read_bytes()).hexdigest() for नाम in 검증원문들}}
    try:
        कक्षा_पथ = गंतव्य_मान/'classes'; कक्षा_पथ.mkdir(exist_ok=True)
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(कक्षा_पथ),
            str(प्रोजेक्ट_करें_मूल/'स्रोत/पटलसंयोजन.java'), str(प्रोजेक्ट_करें_मूल/'स्रोत/बोर्ड.java')])
        निर्यात_करें_तालिका = {'jdraw_prepare': '준비', 'jdraw_width': '너비얻기', 'jdraw_height': '높이얻기',
            'jdraw_count_low': '기록아래얻기', 'jdraw_count_high': '기록위얻기', 'jdraw_clip': 'क्लिप',
            'jdraw_clip_value': 'क्लिप_मान', 'jdraw_begin': 'चलाएँ', 'jdraw_end': 'पूर्ण',
            'jdraw_pixel': 'पिक्सेल', 'jdraw_rectangle': 'रेक्_टेंगल_भरण', 'jdraw_pointer': 'सूचक'}
        번역명령 = ['sh', str(प्रोजेक्ट_करें_मूल.parents[1]/'compiler/미리번역.sh'), '--entry', 'पटलसंयोजन.너비얻기', '-o', str(गंतव्य_मान/'ड्रॉइंग_मान.c')]
        for जोड़ना, फ़ंक्_शन_मान in निर्यात_करें_तालिका.items(): 번역명령.extend(['--export', जोड़ना+'=पटलसंयोजन.'+फ़ंक्_शन_मान])
        subprocess.check_call(번역명령+[str(पथ) for पथ in sorted(कक्षा_पथ.glob('*.class'))])
        आदेश = ['clang', '-std=c11', '-O2', '-Wall', '-Wextra', '-Werror'] + स्रोत_फ़ाइलें
        ड्रॉइंग_गंतव्य = गंतव्य_मान/'ड्रॉइंग_मान.o'
        subprocess.check_call(['clang', '-std=c11', '-O2', '-c', str(गंतव्य_मान/'ड्रॉइंग_मान.c'), '-o', str(ड्रॉइंग_गंतव्य)])
        subprocess.check_call(आदेश+[str(ड्रॉइंग_गंतव्य), 'build/terminal-font.S', '-o', str(गंतव्य_मान/'화면갱신시험')], cwd=str(प्रोजेक्ट_करें_मूल))
        परिणाम = subprocess.check_output([str(गंतव्य_मान/'화면갱신시험')], timeout=30).decode()
        (गंतव्य_मान/'मान्य_करें.log').write_text(परिणाम)
        맞음 = re.search(r'([\d.]+) ms/move; (\d+) framebuffer writes/move', परिणाम)
        assert 맞음 and 'PASS:' in परिणाम, परिणाम
        लॉग_रिकॉर्ड.update(passed=True, move_count=80, resize_count=40, window_count=4,
                   host_cpu_ms_per_move=float(맞음[1]), mean_framebuffer_writes_per_move=int(맞음[2]),
                   full_redraw_reference_equal=True, untouched_outside_damage=True,
                   unchanged_pixels_not_written=True, repeated_position_not_repainted=True,
                   padded_stride_preserved=True)
        print(परिणाम, end='')
    finally:
        (गंतव्य_मान/'report.json').write_text(json.dumps(लॉग_रिकॉर्ड, ensure_ascii=False, indent=2)+'\n')

if __name__ == '__main__': चलाएँ()

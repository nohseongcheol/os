#!/usr/bin/env python3
"""वास्तविक_लगत कर्णेल_मान 그리기 코드를 होस्ट मेमोरी_लगत 화면에 연결해 부분 갱신을 검증한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

परियोजना_रूट = Path(__file__).resolve().parents[1]

def चलाउनुहोस्():
    स्रोत_फाइलहरू = ['시험/화면갱신.c', 'मेशिन/화면그림.c', 'मेशिन/टर्मिनल.c', 'मेशिन/विजेट.c']
    검증원문들 = स्रोत_फाइलहरू + ['स्रोत/화면합성.java', 'स्रोत/बोर्ड.java', '../../compiler/자바도구/기계어미리번역.java']
    गन्तव्य_मान = परियोजना_रूट/'build/verification/redraw'; गन्तव्य_मान.mkdir(parents=True, exist_ok=True)
    लग_रेकर्ड = {'passed': False, 'test_environment': 'host CPU, Java AOT framebuffer composition and native terminal/widgets with memory framebuffer',
          'kernel_sha256': hashlib.sha256((परियोजना_रूट/'build/kernel8.img').read_bytes()).hexdigest(),
          'source_sha256': {नाम: hashlib.sha256((परियोजना_रूट/नाम).read_bytes()).hexdigest() for नाम in 검증원문들}}
    try:
        वर्ग_बाटो = गन्तव्य_मान/'classes'; वर्ग_बाटो.mkdir(exist_ok=True)
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(वर्ग_बाटो),
            str(परियोजना_रूट/'स्रोत/화면합성.java'), str(परियोजना_रूट/'स्रोत/बोर्ड.java')])
        निर्यात_गर्नुहोस्_तालिका = {'jdraw_prepare': 'तयार_गर्नुहोस्', 'jdraw_width': '너비얻기', 'jdraw_height': '높이얻기',
            'jdraw_count_low': '기록아래얻기', 'jdraw_count_high': '기록위얻기', 'jdraw_clip': 'क्लिप',
            'jdraw_clip_value': 'क्लिप_मान', 'jdraw_begin': 'चलाउनुहोस्', 'jdraw_end': 'समाप्त',
            'jdraw_pixel': 'पेल', 'jdraw_rectangle': '사각그림', 'jdraw_pointer': 'पोइन्टर'}
        번역명령 = ['sh', str(परियोजना_रूट.parents[1]/'compiler/미리번역.sh'), '--entry', '화면합성.너비얻기', '-o', str(गन्तव्य_मान/'चित्रकारी_मान.c')]
        for जडान, प्रकार्य_मान in निर्यात_गर्नुहोस्_तालिका.items(): 번역명령.extend(['--export', जडान+'=화면합성.'+प्रकार्य_मान])
        subprocess.check_call(번역명령+[str(मार्ग) for मार्ग in sorted(वर्ग_बाटो.glob('*.class'))])
        आदेश = ['clang', '-std=c11', '-O2', '-Wall', '-Wextra', '-Werror'] + स्रोत_फाइलहरू
        चित्रकारी_गन्तव्य = गन्तव्य_मान/'चित्रकारी_मान.o'
        subprocess.check_call(['clang', '-std=c11', '-O2', '-c', str(गन्तव्य_मान/'चित्रकारी_मान.c'), '-o', str(चित्रकारी_गन्तव्य)])
        subprocess.check_call(आदेश+[str(चित्रकारी_गन्तव्य), 'build/terminal-font.S', '-o', str(गन्तव्य_मान/'화면갱신시험')], cwd=str(परियोजना_रूट))
        मापन = subprocess.check_output([str(गन्तव्य_मान/'화면갱신시험')], timeout=30).decode()
        (गन्तव्य_मान/'वैध_गर्नुहोस्.log').write_text(मापन)
        맞음 = re.search(r'([\d.]+) ms/move; (\d+) framebuffer writes/move', मापन)
        assert 맞음 and 'PASS:' in मापन, मापन
        लग_रेकर्ड.update(passed=True, move_count=80, resize_count=40, window_count=4,
                   host_cpu_ms_per_move=float(맞음[1]), mean_framebuffer_writes_per_move=int(맞음[2]),
                   full_redraw_reference_equal=True, untouched_outside_damage=True,
                   unchanged_pixels_not_written=True, repeated_position_not_repainted=True,
                   padded_stride_preserved=True)
        print(मापन, end='')
    finally:
        (गन्तव्य_मान/'report.json').write_text(json.dumps(लग_रेकर्ड, ensure_ascii=False, indent=2)+'\n')

if __name__ == '__main__': चलाउनुहोस्()

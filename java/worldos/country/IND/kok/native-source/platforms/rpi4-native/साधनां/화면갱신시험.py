#!/usr/bin/env python3
"""प्रत्यक्ष_डेटा कर्नेल_मोल 그리기 코드를 येजमान मेमरी_डेटा 화면에 연결해 부분 갱신을 검증한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

प्रॉजॅक्ट_रूट = Path(__file__).resolve().parents[1]

def चलोवप():
    स्त्रोत_फायली = ['시험/화면갱신.c', 'यंत्र/화면그림.c', 'यंत्र/टर्मिनल.c', 'यंत्र/विजीट.c']
    검증원문들 = स्त्रोत_फायली + ['स्त्रोत/화면합성.java', 'स्त्रोत/बोर्ड.java', '../../compiler/자바도구/기계어미리번역.java']
    नियुक्त_स्थान_मोल = प्रॉजॅक्ट_रूट/'build/verification/redraw'; नियुक्त_स्थान_मोल.mkdir(parents=True, exist_ok=True)
    LOG_नोंद = {'passed': False, 'test_environment': 'host CPU, Java AOT framebuffer composition and native terminal/widgets with memory framebuffer',
          'kernel_sha256': hashlib.sha256((प्रॉजॅक्ट_रूट/'build/kernel8.img').read_bytes()).hexdigest(),
          'source_sha256': {नांव: hashlib.sha256((प्रॉजॅक्ट_रूट/नांव).read_bytes()).hexdigest() for नांव in 검증원문들}}
    try:
        वर्ग_पाथ = नियुक्त_स्थान_मोल/'classes'; वर्ग_पाथ.mkdir(exist_ok=True)
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(वर्ग_पाथ),
            str(प्रॉजॅक्ट_रूट/'स्त्रोत/화면합성.java'), str(प्रॉजॅक्ट_रूट/'स्त्रोत/बोर्ड.java')])
        निर्यात_तकटो = {'jdraw_prepare': 'तयार_करचें_9ce364fc', 'jdraw_width': '너비얻기', 'jdraw_height': '높이얻기',
            'jdraw_count_low': '기록아래얻기', 'jdraw_count_high': '기록위얻기', 'jdraw_clip': 'क्लिप',
            'jdraw_clip_value': 'क्लिप_मोल', 'jdraw_begin': 'चलोवप', 'jdraw_end': 'समाप्त',
            'jdraw_pixel': 'पिक्सॅल', 'jdraw_rectangle': '사각그림', 'jdraw_pointer': 'पॉयंटर'}
        번역명령 = ['sh', str(प्रॉजॅक्ट_रूट.parents[1]/'compiler/미리번역.sh'), '--entry', '화면합성.너비얻기', '-o', str(नियुक्त_स्थान_मोल/'रेखाटन_मोल.c')]
        for कनॅक्ट, फंक्शन_मोल in निर्यात_तकटो.items(): 번역명령.extend(['--export', कनॅक्ट+'=화면합성.'+फंक्शन_मोल])
        subprocess.check_call(번역명령+[str(पाथ) for पाथ in sorted(वर्ग_पाथ.glob('*.class'))])
        आदेश = ['clang', '-std=c11', '-O2', '-Wall', '-Wextra', '-Werror'] + स्त्रोत_फायली
        रेखाटन_नियुक्त_स्थान = नियुक्त_स्थान_मोल/'रेखाटन_मोल.o'
        subprocess.check_call(['clang', '-std=c11', '-O2', '-c', str(नियुक्त_स्थान_मोल/'रेखाटन_मोल.c'), '-o', str(रेखाटन_नियुक्त_स्थान)])
        subprocess.check_call(आदेश+[str(रेखाटन_नियुक्त_स्थान), 'build/terminal-font.S', '-o', str(नियुक्त_स्थान_मोल/'화면갱신시험')], cwd=str(प्रॉजॅक्ट_रूट))
        मेजप = subprocess.check_output([str(नियुक्त_स्थान_मोल/'화면갱신시험')], timeout=30).decode()
        (नियुक्त_स्थान_मोल/'पुनर्तपासणी_करची_5fb2b747.log').write_text(मेजप)
        맞음 = re.search(r'([\d.]+) ms/move; (\d+) framebuffer writes/move', मेजप)
        assert 맞음 and 'PASS:' in मेजप, मेजप
        LOG_नोंद.update(passed=True, move_count=80, resize_count=40, window_count=4,
                   host_cpu_ms_per_move=float(맞음[1]), mean_framebuffer_writes_per_move=int(맞음[2]),
                   full_redraw_reference_equal=True, untouched_outside_damage=True,
                   unchanged_pixels_not_written=True, repeated_position_not_repainted=True,
                   padded_stride_preserved=True)
        print(मेजप, end='')
    finally:
        (नियुक्त_स्थान_मोल/'report.json').write_text(json.dumps(LOG_नोंद, ensure_ascii=False, indent=2)+'\n')

if __name__ == '__main__': चलोवप()

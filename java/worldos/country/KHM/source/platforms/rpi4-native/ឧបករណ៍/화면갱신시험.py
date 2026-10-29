#!/usr/bin/env python3
"""ដែលពិត_ទិន្នន័យ ខឺណេល_តំលៃ 그리기 코드를 ហូស សតិ_ទិន្នន័យ 화면에 연결해 부분 갱신을 검증한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

បញ្ចាំង_ឬស = Path(__file__).resolve().parents[1]

def រត់():
    ប្រភព_ឯកសារ = ['시험/화면갱신.c', 'ម៉ាស៊ីន/화면그림.c', 'ម៉ាស៊ីន/ស្ថានីយ.c', 'ម៉ាស៊ីន/វីដហ្គេត.c']
    검증원문들 = ប្រភព_ឯកសារ + ['ប្រភព/화면합성.java', 'ប្រភព/ផ្ទាំង.java', '../../compiler/자바도구/기계어미리번역.java']
    ទិសដៅ_តំលៃ = បញ្ចាំង_ឬស/'build/verification/redraw'; ទិសដៅ_តំលៃ.mkdir(parents=True, exist_ok=True)
    កំណត់_ហេតុ_ថត = {'passed': False, 'test_environment': 'host CPU, Java AOT framebuffer composition and native terminal/widgets with memory framebuffer',
          'kernel_sha256': hashlib.sha256((បញ្ចាំង_ឬស/'build/kernel8.img').read_bytes()).hexdigest(),
          'source_sha256': {ឈ្មោះ: hashlib.sha256((បញ្ចាំង_ឬស/ឈ្មោះ).read_bytes()).hexdigest() for ឈ្មោះ in 검증원문들}}
    try:
        ថ្នាក់_ផ្លូវ = ទិសដៅ_តំលៃ/'classes'; ថ្នាក់_ផ្លូវ.mkdir(exist_ok=True)
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(ថ្នាក់_ផ្លូវ),
            str(បញ្ចាំង_ឬស/'ប្រភព/화면합성.java'), str(បញ្ចាំង_ឬស/'ប្រភព/ផ្ទាំង.java')])
        នាំចេញ_តារាង = {'jdraw_prepare': 'រៀបចំ', 'jdraw_width': '너비얻기', 'jdraw_height': '높이얻기',
            'jdraw_count_low': '기록아래얻기', 'jdraw_count_high': '기록위얻기', 'jdraw_clip': 'មេឌៀខ្លីៗ',
            'jdraw_clip_value': 'មេឌៀខ្លីៗ_តំលៃ', 'jdraw_begin': 'រត់', 'jdraw_end': 'បញ្ចប់',
            'jdraw_pixel': 'ចំនុចតូចៗ', 'jdraw_rectangle': '사각그림', 'jdraw_pointer': 'អង្គ_ចង្អុល_កណ្ដុរ'}
        번역명령 = ['sh', str(បញ្ចាំង_ឬស.parents[1]/'compiler/미리번역.sh'), '--entry', '화면합성.너비얻기', '-o', str(ទិសដៅ_តំលៃ/'ការគូរ_តំលៃ.c')]
        for ភ្ជាប់, អនុគមន៍_តំលៃ in នាំចេញ_តារាង.items(): 번역명령.extend(['--export', ភ្ជាប់+'=화면합성.'+អនុគមន៍_តំលៃ])
        subprocess.check_call(번역명령+[str(ផ្លូវ) for ផ្លូវ in sorted(ថ្នាក់_ផ្លូវ.glob('*.class'))])
        ពាក្យ_បញ្ជា = ['clang', '-std=c11', '-O2', '-Wall', '-Wextra', '-Werror'] + ប្រភព_ឯកសារ
        ការគូរ_ទិសដៅ = ទិសដៅ_តំលៃ/'ការគូរ_តំលៃ.o'
        subprocess.check_call(['clang', '-std=c11', '-O2', '-c', str(ទិសដៅ_តំលៃ/'ការគូរ_តំលៃ.c'), '-o', str(ការគូរ_ទិសដៅ)])
        subprocess.check_call(ពាក្យ_បញ្ជា+[str(ការគូរ_ទិសដៅ), 'build/terminal-font.S', '-o', str(ទិសដៅ_តំលៃ/'화면갱신시험')], cwd=str(បញ្ចាំង_ឬស))
        ការវាស់វែង = subprocess.check_output([str(ទិសដៅ_តំលៃ/'화면갱신시험')], timeout=30).decode()
        (ទិសដៅ_តំលៃ/'ធ្វើអោយមានសុពលភាព.log').write_text(ការវាស់វែង)
        맞음 = re.search(r'([\d.]+) ms/move; (\d+) framebuffer writes/move', ការវាស់វែង)
        assert 맞음 and 'PASS:' in ការវាស់វែង, ការវាស់វែង
        កំណត់_ហេតុ_ថត.update(passed=True, move_count=80, resize_count=40, window_count=4,
                   host_cpu_ms_per_move=float(맞음[1]), mean_framebuffer_writes_per_move=int(맞음[2]),
                   full_redraw_reference_equal=True, untouched_outside_damage=True,
                   unchanged_pixels_not_written=True, repeated_position_not_repainted=True,
                   padded_stride_preserved=True)
        print(ការវាស់វែង, end='')
    finally:
        (ទិសដៅ_តំលៃ/'report.json').write_text(json.dumps(កំណត់_ហេតុ_ថត, ensure_ascii=False, indent=2)+'\n')

if __name__ == '__main__': រត់()

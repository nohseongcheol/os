#!/usr/bin/env python3
"""ପ୍ରକୃତ_ଡାଟା କେନ୍ଦ୍ରିକ_ମୂଲ୍ୟ 그리기 코드를 ଆୟୋଜକ ମୋମରୀ_ଡାଟା 화면에 연결해 부분 갱신을 검증한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ = Path(__file__).resolve().parents[1]

def ଚଳାନ୍ତୁ():
    ଉତ୍ସ_ଫାଇଲ୍_ଗୁଡିକ = ['시험/화면갱신.c', 'ମେସିନ୍/화면그림.c', 'ମେସିନ୍/ଟର୍ମିନାଲ.c', 'ମେସିନ୍/ୱିଜାର୍ଡ୍.c']
    검증원문들 = ଉତ୍ସ_ଫାଇଲ୍_ଗୁଡିକ + ['ଉତ୍ସ/화면합성.java', 'ଉତ୍ସ/ବୋର୍ଡ୍.java', '../../compiler/자바도구/기계어미리번역.java']
    ଲକ୍ଷସ୍ଥଳ_ମୂଲ୍ୟ = ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍/'build/verification/redraw'; ଲକ୍ଷସ୍ଥଳ_ମୂଲ୍ୟ.mkdir(parents=True, exist_ok=True)
    ଲଗ୍_ଧାଡ଼ି = {'passed': False, 'test_environment': 'host CPU, Java AOT framebuffer composition and native terminal/widgets with memory framebuffer',
          'kernel_sha256': hashlib.sha256((ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍/'build/kernel8.img').read_bytes()).hexdigest(),
          'source_sha256': {ନାମ: hashlib.sha256((ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍/ନାମ).read_bytes()).hexdigest() for ନାମ in 검증원문들}}
    try:
        ଶ୍ରେଣୀ_ପଥ = ଲକ୍ଷସ୍ଥଳ_ମୂଲ୍ୟ/'classes'; ଶ୍ରେଣୀ_ପଥ.mkdir(exist_ok=True)
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(ଶ୍ରେଣୀ_ପଥ),
            str(ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍/'ଉତ୍ସ/화면합성.java'), str(ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍/'ଉତ୍ସ/ବୋର୍ଡ୍.java')])
        ରପ୍ତାନି_କରନ୍ତୁ_ସାରଣୀ = {'jdraw_prepare': 'ପ୍ରସ୍ତୁତ', 'jdraw_width': '너비얻기', 'jdraw_height': '높이얻기',
            'jdraw_count_low': '기록아래얻기', 'jdraw_count_high': '기록위얻기', 'jdraw_clip': 'କ୍ଲିପ୍',
            'jdraw_clip_value': 'କ୍ଲିପ୍_ମୂଲ୍ୟ', 'jdraw_begin': 'ଚଳାନ୍ତୁ', 'jdraw_end': 'ସମାପ୍ତ',
            'jdraw_pixel': 'ପିକ୍ସେଲ୍', 'jdraw_rectangle': '사각그림', 'jdraw_pointer': 'ପଏଣ୍ଟର୍'}
        번역명령 = ['sh', str(ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍.parents[1]/'compiler/미리번역.sh'), '--entry', '화면합성.너비얻기', '-o', str(ଲକ୍ଷସ୍ଥଳ_ମୂଲ୍ୟ/'ଅଙ୍କନ_ମୂଲ୍ୟ.c')]
        for ସଂଯୋଗ_କରନ୍ତୁ, Excel_ଟେବଲ୍_ମୂଲ୍ୟ in ରପ୍ତାନି_କରନ୍ତୁ_ସାରଣୀ.items(): 번역명령.extend(['--export', ସଂଯୋଗ_କରନ୍ତୁ+'=화면합성.'+Excel_ଟେବଲ୍_ମୂଲ୍ୟ])
        subprocess.check_call(번역명령+[str(ପଥ) for ପଥ in sorted(ଶ୍ରେଣୀ_ପଥ.glob('*.class'))])
        ନିର୍ଦ୍ଦେଶ = ['clang', '-std=c11', '-O2', '-Wall', '-Wextra', '-Werror'] + ଉତ୍ସ_ଫାଇଲ୍_ଗୁଡିକ
        ଅଙ୍କନ_ଲକ୍ଷସ୍ଥଳ = ଲକ୍ଷସ୍ଥଳ_ମୂଲ୍ୟ/'ଅଙ୍କନ_ମୂଲ୍ୟ.o'
        subprocess.check_call(['clang', '-std=c11', '-O2', '-c', str(ଲକ୍ଷସ୍ଥଳ_ମୂଲ୍ୟ/'ଅଙ୍କନ_ମୂଲ୍ୟ.c'), '-o', str(ଅଙ୍କନ_ଲକ୍ଷସ୍ଥଳ)])
        subprocess.check_call(ନିର୍ଦ୍ଦେଶ+[str(ଅଙ୍କନ_ଲକ୍ଷସ୍ଥଳ), 'build/terminal-font.S', '-o', str(ଲକ୍ଷସ୍ଥଳ_ମୂଲ୍ୟ/'화면갱신시험')], cwd=str(ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍))
        ମାପ = subprocess.check_output([str(ଲକ୍ଷସ୍ଥଳ_ମୂଲ୍ୟ/'화면갱신시험')], timeout=30).decode()
        (ଲକ୍ଷସ୍ଥଳ_ମୂଲ୍ୟ/'ବୈଧକରଣ.log').write_text(ମାପ)
        맞음 = re.search(r'([\d.]+) ms/move; (\d+) framebuffer writes/move', ମାପ)
        assert 맞음 and 'PASS:' in ମାପ, ମାପ
        ଲଗ୍_ଧାଡ଼ି.update(passed=True, move_count=80, resize_count=40, window_count=4,
                   host_cpu_ms_per_move=float(맞음[1]), mean_framebuffer_writes_per_move=int(맞음[2]),
                   full_redraw_reference_equal=True, untouched_outside_damage=True,
                   unchanged_pixels_not_written=True, repeated_position_not_repainted=True,
                   padded_stride_preserved=True)
        print(ମାପ, end='')
    finally:
        (ଲକ୍ଷସ୍ଥଳ_ମୂଲ୍ୟ/'report.json').write_text(json.dumps(ଲଗ୍_ଧାଡ଼ି, ensure_ascii=False, indent=2)+'\n')

if __name__ == '__main__': ଚଳାନ୍ତୁ()

#!/usr/bin/env python3
"""තථ්_ය_දත්ත කර්නලය_අගය 그리기 코드를 ධාරකය මතකය_දත්ත 화면에 연결해 부분 갱신을 검증한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

기준 = Path(__file__).resolve().parents[1]

def ක්_රියාත්මක_කරන්න_2():
    මූලය_ගොනු = ['시험/화면갱신.c', 'යන්ත්_රය/화면그림.c', 'යන්ත්_රය/අග්_රය.c', 'යන්ත්_රය/විජෙට්ටුව.c']
    검증원문들 = මූලය_ගොනු + ['මූලය/화면합성.java', 'මූලය/보드.java', '../../compiler/자바도구/기계어미리번역.java']
    ගමනාන්තය_අගය = 기준/'build/verification/redraw'; ගමනාන්තය_අගය.mkdir(parents=True, exist_ok=True)
    ලොගය_පේළිය = {'passed': False, 'test_environment': 'host CPU, Java AOT framebuffer composition and native terminal/widgets with memory framebuffer',
          'kernel_sha256': hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),
          'source_sha256': {නම: hashlib.sha256((기준/නම).read_bytes()).hexdigest() for නම in 검증원문들}}
    try:
        පන්තිය_පෙත = ගමනාන්තය_අගය/'classes'; පන්තිය_පෙත.mkdir(exist_ok=True)
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(පන්තිය_පෙත),
            str(기준/'මූලය/화면합성.java'), str(기준/'මූලය/보드.java')])
        නිර්යාත_කරන්න_වගුව = {'jdraw_prepare': 'පිළියෙල_කරන්න', 'jdraw_width': '너비얻기', 'jdraw_height': '높이얻기',
            'jdraw_count_low': '기록아래얻기', 'jdraw_count_high': '기록위얻기', 'jdraw_clip': 'පසුර',
            'jdraw_clip_value': 'පසුර_අගය', 'jdraw_begin': 'ක්_රියාත්මක_කරන්න_2', 'jdraw_end': 'ෆිනිෂ්',
            'jdraw_pixel': 'පික්සලය', 'jdraw_rectangle': '사각그림', 'jdraw_pointer': 'පොයින්ටරය'}
        번역명령 = ['sh', str(기준.parents[1]/'compiler/미리번역.sh'), '--entry', '화면합성.너비얻기', '-o', str(ගමනාන්තය_අගය/'චිත්_රය_අගය.c')]
        for සම්බන්ද_වන්න, ශ්_රිතය_අගය in නිර්යාත_කරන්න_වගුව.items(): 번역명령.extend(['--export', සම්බන්ද_වන්න+'=화면합성.'+ශ්_රිතය_අගය])
        subprocess.check_call(번역명령+[str(මාර්_ගය) for මාර්_ගය in sorted(පන්තිය_පෙත.glob('*.class'))])
        විධානය = ['clang', '-std=c11', '-O2', '-Wall', '-Wextra', '-Werror'] + මූලය_ගොනු
        චිත්_රය_ගමනාන්තය = ගමනාන්තය_අගය/'චිත්_රය_අගය.o'
        subprocess.check_call(['clang', '-std=c11', '-O2', '-c', str(ගමනාන්තය_අගය/'චිත්_රය_අගය.c'), '-o', str(චිත්_රය_ගමනාන්තය)])
        subprocess.check_call(විධානය+[str(චිත්_රය_ගමනාන්තය), 'build/terminal-font.S', '-o', str(ගමනාන්තය_අගය/'화면갱신시험')], cwd=str(기준))
        결과 = subprocess.check_output([str(ගමනාන්තය_අගය/'화면갱신시험')], timeout=30).decode()
        (ගමනාන්තය_අගය/'වලංගු_කරන්න.log').write_text(결과)
        맞음 = re.search(r'([\d.]+) ms/move; (\d+) framebuffer writes/move', 결과)
        assert 맞음 and 'PASS:' in 결과, 결과
        ලොගය_පේළිය.update(passed=True, move_count=80, resize_count=40, window_count=4,
                   host_cpu_ms_per_move=float(맞음[1]), mean_framebuffer_writes_per_move=int(맞음[2]),
                   full_redraw_reference_equal=True, untouched_outside_damage=True,
                   unchanged_pixels_not_written=True, repeated_position_not_repainted=True,
                   padded_stride_preserved=True)
        print(결과, end='')
    finally:
        (ගමනාන්තය_අගය/'report.json').write_text(json.dumps(ලොගය_පේළිය, ensure_ascii=False, indent=2)+'\n')

if __name__ == '__main__': ක්_රියාත්මක_කරන්න_2()

#!/usr/bin/env python3
"""ನಿಜವಾದ_ಡೇಟಾ ಕರ್ನಲ್_ಮೌಲ್ಯ 그리기 코드를 ಹೋಸ್ಟ್ ಮೆಮೊರಿ_ಡೇಟಾ 화면에 연결해 부분 갱신을 검증한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

ಬಿಂಬಿಸು_ಮೂಲ = Path(__file__).resolve().parents[1]

def ಚಲಾಯಿಸು_2():
    ಮೂಲ_ಫೈಲ್_ಗಳು = ['시험/화면갱신.c', 'ಯಂತ್ರ/화면그림.c', 'ಯಂತ್ರ/ಟರ್ಮಿನಲ್.c', 'ಯಂತ್ರ/ವಿಜೆಟ್.c']
    검증원문들 = ಮೂಲ_ಫೈಲ್_ಗಳು + ['ಮೂಲ/화면합성.java', 'ಮೂಲ/ಬೋರ್ಡ್.java', '../../compiler/자바도구/기계어미리번역.java']
    ಗಮ್ಯಸ್ಥಾನ_ಮೌಲ್ಯ = ಬಿಂಬಿಸು_ಮೂಲ/'build/verification/redraw'; ಗಮ್ಯಸ್ಥಾನ_ಮೌಲ್ಯ.mkdir(parents=True, exist_ok=True)
    ಲಾಗ್_ದಾಖಲೆ = {'passed': False, 'test_environment': 'host CPU, Java AOT framebuffer composition and native terminal/widgets with memory framebuffer',
          'kernel_sha256': hashlib.sha256((ಬಿಂಬಿಸು_ಮೂಲ/'build/kernel8.img').read_bytes()).hexdigest(),
          'source_sha256': {ಹೆಸರು: hashlib.sha256((ಬಿಂಬಿಸು_ಮೂಲ/ಹೆಸರು).read_bytes()).hexdigest() for ಹೆಸರು in 검증원문들}}
    try:
        ವರ್ಗ_ಹಾದಿ = ಗಮ್ಯಸ್ಥಾನ_ಮೌಲ್ಯ/'classes'; ವರ್ಗ_ಹಾದಿ.mkdir(exist_ok=True)
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(ವರ್ಗ_ಹಾದಿ),
            str(ಬಿಂಬಿಸು_ಮೂಲ/'ಮೂಲ/화면합성.java'), str(ಬಿಂಬಿಸು_ಮೂಲ/'ಮೂಲ/ಬೋರ್ಡ್.java')])
        ರಫ್ತುಗೊಳಿಸು_ಕೋಷ್ಟಕ = {'jdraw_prepare': 'ಸಿದ್ಧಪಡಿಸು', 'jdraw_width': '너비얻기', 'jdraw_height': '높이얻기',
            'jdraw_count_low': '기록아래얻기', 'jdraw_count_high': '기록위얻기', 'jdraw_clip': 'ಕ್ಲಿಪ್',
            'jdraw_clip_value': 'ಕ್ಲಿಪ್_ಮೌಲ್ಯ', 'jdraw_begin': 'ಚಲಾಯಿಸು_2', 'jdraw_end': 'ಮುಗಿಸು',
            'jdraw_pixel': 'ಪೆಲ್', 'jdraw_rectangle': '사각그림', 'jdraw_pointer': 'ಸೂಚಕ'}
        번역명령 = ['sh', str(ಬಿಂಬಿಸು_ಮೂಲ.parents[1]/'compiler/미리번역.sh'), '--entry', '화면합성.너비얻기', '-o', str(ಗಮ್ಯಸ್ಥಾನ_ಮೌಲ್ಯ/'ಚಿತ್ರರಚನೆ_ಮೌಲ್ಯ.c')]
        for ಸಂಪರ್ಕ_ಕಲ್ಪಿಸು, ಕಾರ್ಯ_ಮೌಲ್ಯ in ರಫ್ತುಗೊಳಿಸು_ಕೋಷ್ಟಕ.items(): 번역명령.extend(['--export', ಸಂಪರ್ಕ_ಕಲ್ಪಿಸು+'=화면합성.'+ಕಾರ್ಯ_ಮೌಲ್ಯ])
        subprocess.check_call(번역명령+[str(ಮಾರ್ಗ) for ಮಾರ್ಗ in sorted(ವರ್ಗ_ಹಾದಿ.glob('*.class'))])
        ಆಜ್ಞೆ = ['clang', '-std=c11', '-O2', '-Wall', '-Wextra', '-Werror'] + ಮೂಲ_ಫೈಲ್_ಗಳು
        ಚಿತ್ರರಚನೆ_ಗಮ್ಯಸ್ಥಾನ = ಗಮ್ಯಸ್ಥಾನ_ಮೌಲ್ಯ/'ಚಿತ್ರರಚನೆ_ಮೌಲ್ಯ.o'
        subprocess.check_call(['clang', '-std=c11', '-O2', '-c', str(ಗಮ್ಯಸ್ಥಾನ_ಮೌಲ್ಯ/'ಚಿತ್ರರಚನೆ_ಮೌಲ್ಯ.c'), '-o', str(ಚಿತ್ರರಚನೆ_ಗಮ್ಯಸ್ಥಾನ)])
        subprocess.check_call(ಆಜ್ಞೆ+[str(ಚಿತ್ರರಚನೆ_ಗಮ್ಯಸ್ಥಾನ), 'build/terminal-font.S', '-o', str(ಗಮ್ಯಸ್ಥಾನ_ಮೌಲ್ಯ/'화면갱신시험')], cwd=str(ಬಿಂಬಿಸು_ಮೂಲ))
        ಮಾಪನ = subprocess.check_output([str(ಗಮ್ಯಸ್ಥಾನ_ಮೌಲ್ಯ/'화면갱신시험')], timeout=30).decode()
        (ಗಮ್ಯಸ್ಥಾನ_ಮೌಲ್ಯ/'ಸಕ್ರಮೀಕರಿಸು.log').write_text(ಮಾಪನ)
        맞음 = re.search(r'([\d.]+) ms/move; (\d+) framebuffer writes/move', ಮಾಪನ)
        assert 맞음 and 'PASS:' in ಮಾಪನ, ಮಾಪನ
        ಲಾಗ್_ದಾಖಲೆ.update(passed=True, move_count=80, resize_count=40, window_count=4,
                   host_cpu_ms_per_move=float(맞음[1]), mean_framebuffer_writes_per_move=int(맞음[2]),
                   full_redraw_reference_equal=True, untouched_outside_damage=True,
                   unchanged_pixels_not_written=True, repeated_position_not_repainted=True,
                   padded_stride_preserved=True)
        print(ಮಾಪನ, end='')
    finally:
        (ಗಮ್ಯಸ್ಥಾನ_ಮೌಲ್ಯ/'report.json').write_text(json.dumps(ಲಾಗ್_ದಾಖಲೆ, ensure_ascii=False, indent=2)+'\n')

if __name__ == '__main__': ಚಲಾಯಿಸು_2()

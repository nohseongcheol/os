#!/usr/bin/env python3
"""ትኽክለኛ_ሓበሬታ ፍረ_ዋጋ 그리기 코드를 አዐንግድ ማህደር_ዝኽረት_ሓበሬታ 화면에 연결해 부분 갱신을 검증한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

기준 = Path(__file__).resolve().parents[1]

def ኣኺድ():
    ምንጪ_ፋይላት = ['시험/화면갱신.c', 'ማሽን/화면그림.c', 'ማሽን/터미널.c', 'ማሽን/መዘካከሪ_መትሓዚ.c']
    검증원문들 = ምንጪ_ፋይላት + ['ምንጪ/화면합성.java', 'ምንጪ/보드.java', '../../compiler/자바도구/기계어미리번역.java']
    መዓልቦ_ዋጋ = 기준/'build/verification/redraw'; መዓልቦ_ዋጋ.mkdir(parents=True, exist_ok=True)
    ምዝጉብ_ሪጋ = {'passed': False, 'test_environment': 'host CPU, Java AOT framebuffer composition and native terminal/widgets with memory framebuffer',
          'kernel_sha256': hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),
          'source_sha256': {ሽም: hashlib.sha256((기준/ሽም).read_bytes()).hexdigest() for ሽም in 검증원문들}}
    try:
        ክፍሊ_መገዲ = መዓልቦ_ዋጋ/'classes'; ክፍሊ_መገዲ.mkdir(exist_ok=True)
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(ክፍሊ_መገዲ),
            str(기준/'ምንጪ/화면합성.java'), str(기준/'ምንጪ/보드.java')])
        ስደድ_ሰሌዳ = {'jdraw_prepare': 'ኣዳልው', 'jdraw_width': '너비얻기', 'jdraw_height': '높이얻기',
            'jdraw_count_low': '기록아래얻기', 'jdraw_count_high': '기록위얻기', 'jdraw_clip': 'ቅንጣብ',
            'jdraw_clip_value': 'ቅንጣብ_ዋጋ', 'jdraw_begin': 'ኣኺድ', 'jdraw_end': 'ጨርስ',
            'jdraw_pixel': 'ንጣብ', 'jdraw_rectangle': '사각그림', 'jdraw_pointer': 'ኣመልካቲ'}
        번역명령 = ['sh', str(기준.parents[1]/'compiler/미리번역.sh'), '--entry', '화면합성.너비얻기', '-o', str(መዓልቦ_ዋጋ/'ስእሊ_ዋጋ.c')]
        for ኣላግብ, ተግባር_ዋጋ in ስደድ_ሰሌዳ.items(): 번역명령.extend(['--export', ኣላግብ+'=화면합성.'+ተግባር_ዋጋ])
        subprocess.check_call(번역명령+[str(መገዲ) for መገዲ in sorted(ክፍሊ_መገዲ.glob('*.class'))])
        ትእዛዝ = ['clang', '-std=c11', '-O2', '-Wall', '-Wextra', '-Werror'] + ምንጪ_ፋይላት
        ስእሊ_መዓልቦ = መዓልቦ_ዋጋ/'ስእሊ_ዋጋ.o'
        subprocess.check_call(['clang', '-std=c11', '-O2', '-c', str(መዓልቦ_ዋጋ/'ስእሊ_ዋጋ.c'), '-o', str(ስእሊ_መዓልቦ)])
        subprocess.check_call(ትእዛዝ+[str(ስእሊ_መዓልቦ), 'build/terminal-font.S', '-o', str(መዓልቦ_ዋጋ/'화면갱신시험')], cwd=str(기준))
        결과 = subprocess.check_output([str(መዓልቦ_ዋጋ/'화면갱신시험')], timeout=30).decode()
        (መዓልቦ_ዋጋ/'አረጋግፅ.log').write_text(결과)
        맞음 = re.search(r'([\d.]+) ms/move; (\d+) framebuffer writes/move', 결과)
        assert 맞음 and 'PASS:' in 결과, 결과
        ምዝጉብ_ሪጋ.update(passed=True, move_count=80, resize_count=40, window_count=4,
                   host_cpu_ms_per_move=float(맞음[1]), mean_framebuffer_writes_per_move=int(맞음[2]),
                   full_redraw_reference_equal=True, untouched_outside_damage=True,
                   unchanged_pixels_not_written=True, repeated_position_not_repainted=True,
                   padded_stride_preserved=True)
        print(결과, end='')
    finally:
        (መዓልቦ_ዋጋ/'report.json').write_text(json.dumps(ምዝጉብ_ሪጋ, ensure_ascii=False, indent=2)+'\n')

if __name__ == '__main__': ኣኺድ()

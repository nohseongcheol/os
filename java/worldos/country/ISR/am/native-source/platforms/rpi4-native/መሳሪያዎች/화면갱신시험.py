#!/usr/bin/env python3
"""ትክክለኛ_ውሂብ ዓንኳር_እሴት 그리기 코드를 አዘጋጅ_b78e430d ማስቀመጫ_ውሂብ 화면에 연결해 부분 갱신을 검증한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

አሳይ_ስር = Path(__file__).resolve().parents[1]

def ማስኬጃ():
    ምንጭ_ፋይሎች = ['시험/화면갱신.c', 'ማሽን/화면그림.c', 'ማሽን/ተርሚናል.c', 'ማሽን/ዊድጌት.c']
    검증원문들 = ምንጭ_ፋይሎች + ['ምንጭ/화면합성.java', 'ምንጭ/ቦርድ.java', '../../compiler/자바도구/기계어미리번역.java']
    መድረሻ_እሴት = አሳይ_ስር/'build/verification/redraw'; መድረሻ_እሴት.mkdir(parents=True, exist_ok=True)
    መዝግብ_ረድፍ = {'passed': False, 'test_environment': 'host CPU, Java AOT framebuffer composition and native terminal/widgets with memory framebuffer',
          'kernel_sha256': hashlib.sha256((አሳይ_ስር/'build/kernel8.img').read_bytes()).hexdigest(),
          'source_sha256': {ስም: hashlib.sha256((አሳይ_ስር/ስም).read_bytes()).hexdigest() for ስም in 검증원문들}}
    try:
        መደብ_ዱካ = መድረሻ_እሴት/'classes'; መደብ_ዱካ.mkdir(exist_ok=True)
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(መደብ_ዱካ),
            str(አሳይ_ስር/'ምንጭ/화면합성.java'), str(አሳይ_ስር/'ምንጭ/ቦርድ.java')])
        አስወጣ_ሰንጠረዥ = {'jdraw_prepare': 'አዘጋጅ_9ce364fc', 'jdraw_width': '너비얻기', 'jdraw_height': '높이얻기',
            'jdraw_count_low': '기록아래얻기', 'jdraw_count_high': '기록위얻기', 'jdraw_clip': 'ቅንጥብ',
            'jdraw_clip_value': 'ቅንጥብ_እሴት', 'jdraw_begin': 'ማስኬጃ', 'jdraw_end': 'ጨርስ',
            'jdraw_pixel': 'ፒክስል', 'jdraw_rectangle': '사각그림', 'jdraw_pointer': 'ጠቋሚ'}
        번역명령 = ['sh', str(አሳይ_ስር.parents[1]/'compiler/미리번역.sh'), '--entry', '화면합성.너비얻기', '-o', str(መድረሻ_እሴት/'ስዕል_እሴት.c')]
        for መገናኛ, ተግባር_እሴት in አስወጣ_ሰንጠረዥ.items(): 번역명령.extend(['--export', መገናኛ+'=화면합성.'+ተግባር_እሴት])
        subprocess.check_call(번역명령+[str(መተላለፊያ) for መተላለፊያ in sorted(መደብ_ዱካ.glob('*.class'))])
        ትእዛዝ = ['clang', '-std=c11', '-O2', '-Wall', '-Wextra', '-Werror'] + ምንጭ_ፋይሎች
        ስዕል_መድረሻ = መድረሻ_እሴት/'ስዕል_እሴት.o'
        subprocess.check_call(['clang', '-std=c11', '-O2', '-c', str(መድረሻ_እሴት/'ስዕል_እሴት.c'), '-o', str(ስዕል_መድረሻ)])
        subprocess.check_call(ትእዛዝ+[str(ስዕል_መድረሻ), 'build/terminal-font.S', '-o', str(መድረሻ_እሴት/'화면갱신시험')], cwd=str(አሳይ_ስር))
        ልኬት = subprocess.check_output([str(መድረሻ_እሴት/'화면갱신시험')], timeout=30).decode()
        (መድረሻ_እሴት/'ትክክለኛነት_አረጋግጥ.log').write_text(ልኬት)
        맞음 = re.search(r'([\d.]+) ms/move; (\d+) framebuffer writes/move', ልኬት)
        assert 맞음 and 'PASS:' in ልኬት, ልኬት
        መዝግብ_ረድፍ.update(passed=True, move_count=80, resize_count=40, window_count=4,
                   host_cpu_ms_per_move=float(맞음[1]), mean_framebuffer_writes_per_move=int(맞음[2]),
                   full_redraw_reference_equal=True, untouched_outside_damage=True,
                   unchanged_pixels_not_written=True, repeated_position_not_repainted=True,
                   padded_stride_preserved=True)
        print(ልኬት, end='')
    finally:
        (መድረሻ_እሴት/'report.json').write_text(json.dumps(መዝግብ_ረድፍ, ensure_ascii=False, indent=2)+'\n')

if __name__ == '__main__': ማስኬጃ()

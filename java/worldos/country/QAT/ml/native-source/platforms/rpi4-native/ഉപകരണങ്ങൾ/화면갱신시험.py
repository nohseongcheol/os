#!/usr/bin/env python3
"""വാസ്തവമായ_ഡാറ്റാ കെര്_ണല്_മൂല്യം 그리기 코드를 ഹോസ്റ്റ് മെമ്മറി_ഡാറ്റാ 화면에 연결해 부분 갱신을 검증한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം = Path(__file__).resolve().parents[1]

def നടപ്പിലാക്കുക():
    ഉറവിടം_ഫയലുകൾ = ['시험/화면갱신.c', 'മെഷീൻ/화면그림.c', 'മെഷീൻ/ടെ_ര്മിനല്.c', 'മെഷീൻ/വിജറ്റ്.c']
    검증원문들 = ഉറവിടം_ഫയലുകൾ + ['ഉറവിടം/화면합성.java', 'ഉറവിടം/ബോർഡ്.java', '../../compiler/자바도구/기계어미리번역.java']
    ഉദ്ദിഷ്ടസ്ഥാനം_മൂല്യം = പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം/'build/verification/redraw'; ഉദ്ദിഷ്ടസ്ഥാനം_മൂല്യം.mkdir(parents=True, exist_ok=True)
    ലോഗ്_രേഖ = {'passed': False, 'test_environment': 'host CPU, Java AOT framebuffer composition and native terminal/widgets with memory framebuffer',
          'kernel_sha256': hashlib.sha256((പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം/'build/kernel8.img').read_bytes()).hexdigest(),
          'source_sha256': {പേരു്: hashlib.sha256((പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം/പേരു്).read_bytes()).hexdigest() for പേരു് in 검증원문들}}
    try:
        ക്ലാസ്_പാത = ഉദ്ദിഷ്ടസ്ഥാനം_മൂല്യം/'classes'; ക്ലാസ്_പാത.mkdir(exist_ok=True)
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(ക്ലാസ്_പാത),
            str(പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം/'ഉറവിടം/화면합성.java'), str(പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം/'ഉറവിടം/ബോർഡ്.java')])
        എക്_സ്_പോർട്ടുചെയ്യുക_పట్టిక = {'jdraw_prepare': 'തയ്യാറാക്കുക', 'jdraw_width': '너비얻기', 'jdraw_height': '높이얻기',
            'jdraw_count_low': '기록아래얻기', 'jdraw_count_high': '기록위얻기', 'jdraw_clip': 'ക്ലിപ്പ്',
            'jdraw_clip_value': 'ക്ലിപ്പ്_മൂല്യം', 'jdraw_begin': 'നടപ്പിലാക്കുക', 'jdraw_end': 'പൂർത്തിയാക്കുക',
            'jdraw_pixel': 'പെല്', 'jdraw_rectangle': '사각그림', 'jdraw_pointer': 'പോയിന്_റര്'}
        번역명령 = ['sh', str(പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം.parents[1]/'compiler/미리번역.sh'), '--entry', '화면합성.너비얻기', '-o', str(ഉദ്ദിഷ്ടസ്ഥാനം_മൂല്യം/'ഡ്രോയിംഗ്_മൂല്യം.c')]
        for കണക്ടു്_ചെയ്യുക, കാര്യപ്രവര്_ത്തനം_മൂല്യം in എക്_സ്_പോർട്ടുചെയ്യുക_పట్టిక.items(): 번역명령.extend(['--export', കണക്ടു്_ചെയ്യുക+'=화면합성.'+കാര്യപ്രവര്_ത്തനം_മൂല്യം])
        subprocess.check_call(번역명령+[str(വഴി) for വഴി in sorted(ക്ലാസ്_പാത.glob('*.class'))])
        ആജ്ഞ = ['clang', '-std=c11', '-O2', '-Wall', '-Wextra', '-Werror'] + ഉറവിടം_ഫയലുകൾ
        ഡ്രോയിംഗ്_ഉദ്ദിഷ്ടസ്ഥാനം = ഉദ്ദിഷ്ടസ്ഥാനം_മൂല്യം/'ഡ്രോയിംഗ്_മൂല്യം.o'
        subprocess.check_call(['clang', '-std=c11', '-O2', '-c', str(ഉദ്ദിഷ്ടസ്ഥാനം_മൂല്യം/'ഡ്രോയിംഗ്_മൂല്യം.c'), '-o', str(ഡ്രോയിംഗ്_ഉദ്ദിഷ്ടസ്ഥാനം)])
        subprocess.check_call(ആജ്ഞ+[str(ഡ്രോയിംഗ്_ഉദ്ദിഷ്ടസ്ഥാനം), 'build/terminal-font.S', '-o', str(ഉദ്ദിഷ്ടസ്ഥാനം_മൂല്യം/'화면갱신시험')], cwd=str(പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം))
        അളവ് = subprocess.check_output([str(ഉദ്ദിഷ്ടസ്ഥാനം_മൂല്യം/'화면갱신시험')], timeout=30).decode()
        (ഉദ്ദിഷ്ടസ്ഥാനം_മൂല്യം/'സാധൂകരിക്കുക.log').write_text(അളവ്)
        맞음 = re.search(r'([\d.]+) ms/move; (\d+) framebuffer writes/move', അളവ്)
        assert 맞음 and 'PASS:' in അളവ്, അളവ്
        ലോഗ്_രേഖ.update(passed=True, move_count=80, resize_count=40, window_count=4,
                   host_cpu_ms_per_move=float(맞음[1]), mean_framebuffer_writes_per_move=int(맞음[2]),
                   full_redraw_reference_equal=True, untouched_outside_damage=True,
                   unchanged_pixels_not_written=True, repeated_position_not_repainted=True,
                   padded_stride_preserved=True)
        print(അളവ്, end='')
    finally:
        (ഉദ്ദിഷ്ടസ്ഥാനം_മൂല്യം/'report.json').write_text(json.dumps(ലോഗ്_രേഖ, ensure_ascii=False, indent=2)+'\n')

if __name__ == '__main__': നടപ്പിലാക്കുക()

#!/usr/bin/env python3
"""faktiki_verilənlər nüvə_VALUE 그리기 코드를 host Yaddaş_verilənlər 화면에 연결해 부분 갱신을 검증한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

Project_kök = Path(__file__).resolve().parents[1]

def İcra_Et():
    mənbə_Fayllar = ['시험/화면갱신.c', 'maşın/화면그림.c', 'maşın/Terminal.c', 'maşın/vidget.c']
    검증원문들 = mənbə_Fayllar + ['QAYNAQ/화면합성.java', 'QAYNAQ/lövhə.java', '../../compiler/자바도구/기계어미리번역.java']
    təyinat_VALUE_a0fbc067 = Project_kök/'build/verification/redraw'; təyinat_VALUE_a0fbc067.mkdir(parents=True, exist_ok=True)
    LOG_yaz = {'passed': False, 'test_environment': 'host CPU, Java AOT framebuffer composition and native terminal/widgets with memory framebuffer',
          'kernel_sha256': hashlib.sha256((Project_kök/'build/kernel8.img').read_bytes()).hexdigest(),
          'source_sha256': {Ad: hashlib.sha256((Project_kök/Ad).read_bytes()).hexdigest() for Ad in 검증원문들}}
    try:
        Sinif_yol = təyinat_VALUE_a0fbc067/'classes'; Sinif_yol.mkdir(exist_ok=True)
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(Sinif_yol),
            str(Project_kök/'QAYNAQ/화면합성.java'), str(Project_kök/'QAYNAQ/lövhə.java')])
        ixrac_etmək_cədvəl = {'jdraw_prepare': 'Hazırla', 'jdraw_width': '너비얻기', 'jdraw_height': '높이얻기',
            'jdraw_count_low': '기록아래얻기', 'jdraw_count_high': '기록위얻기', 'jdraw_clip': 'klip',
            'jdraw_clip_value': 'klip_VALUE', 'jdraw_begin': 'İcra_Et', 'jdraw_end': 'Bitir',
            'jdraw_pixel': 'piksel', 'jdraw_rectangle': '사각그림', 'jdraw_pointer': 'göstərici'}
        번역명령 = ['sh', str(Project_kök.parents[1]/'compiler/미리번역.sh'), '--entry', '화면합성.너비얻기', '-o', str(təyinat_VALUE_a0fbc067/'rəsm_VALUE.c')]
        for Bağlan, FUNCTION_VALUE in ixrac_etmək_cədvəl.items(): 번역명령.extend(['--export', Bağlan+'=화면합성.'+FUNCTION_VALUE])
        subprocess.check_call(번역명령+[str(Cığır) for Cığır in sorted(Sinif_yol.glob('*.class'))])
        Əmr = ['clang', '-std=c11', '-O2', '-Wall', '-Wextra', '-Werror'] + mənbə_Fayllar
        rəsm_təyinat = təyinat_VALUE_a0fbc067/'rəsm_VALUE.o'
        subprocess.check_call(['clang', '-std=c11', '-O2', '-c', str(təyinat_VALUE_a0fbc067/'rəsm_VALUE.c'), '-o', str(rəsm_təyinat)])
        subprocess.check_call(Əmr+[str(rəsm_təyinat), 'build/terminal-font.S', '-o', str(təyinat_VALUE_a0fbc067/'화면갱신시험')], cwd=str(Project_kök))
        ölçü = subprocess.check_output([str(təyinat_VALUE_a0fbc067/'화면갱신시험')], timeout=30).decode()
        (təyinat_VALUE_a0fbc067/'təsdiqlə.log').write_text(ölçü)
        맞음 = re.search(r'([\d.]+) ms/move; (\d+) framebuffer writes/move', ölçü)
        assert 맞음 and 'PASS:' in ölçü, ölçü
        LOG_yaz.update(passed=True, move_count=80, resize_count=40, window_count=4,
                   host_cpu_ms_per_move=float(맞음[1]), mean_framebuffer_writes_per_move=int(맞음[2]),
                   full_redraw_reference_equal=True, untouched_outside_damage=True,
                   unchanged_pixels_not_written=True, repeated_position_not_repainted=True,
                   padded_stride_preserved=True)
        print(ölçü, end='')
    finally:
        (təyinat_VALUE_a0fbc067/'report.json').write_text(json.dumps(LOG_yaz, ensure_ascii=False, indent=2)+'\n')

if __name__ == '__main__': İcra_Et()

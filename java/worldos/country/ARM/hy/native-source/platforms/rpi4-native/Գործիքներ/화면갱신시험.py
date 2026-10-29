#!/usr/bin/env python3
"""իրական_տվյալ միջուկ_արժեք 그리기 코드를 հոստ Հիշողություն_տվյալ 화면에 연결해 부분 갱신을 검증한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

արձակել_արմատ = Path(__file__).resolve().parents[1]

def Գործարկել():
    աղբյուր_Նիշքեր = ['시험/화면갱신.c', 'մեքենա/화면그림.c', 'մեքենա/Տերմինալ.c', 'մեքենա/վիջեթ.c']
    검증원문들 = աղբյուր_Նիշքեր + ['ԱՂԲՅՈՒՐ/화면합성.java', 'ԱՂԲՅՈՒՐ/տախտակ.java', '../../compiler/자바도구/기계어미리번역.java']
    նպատակակետ_արժեք = արձակել_արմատ/'build/verification/redraw'; նպատակակետ_արժեք.mkdir(parents=True, exist_ok=True)
    մատյան_տող = {'passed': False, 'test_environment': 'host CPU, Java AOT framebuffer composition and native terminal/widgets with memory framebuffer',
          'kernel_sha256': hashlib.sha256((արձակել_արմատ/'build/kernel8.img').read_bytes()).hexdigest(),
          'source_sha256': {Անուն: hashlib.sha256((արձակել_արմատ/Անուն).read_bytes()).hexdigest() for Անուն in 검증원문들}}
    try:
        դաս_ուղի = նպատակակետ_արժեք/'classes'; դաս_ուղի.mkdir(exist_ok=True)
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(դաս_ուղի),
            str(արձակել_արմատ/'ԱՂԲՅՈՒՐ/화면합성.java'), str(արձակել_արմատ/'ԱՂԲՅՈՒՐ/տախտակ.java')])
        արտահանել_աղյուսակ = {'jdraw_prepare': 'Պատրաստել', 'jdraw_width': '너비얻기', 'jdraw_height': '높이얻기',
            'jdraw_count_low': '기록아래얻기', 'jdraw_count_high': '기록위얻기', 'jdraw_clip': 'հոլովակ',
            'jdraw_clip_value': 'հոլովակ_արժեք', 'jdraw_begin': 'Գործարկել', 'jdraw_end': 'Ավարտ',
            'jdraw_pixel': 'փիքսել', 'jdraw_rectangle': '사각그림', 'jdraw_pointer': 'նշորդ'}
        번역명령 = ['sh', str(արձակել_արմատ.parents[1]/'compiler/미리번역.sh'), '--entry', '화면합성.너비얻기', '-o', str(նպատակակետ_արժեք/'նկար_արժեք_c143fe9e.c')]
        for Միացնել, ՖՈՒՆԿՑԻԱ_արժեք in արտահանել_աղյուսակ.items(): 번역명령.extend(['--export', Միացնել+'=화면합성.'+ՖՈՒՆԿՑԻԱ_արժեք])
        subprocess.check_call(번역명령+[str(Ճանապարհ) for Ճանապարհ in sorted(դաս_ուղի.glob('*.class'))])
        Հրահանգ = ['clang', '-std=c11', '-O2', '-Wall', '-Wextra', '-Werror'] + աղբյուր_Նիշքեր
        նկար_նպատակակետ = նպատակակետ_արժեք/'նկար_արժեք_c143fe9e.o'
        subprocess.check_call(['clang', '-std=c11', '-O2', '-c', str(նպատակակետ_արժեք/'նկար_արժեք_c143fe9e.c'), '-o', str(նկար_նպատակակետ)])
        subprocess.check_call(Հրահանգ+[str(նկար_նպատակակետ), 'build/terminal-font.S', '-o', str(նպատակակետ_արժեք/'화면갱신시험')], cwd=str(արձակել_արմատ))
        չափ = subprocess.check_output([str(նպատակակետ_արժեք/'화면갱신시험')], timeout=30).decode()
        (նպատակակետ_արժեք/'վավերացնել.log').write_text(չափ)
        맞음 = re.search(r'([\d.]+) ms/move; (\d+) framebuffer writes/move', չափ)
        assert 맞음 and 'PASS:' in չափ, չափ
        մատյան_տող.update(passed=True, move_count=80, resize_count=40, window_count=4,
                   host_cpu_ms_per_move=float(맞음[1]), mean_framebuffer_writes_per_move=int(맞음[2]),
                   full_redraw_reference_equal=True, untouched_outside_damage=True,
                   unchanged_pixels_not_written=True, repeated_position_not_repainted=True,
                   padded_stride_preserved=True)
        print(չափ, end='')
    finally:
        (նպատակակետ_արժեք/'report.json').write_text(json.dumps(մատյան_տող, ensure_ascii=False, indent=2)+'\n')

if __name__ == '__main__': Գործարկել()

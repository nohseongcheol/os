#!/usr/bin/env python3
"""ھەقىقىي_مەلۇمات يادرو_قىممىتى 그리기 코드를 باقار ساقلىغۇچ_مەلۇمات 화면에 연결해 부분 갱신을 검증한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

كۆرسىتىش_يىلتىز = Path(__file__).resolve().parents[1]

def ئىجرا_قىل_2():
    مەنبە_ھۆججەت = ['시험/화면갱신.c', 'ماشىنا/화면그림.c', 'ماشىنا/تېرمىنال.c', 'ماشىنا/بىرىكمە.c']
    검증원문들 = مەنبە_ھۆججەت + ['مەنبە/화면합성.java', 'مەنبە/سۇپا.java', '../../compiler/자바도구/기계어미리번역.java']
    نىشان_قىممىتى = كۆرسىتىش_يىلتىز/'build/verification/redraw'; نىشان_قىممىتى.mkdir(parents=True, exist_ok=True)
    خاتىرە_قۇر = {'passed': False, 'test_environment': 'host CPU, Java AOT framebuffer composition and native terminal/widgets with memory framebuffer',
          'kernel_sha256': hashlib.sha256((كۆرسىتىش_يىلتىز/'build/kernel8.img').read_bytes()).hexdigest(),
          'source_sha256': {ئاتى: hashlib.sha256((كۆرسىتىش_يىلتىز/ئاتى).read_bytes()).hexdigest() for ئاتى in 검증원문들}}
    try:
        تۈركۈم_يول = نىشان_قىممىتى/'classes'; تۈركۈم_يول.mkdir(exist_ok=True)
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(تۈركۈم_يول),
            str(كۆرسىتىش_يىلتىز/'مەنبە/화면합성.java'), str(كۆرسىتىش_يىلتىز/'مەنبە/سۇپا.java')])
        چىقىرىش_جەدۋەل = {'jdraw_prepare': 'تەييارلىماق', 'jdraw_width': '너비얻기', 'jdraw_height': '높이얻기',
            'jdraw_count_low': '기록아래얻기', 'jdraw_count_high': '기록위얻기', 'jdraw_clip': 'كەسمە',
            'jdraw_clip_value': 'كەسمە_قىممىتى', 'jdraw_begin': 'ئىجرا_قىل_2', 'jdraw_end': 'تاماملىماق',
            'jdraw_pixel': 'پىكسېل', 'jdraw_rectangle': '사각그림', 'jdraw_pointer': 'ئىسترېلكا'}
        번역명령 = ['sh', str(كۆرسىتىش_يىلتىز.parents[1]/'compiler/미리번역.sh'), '--entry', '화면합성.너비얻기', '-o', str(نىشان_قىممىتى/'سىزىش_قىممىتى.c')]
        for ئۇلا, فۇنكسىيە_قىممىتى in چىقىرىش_جەدۋەل.items(): 번역명령.extend(['--export', ئۇلا+'=화면합성.'+فۇنكسىيە_قىممىتى])
        subprocess.check_call(번역명령+[str(يول) for يول in sorted(تۈركۈم_يول.glob('*.class'))])
        بۇيرۇق = ['clang', '-std=c11', '-O2', '-Wall', '-Wextra', '-Werror'] + مەنبە_ھۆججەت
        سىزىش_نىشان = نىشان_قىممىتى/'سىزىش_قىممىتى.o'
        subprocess.check_call(['clang', '-std=c11', '-O2', '-c', str(نىشان_قىممىتى/'سىزىش_قىممىتى.c'), '-o', str(سىزىش_نىشان)])
        subprocess.check_call(بۇيرۇق+[str(سىزىش_نىشان), 'build/terminal-font.S', '-o', str(نىشان_قىممىتى/'화면갱신시험')], cwd=str(كۆرسىتىش_يىلتىز))
        ئۆلچەم = subprocess.check_output([str(نىشان_قىممىتى/'화면갱신시험')], timeout=30).decode()
        (نىشان_قىممىتى/'دەلىللەش.log').write_text(ئۆلچەم)
        맞음 = re.search(r'([\d.]+) ms/move; (\d+) framebuffer writes/move', ئۆلچەم)
        assert 맞음 and 'PASS:' in ئۆلچەم, ئۆلچەم
        خاتىرە_قۇر.update(passed=True, move_count=80, resize_count=40, window_count=4,
                   host_cpu_ms_per_move=float(맞음[1]), mean_framebuffer_writes_per_move=int(맞음[2]),
                   full_redraw_reference_equal=True, untouched_outside_damage=True,
                   unchanged_pixels_not_written=True, repeated_position_not_repainted=True,
                   padded_stride_preserved=True)
        print(ئۆلچەم, end='')
    finally:
        (نىشان_قىممىتى/'report.json').write_text(json.dumps(خاتىرە_قۇر, ensure_ascii=False, indent=2)+'\n')

if __name__ == '__main__': ئىجرا_قىل_2()

#!/usr/bin/env python3
"""რეალური_მონაცემები ბირთვი_მნიშვნელობა 그리기 코드를 მასპინძელი მეხსიერება_მონაცემები 화면에 연결해 부분 갱신을 검증한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

პროეცირება_ფესვი = Path(__file__).resolve().parents[1]

def გაშვება():
    წყარო_ფაილები = ['시험/화면갱신.c', 'კომპიუტერი/화면그림.c', 'კომპიუტერი/ტერმინალი.c', 'კომპიუტერი/ვიჯეტი.c']
    검증원문들 = წყარო_ფაილები + ['წყარო/화면합성.java', 'წყარო/დაფა.java', '../../compiler/자바도구/기계어미리번역.java']
    მიმართულება_მნიშვნელობა = პროეცირება_ფესვი/'build/verification/redraw'; მიმართულება_მნიშვნელობა.mkdir(parents=True, exist_ok=True)
    ჟურნალი_ჩაწერა = {'passed': False, 'test_environment': 'host CPU, Java AOT framebuffer composition and native terminal/widgets with memory framebuffer',
          'kernel_sha256': hashlib.sha256((პროეცირება_ფესვი/'build/kernel8.img').read_bytes()).hexdigest(),
          'source_sha256': {სახელი: hashlib.sha256((პროეცირება_ფესვი/სახელი).read_bytes()).hexdigest() for სახელი in 검증원문들}}
    try:
        კლასი_მდებარეობა = მიმართულება_მნიშვნელობა/'classes'; კლასი_მდებარეობა.mkdir(exist_ok=True)
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(კლასი_მდებარეობა),
            str(პროეცირება_ფესვი/'წყარო/화면합성.java'), str(პროეცირება_ფესვი/'წყარო/დაფა.java')])
        ექსპორტი_ცხრილი = {'jdraw_prepare': 'მომზადება', 'jdraw_width': '너비얻기', 'jdraw_height': '높이얻기',
            'jdraw_count_low': '기록아래얻기', 'jdraw_count_high': '기록위얻기', 'jdraw_clip': 'კლიპი',
            'jdraw_clip_value': 'კლიპი_მნიშვნელობა', 'jdraw_begin': 'გაშვება', 'jdraw_end': 'დასრულება',
            'jdraw_pixel': 'პიქსელი', 'jdraw_rectangle': '사각그림', 'jdraw_pointer': 'კურსორი'}
        번역명령 = ['sh', str(პროეცირება_ფესვი.parents[1]/'compiler/미리번역.sh'), '--entry', '화면합성.너비얻기', '-o', str(მიმართულება_მნიშვნელობა/'ნახატი_მნიშვნელობა_c143fe9e.c')]
        for დაკავშირება, ფუნქცია_მნიშვნელობა in ექსპორტი_ცხრილი.items(): 번역명령.extend(['--export', დაკავშირება+'=화면합성.'+ფუნქცია_მნიშვნელობა])
        subprocess.check_call(번역명령+[str(გეზი) for გეზი in sorted(კლასი_მდებარეობა.glob('*.class'))])
        ბრძანება = ['clang', '-std=c11', '-O2', '-Wall', '-Wextra', '-Werror'] + წყარო_ფაილები
        ნახატი_მიმართულება = მიმართულება_მნიშვნელობა/'ნახატი_მნიშვნელობა_c143fe9e.o'
        subprocess.check_call(['clang', '-std=c11', '-O2', '-c', str(მიმართულება_მნიშვნელობა/'ნახატი_მნიშვნელობა_c143fe9e.c'), '-o', str(ნახატი_მიმართულება)])
        subprocess.check_call(ბრძანება+[str(ნახატი_მიმართულება), 'build/terminal-font.S', '-o', str(მიმართულება_მნიშვნელობა/'화면갱신시험')], cwd=str(პროეცირება_ფესვი))
        გაზომვა = subprocess.check_output([str(მიმართულება_მნიშვნელობა/'화면갱신시험')], timeout=30).decode()
        (მიმართულება_მნიშვნელობა/'შემოწმება.log').write_text(გაზომვა)
        맞음 = re.search(r'([\d.]+) ms/move; (\d+) framebuffer writes/move', გაზომვა)
        assert 맞음 and 'PASS:' in გაზომვა, გაზომვა
        ჟურნალი_ჩაწერა.update(passed=True, move_count=80, resize_count=40, window_count=4,
                   host_cpu_ms_per_move=float(맞음[1]), mean_framebuffer_writes_per_move=int(맞음[2]),
                   full_redraw_reference_equal=True, untouched_outside_damage=True,
                   unchanged_pixels_not_written=True, repeated_position_not_repainted=True,
                   padded_stride_preserved=True)
        print(გაზომვა, end='')
    finally:
        (მიმართულება_მნიშვნელობა/'report.json').write_text(json.dumps(ჟურნალი_ჩაწერა, ensure_ascii=False, indent=2)+'\n')

if __name__ == '__main__': გაშვება()

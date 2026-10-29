#!/usr/bin/env python3
"""실제 نوغی_ارزښت 그리기 코드를 کوربه 메모리 화면에 연결해 부분 갱신을 검증한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

기준 = Path(__file__).resolve().parents[1]

def ځغلول():
    원문들 = ['시험/화면갱신.c', '기계/화면그림.c', '기계/پايالی.c', '기계/화면요소.c']
    검증원문들 = 원문들 + ['سرچينه/화면합성.java', 'سرچينه/보드.java', '../../compiler/자바도구/기계어미리번역.java']
    موخه_ارزښت = 기준/'build/verification/redraw'; موخه_ارزښت.mkdir(parents=True, exist_ok=True)
    خبرال_کیل = {'passed': False, 'test_environment': 'host CPU, Java AOT framebuffer composition and native terminal/widgets with memory framebuffer',
          'kernel_sha256': hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),
          'source_sha256': {نوم: hashlib.sha256((기준/نوم).read_bytes()).hexdigest() for نوم in 검증원문들}}
    try:
        پاړکى_يونلور = موخه_ارزښت/'classes'; پاړکى_يونلور.mkdir(exist_ok=True)
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(پاړکى_يونلور),
            str(기준/'سرچينه/화면합성.java'), str(기준/'سرچينه/보드.java')])
        بهرول_لښتيال = {'jdraw_prepare': '준비', 'jdraw_width': '너비얻기', 'jdraw_height': '높이얻기',
            'jdraw_count_low': '기록아래얻기', 'jdraw_count_high': '기록위얻기', 'jdraw_clip': 'ټوټه',
            'jdraw_clip_value': 'ټوټه_ارزښت', 'jdraw_begin': 'ځغلول', 'jdraw_end': '마침',
            'jdraw_pixel': 'پکسل', 'jdraw_rectangle': '사각그림', 'jdraw_pointer': '포인터'}
        번역명령 = ['sh', str(기준.parents[1]/'compiler/미리번역.sh'), '--entry', '화면합성.너비얻기', '-o', str(موخه_ارزښت/'그림.c')]
        for نښلېدل, 함수 in بهرول_لښتيال.items(): 번역명령.extend(['--export', نښلېدل+'=화면합성.'+함수])
        subprocess.check_call(번역명령+[str(يونلور) for يونلور in sorted(پاړکى_يونلور.glob('*.class'))])
        بولۍ = ['clang', '-std=c11', '-O2', '-Wall', '-Wextra', '-Werror'] + 원문들
        그림목적 = موخه_ارزښت/'그림.o'
        subprocess.check_call(['clang', '-std=c11', '-O2', '-c', str(موخه_ارزښت/'그림.c'), '-o', str(그림목적)])
        subprocess.check_call(بولۍ+[str(그림목적), 'build/terminal-font.S', '-o', str(موخه_ارزښت/'화면갱신시험')], cwd=str(기준))
        결과 = subprocess.check_output([str(موخه_ارزښت/'화면갱신시험')], timeout=30).decode()
        (موخه_ارزښت/'검증.log').write_text(결과)
        맞음 = re.search(r'([\d.]+) ms/move; (\d+) framebuffer writes/move', 결과)
        assert 맞음 and 'PASS:' in 결과, 결과
        خبرال_کیل.update(passed=True, move_count=80, resize_count=40, window_count=4,
                   host_cpu_ms_per_move=float(맞음[1]), mean_framebuffer_writes_per_move=int(맞음[2]),
                   full_redraw_reference_equal=True, untouched_outside_damage=True,
                   unchanged_pixels_not_written=True, repeated_position_not_repainted=True,
                   padded_stride_preserved=True)
        print(결과, end='')
    finally:
        (موخه_ارزښت/'report.json').write_text(json.dumps(خبرال_کیل, ensure_ascii=False, indent=2)+'\n')

if __name__ == '__main__': ځغلول()

#!/usr/bin/env python3
"""প্ৰকৃত_ডাটা কাৰ্ণেল_মান 그리기 코드를 হ_ষ্ট মেম_ৰি_ডাটা 화면에 연결해 부분 갱신을 검증한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

기준 = Path(__file__).resolve().parents[1]

def সঞ্চালন():
    উৎস_ফাইলসমূহ = ['시험/화면갱신.c', 'মেচিন/화면그림.c', 'মেচিন/টাৰ্মিনেল.c', 'মেচিন/ৱিজেট.c']
    검증원문들 = উৎস_ফাইলসমূহ + ['উৎস/화면합성.java', 'উৎস/ব_ৰ্ড.java', '../../compiler/자바도구/기계어미리번역.java']
    গন্তব্য_স্থান_মান = 기준/'build/verification/redraw'; গন্তব্য_স্থান_মান.mkdir(parents=True, exist_ok=True)
    লগ_শাৰী = {'passed': False, 'test_environment': 'host CPU, Java AOT framebuffer composition and native terminal/widgets with memory framebuffer',
          'kernel_sha256': hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),
          'source_sha256': {নাম: hashlib.sha256((기준/নাম).read_bytes()).hexdigest() for নাম in 검증원문들}}
    try:
        শ্ৰেণী_পথ = গন্তব্য_স্থান_মান/'classes'; শ্ৰেণী_পথ.mkdir(exist_ok=True)
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(শ্ৰেণী_পথ),
            str(기준/'উৎস/화면합성.java'), str(기준/'উৎস/ব_ৰ্ড.java')])
        ৰপ্তানি_কৰক_তালিকা = {'jdraw_prepare': 'প্ৰস্তুত_কৰক', 'jdraw_width': '너비얻기', 'jdraw_height': '높이얻기',
            'jdraw_count_low': '기록아래얻기', 'jdraw_count_high': '기록위얻기', 'jdraw_clip': 'ক্লিপ',
            'jdraw_clip_value': 'ক্লিপ_মান', 'jdraw_begin': 'সঞ্চালন', 'jdraw_end': 'সমাপ্ত_কৰক',
            'jdraw_pixel': 'পিক্সেল', 'jdraw_rectangle': '사각그림', 'jdraw_pointer': 'পইণ্টাৰ'}
        번역명령 = ['sh', str(기준.parents[1]/'compiler/미리번역.sh'), '--entry', '화면합성.너비얻기', '-o', str(গন্তব্য_স্থান_মান/'অংকন_মান.c')]
        for সংযোগ_স্থাপনা, ফাংছন_মান in ৰপ্তানি_কৰক_তালিকা.items(): 번역명령.extend(['--export', সংযোগ_স্থাপনা+'=화면합성.'+ফাংছন_মান])
        subprocess.check_call(번역명령+[str(পথ) for পথ in sorted(শ্ৰেণী_পথ.glob('*.class'))])
        কমান্ড = ['clang', '-std=c11', '-O2', '-Wall', '-Wextra', '-Werror'] + উৎস_ফাইলসমূহ
        অংকন_গন্তব্য_স্থান = গন্তব্য_স্থান_মান/'অংকন_মান.o'
        subprocess.check_call(['clang', '-std=c11', '-O2', '-c', str(গন্তব্য_স্থান_মান/'অংকন_মান.c'), '-o', str(অংকন_গন্তব্য_স্থান)])
        subprocess.check_call(কমান্ড+[str(অংকন_গন্তব্য_স্থান), 'build/terminal-font.S', '-o', str(গন্তব্য_স্থান_মান/'화면갱신시험')], cwd=str(기준))
        পৰিমাপ = subprocess.check_output([str(গন্তব্য_স্থান_মান/'화면갱신시험')], timeout=30).decode()
        (গন্তব্য_স্থান_মান/'বৈধকৰণ_কৰক.log').write_text(পৰিমাপ)
        맞음 = re.search(r'([\d.]+) ms/move; (\d+) framebuffer writes/move', পৰিমাপ)
        assert 맞음 and 'PASS:' in পৰিমাপ, পৰিমাপ
        লগ_শাৰী.update(passed=True, move_count=80, resize_count=40, window_count=4,
                   host_cpu_ms_per_move=float(맞음[1]), mean_framebuffer_writes_per_move=int(맞음[2]),
                   full_redraw_reference_equal=True, untouched_outside_damage=True,
                   unchanged_pixels_not_written=True, repeated_position_not_repainted=True,
                   padded_stride_preserved=True)
        print(পৰিমাপ, end='')
    finally:
        (গন্তব্য_স্থান_মান/'report.json').write_text(json.dumps(লগ_শাৰী, ensure_ascii=False, indent=2)+'\n')

if __name__ == '__main__': সঞ্চালন()

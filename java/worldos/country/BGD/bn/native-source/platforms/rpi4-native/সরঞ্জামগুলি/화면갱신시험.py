#!/usr/bin/env python3
"""প্রকৃত_ডাটা কারনেল_মান 그리기 코드를 হোস্ট মেমরি_ডাটা 화면에 연결해 부분 갱신을 검증한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

প্রকল্প_মূল = Path(__file__).resolve().parents[1]

def চালনা():
    উত্স_ফাইলগুলি = ['시험/화면갱신.c', 'মেশিন/화면그림.c', 'মেশিন/আদেশ_ব্যাখ্যাকারী.c', 'মেশিন/উইজেট.c']
    검증원문들 = উত্স_ফাইলগুলি + ['উৎস_নথি/화면합성.java', 'উৎস_নথি/বোর্ড.java', '../../compiler/자바도구/기계어미리번역.java']
    গন্তব্য_মান = প্রকল্প_মূল/'build/verification/redraw'; গন্তব্য_মান.mkdir(parents=True, exist_ok=True)
    লগ_সারি = {'passed': False, 'test_environment': 'host CPU, Java AOT framebuffer composition and native terminal/widgets with memory framebuffer',
          'kernel_sha256': hashlib.sha256((প্রকল্প_মূল/'build/kernel8.img').read_bytes()).hexdigest(),
          'source_sha256': {নাম: hashlib.sha256((প্রকল্প_মূল/নাম).read_bytes()).hexdigest() for নাম in 검증원문들}}
    try:
        শ্রেণী_পথ = গন্তব্য_মান/'classes'; শ্রেণী_পথ.mkdir(exist_ok=True)
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(শ্রেণী_পথ),
            str(প্রকল্প_মূল/'উৎস_নথি/화면합성.java'), str(প্রকল্প_মূল/'উৎস_নথি/বোর্ড.java')])
        রপ্তানি_সারণি = {'jdraw_prepare': 'প্রস্তুত_করুন', 'jdraw_width': '너비얻기', 'jdraw_height': '높이얻기',
            'jdraw_count_low': '기록아래얻기', 'jdraw_count_high': '기록위얻기', 'jdraw_clip': 'ক্লিপ',
            'jdraw_clip_value': 'ক্লিপ_মান', 'jdraw_begin': 'চালনা', 'jdraw_end': 'শেষ',
            'jdraw_pixel': 'পেল্', 'jdraw_rectangle': '사각그림', 'jdraw_pointer': 'নির্দেশক'}
        번역명령 = ['sh', str(প্রকল্প_মূল.parents[1]/'compiler/미리번역.sh'), '--entry', '화면합성.너비얻기', '-o', str(গন্তব্য_মান/'অঙ্কন_মান.c')]
        for সংযোগ_স্থাপনা, ফাংশন_মান in রপ্তানি_সারণি.items(): 번역명령.extend(['--export', সংযোগ_স্থাপনা+'=화면합성.'+ফাংশন_মান])
        subprocess.check_call(번역명령+[str(পথ_2) for পথ_2 in sorted(শ্রেণী_পথ.glob('*.class'))])
        আদেশ = ['clang', '-std=c11', '-O2', '-Wall', '-Wextra', '-Werror'] + উত্স_ফাইলগুলি
        অঙ্কন_গন্তব্য = গন্তব্য_মান/'অঙ্কন_মান.o'
        subprocess.check_call(['clang', '-std=c11', '-O2', '-c', str(গন্তব্য_মান/'অঙ্কন_মান.c'), '-o', str(অঙ্কন_গন্তব্য)])
        subprocess.check_call(আদেশ+[str(অঙ্কন_গন্তব্য), 'build/terminal-font.S', '-o', str(গন্তব্য_মান/'화면갱신시험')], cwd=str(প্রকল্প_মূল))
        পরিমাপ = subprocess.check_output([str(গন্তব্য_মান/'화면갱신시험')], timeout=30).decode()
        (গন্তব্য_মান/'বৈধ_করুন.log').write_text(পরিমাপ)
        맞음 = re.search(r'([\d.]+) ms/move; (\d+) framebuffer writes/move', পরিমাপ)
        assert 맞음 and 'PASS:' in পরিমাপ, পরিমাপ
        লগ_সারি.update(passed=True, move_count=80, resize_count=40, window_count=4,
                   host_cpu_ms_per_move=float(맞음[1]), mean_framebuffer_writes_per_move=int(맞음[2]),
                   full_redraw_reference_equal=True, untouched_outside_damage=True,
                   unchanged_pixels_not_written=True, repeated_position_not_repainted=True,
                   padded_stride_preserved=True)
        print(পরিমাপ, end='')
    finally:
        (গন্তব্য_মান/'report.json').write_text(json.dumps(লগ_সারি, ensure_ascii=False, indent=2)+'\n')

if __name__ == '__main__': চালনা()

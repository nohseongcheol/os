#!/usr/bin/env python3
"""ᎤᏙᎯᏳ_ᎾᏍᎩ_ᎨᏒ_ᎦᏟᏌᏅᎯ kernel_ᏧᎬᏩᎶᏗᏯ 그리기 코드를 ᎠᏁᏢᏍᎩ ᎠᏅᏓᏗᏍᏙ_ᎦᏟᏌᏅᎯ 화면에 연결해 부분 갱신을 검증한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

기준 = Path(__file__).resolve().parents[1]

def ᎠᎢᏎᏍᏗ():
    원문들 = ['시험/화면갱신.c', '기계/화면그림.c', '기계/터미널.c', '기계/화면요소.c']
    검증원문들 = 원문들 + ['ᎦᏟᏌᏅᎯ_0201f362/화면합성.java', 'ᎦᏟᏌᏅᎯ_0201f362/보드.java', '../../compiler/자바도구/기계어미리번역.java']
    ᏮᎦᏛᎢ_ᏧᎬᏩᎶᏗᏯ = 기준/'build/verification/redraw'; ᏮᎦᏛᎢ_ᏧᎬᏩᎶᏗᏯ.mkdir(parents=True, exist_ok=True)
    ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ = {'passed': False, 'test_environment': 'host CPU, Java AOT framebuffer composition and native terminal/widgets with memory framebuffer',
          'kernel_sha256': hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),
          'source_sha256': {ᏚᏙᎥᎢ: hashlib.sha256((기준/ᏚᏙᎥᎢ).read_bytes()).hexdigest() for ᏚᏙᎥᎢ in 검증원문들}}
    try:
        ᏄᏍᏛᎢ_ᎠᏍᏓᏩᏛᏍᏗ = ᏮᎦᏛᎢ_ᏧᎬᏩᎶᏗᏯ/'classes'; ᏄᏍᏛᎢ_ᎠᏍᏓᏩᏛᏍᏗ.mkdir(exist_ok=True)
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(ᏄᏍᏛᎢ_ᎠᏍᏓᏩᏛᏍᏗ),
            str(기준/'ᎦᏟᏌᏅᎯ_0201f362/화면합성.java'), str(기준/'ᎦᏟᏌᏅᎯ_0201f362/보드.java')])
        ᏫᎦᏌᏙᎣᏍᏗ_ᏧᎾᎶᎢᏓ = {'jdraw_prepare': 'ᎭᏛᏅᎢᏍᏓ', 'jdraw_width': '너비얻기', 'jdraw_height': '높이얻기',
            'jdraw_count_low': '기록아래얻기', 'jdraw_count_high': '기록위얻기', 'jdraw_clip': 'ᎠᎬᎭᎸᏓ_ᏗᏓᏴᎳᏛᏙᏗ',
            'jdraw_clip_value': 'ᎠᎬᎭᎸᏓ_ᏗᏓᏴᎳᏛᏙᏗ_ᏧᎬᏩᎶᏗᏯ', 'jdraw_begin': 'ᎠᎢᏎᏍᏗ', 'jdraw_end': 'ᎯᏍᏆᏓ',
            'jdraw_pixel': 'pel', 'jdraw_rectangle': '사각그림', 'jdraw_pointer': 'ᎠᏎᎯᎯ'}
        번역명령 = ['sh', str(기준.parents[1]/'compiler/미리번역.sh'), '--entry', '화면합성.너비얻기', '-o', str(ᏮᎦᏛᎢ_ᏧᎬᏩᎶᏗᏯ/'ᎠᏍᏓᏅᎿᏂᏙᎸ_ᏧᎬᏩᎶᏗᏯ.c')]
        for ᎫᏓᎳ, ᏧᎸᏫᏍᏓᏁᏗᏱ_ᏧᎬᏩᎶᏗᏯ in ᏫᎦᏌᏙᎣᏍᏗ_ᏧᎾᎶᎢᏓ.items(): 번역명령.extend(['--export', ᎫᏓᎳ+'=화면합성.'+ᏧᎸᏫᏍᏓᏁᏗᏱ_ᏧᎬᏩᎶᏗᏯ])
        subprocess.check_call(번역명령+[str(ᎠᏍᏓᏩᏛᏍᏗ) for ᎠᏍᏓᏩᏛᏍᏗ in sorted(ᏄᏍᏛᎢ_ᎠᏍᏓᏩᏛᏍᏗ.glob('*.class'))])
        ᎤᏁᏤᎸᎩ = ['clang', '-std=c11', '-O2', '-Wall', '-Wextra', '-Werror'] + 원문들
        ᎠᏍᏓᏅᎿᏂᏙᎸ_ᏮᎦᏛᎢ = ᏮᎦᏛᎢ_ᏧᎬᏩᎶᏗᏯ/'ᎠᏍᏓᏅᎿᏂᏙᎸ_ᏧᎬᏩᎶᏗᏯ.o'
        subprocess.check_call(['clang', '-std=c11', '-O2', '-c', str(ᏮᎦᏛᎢ_ᏧᎬᏩᎶᏗᏯ/'ᎠᏍᏓᏅᎿᏂᏙᎸ_ᏧᎬᏩᎶᏗᏯ.c'), '-o', str(ᎠᏍᏓᏅᎿᏂᏙᎸ_ᏮᎦᏛᎢ)])
        subprocess.check_call(ᎤᏁᏤᎸᎩ+[str(ᎠᏍᏓᏅᎿᏂᏙᎸ_ᏮᎦᏛᎢ), 'build/terminal-font.S', '-o', str(ᏮᎦᏛᎢ_ᏧᎬᏩᎶᏗᏯ/'화면갱신시험')], cwd=str(기준))
        결과 = subprocess.check_output([str(ᏮᎦᏛᎢ_ᏧᎬᏩᎶᏗᏯ/'화면갱신시험')], timeout=30).decode()
        (ᏮᎦᏛᎢ_ᏧᎬᏩᎶᏗᏯ/'ᎪᎯᏳᏙᏗ.log').write_text(결과)
        맞음 = re.search(r'([\d.]+) ms/move; (\d+) framebuffer writes/move', 결과)
        assert 맞음 and 'PASS:' in 결과, 결과
        ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ.update(passed=True, move_count=80, resize_count=40, window_count=4,
                   host_cpu_ms_per_move=float(맞음[1]), mean_framebuffer_writes_per_move=int(맞음[2]),
                   full_redraw_reference_equal=True, untouched_outside_damage=True,
                   unchanged_pixels_not_written=True, repeated_position_not_repainted=True,
                   padded_stride_preserved=True)
        print(결과, end='')
    finally:
        (ᏮᎦᏛᎢ_ᏧᎬᏩᎶᏗᏯ/'report.json').write_text(json.dumps(ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ, ensure_ascii=False, indent=2)+'\n')

if __name__ == '__main__': ᎠᎢᏎᏍᏗ()

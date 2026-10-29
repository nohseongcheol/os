#!/usr/bin/env python3
"""వాస్తవ_డేటా కెర్నల్_మూల్యం 그리기 코드를 హోస్ట్ మెమరీ_డేటా 화면에 연결해 부분 갱신을 검증한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

ప్రొజెక్ట్_మూలం = Path(__file__).resolve().parents[1]

def నడుపుము():
    మూలం_ఫైల్_లు = ['시험/화면갱신.c', 'యంత్రం/화면그림.c', 'యంత్రం/టెర్మినల్.c', 'యంత్రం/విడ్జెట్.c']
    검증원문들 = మూలం_ఫైల్_లు + ['వనరు/화면합성.java', 'వనరు/బోర్డు.java', '../../compiler/자바도구/기계어미리번역.java']
    గమ్యం_మూల్యం = ప్రొజెక్ట్_మూలం/'build/verification/redraw'; గమ్యం_మూల్యం.mkdir(parents=True, exist_ok=True)
    లాగ్_వరుస = {'passed': False, 'test_environment': 'host CPU, Java AOT framebuffer composition and native terminal/widgets with memory framebuffer',
          'kernel_sha256': hashlib.sha256((ప్రొజెక్ట్_మూలం/'build/kernel8.img').read_bytes()).hexdigest(),
          'source_sha256': {పేరు: hashlib.sha256((ప్రొజెక్ట్_మూలం/పేరు).read_bytes()).hexdigest() for పేరు in 검증원문들}}
    try:
        తరగతి_పథం = గమ్యం_మూల్యం/'classes'; తరగతి_పథం.mkdir(exist_ok=True)
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(తరగతి_పథం),
            str(ప్రొజెక్ట్_మూలం/'వనరు/화면합성.java'), str(ప్రొజెక్ట్_మూలం/'వనరు/బోర్డు.java')])
        ఎగుమతి_చేయు_పట్టిక = {'jdraw_prepare': 'సిద్ధం_చేయు', 'jdraw_width': '너비얻기', 'jdraw_height': '높이얻기',
            'jdraw_count_low': '기록아래얻기', 'jdraw_count_high': '기록위얻기', 'jdraw_clip': 'క్లిప్',
            'jdraw_clip_value': 'క్లిప్_మూల్యం', 'jdraw_begin': 'నడుపుము', 'jdraw_end': 'ముగింపు',
            'jdraw_pixel': 'పెల్', 'jdraw_rectangle': '사각그림', 'jdraw_pointer': 'పాయింటర్'}
        번역명령 = ['sh', str(ప్రొజెక్ట్_మూలం.parents[1]/'compiler/미리번역.sh'), '--entry', '화면합성.너비얻기', '-o', str(గమ్యం_మూల్యం/'రేఖాచిత్రణ_మూల్యం.c')]
        for కనెక్టుచేయి, కార్యం_మూల్యం in ఎగుమతి_చేయు_పట్టిక.items(): 번역명령.extend(['--export', కనెక్టుచేయి+'=화면합성.'+కార్యం_మూల్యం])
        subprocess.check_call(번역명령+[str(పాత్) for పాత్ in sorted(తరగతి_పథం.glob('*.class'))])
        ఆదేశము = ['clang', '-std=c11', '-O2', '-Wall', '-Wextra', '-Werror'] + మూలం_ఫైల్_లు
        రేఖాచిత్రణ_గమ్యం = గమ్యం_మూల్యం/'రేఖాచిత్రణ_మూల్యం.o'
        subprocess.check_call(['clang', '-std=c11', '-O2', '-c', str(గమ్యం_మూల్యం/'రేఖాచిత్రణ_మూల్యం.c'), '-o', str(రేఖాచిత్రణ_గమ్యం)])
        subprocess.check_call(ఆదేశము+[str(రేఖాచిత్రణ_గమ్యం), 'build/terminal-font.S', '-o', str(గమ్యం_మూల్యం/'화면갱신시험')], cwd=str(ప్రొజెక్ట్_మూలం))
        ప్రమాణం = subprocess.check_output([str(గమ్యం_మూల్యం/'화면갱신시험')], timeout=30).decode()
        (గమ్యం_మూల్యం/'నిర్థారీకరించు.log').write_text(ప్రమాణం)
        맞음 = re.search(r'([\d.]+) ms/move; (\d+) framebuffer writes/move', ప్రమాణం)
        assert 맞음 and 'PASS:' in ప్రమాణం, ప్రమాణం
        లాగ్_వరుస.update(passed=True, move_count=80, resize_count=40, window_count=4,
                   host_cpu_ms_per_move=float(맞음[1]), mean_framebuffer_writes_per_move=int(맞음[2]),
                   full_redraw_reference_equal=True, untouched_outside_damage=True,
                   unchanged_pixels_not_written=True, repeated_position_not_repainted=True,
                   padded_stride_preserved=True)
        print(ప్రమాణం, end='')
    finally:
        (గమ్యం_మూల్యం/'report.json').write_text(json.dumps(లాగ్_వరుస, ensure_ascii=False, indent=2)+'\n')

if __name__ == '__main__': నడుపుము()

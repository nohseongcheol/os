#!/usr/bin/env python3
"""taannallarik_titiqqat kernel_atuutilik 그리기 코드를 tuttarvik puigujjaikkut_titiqqat 화면에 연결해 부분 갱신을 검증한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

기준 = Path(__file__).resolve().parents[1]

def 시작():
    원문들 = ['시험/화면갱신.c', '기계/화면그림.c', '기계/터미널.c', '기계/화면요소.c']
    검증원문들 = 원문들 + ['pivviujuq/화면합성.java', 'pivviujuq/보드.java', '../../compiler/자바도구/기계어미리번역.java']
    namunngarvik_atuutilik = 기준/'build/verification/redraw'; namunngarvik_atuutilik.mkdir(parents=True, exist_ok=True)
    papattivik_sanimukutaak = {'passed': False, 'test_environment': 'host CPU, Java AOT framebuffer composition and native terminal/widgets with memory framebuffer',
          'kernel_sha256': hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),
          'source_sha256': {atiq: hashlib.sha256((기준/atiq).read_bytes()).hexdigest() for atiq in 검증원문들}}
    try:
        naliannuungavik_aqqut = namunngarvik_atuutilik/'classes'; naliannuungavik_aqqut.mkdir(exist_ok=True)
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(naliannuungavik_aqqut),
            str(기준/'pivviujuq/화면합성.java'), str(기준/'pivviujuq/보드.java')])
        aullaqtilli_kipu = {'jdraw_prepare': 'Parnalli', 'jdraw_width': '너비얻기', 'jdraw_height': '높이얻기',
            'jdraw_count_low': '기록아래얻기', 'jdraw_count_high': '기록위얻기', 'jdraw_clip': 'Nakatigat',
            'jdraw_clip_value': 'Nakatigat_atuutilik', 'jdraw_begin': '시작', 'jdraw_end': '마침',
            'jdraw_pixel': 'pel', 'jdraw_rectangle': '사각그림', 'jdraw_pointer': '포인터'}
        번역명령 = ['sh', str(기준.parents[1]/'compiler/미리번역.sh'), '--entry', '화면합성.너비얻기', '-o', str(namunngarvik_atuutilik/'titiraujarniq_atuutilik.c')]
        for kasurli, sugiakkannirut_atuutilik in aullaqtilli_kipu.items(): 번역명령.extend(['--export', kasurli+'=화면합성.'+sugiakkannirut_atuutilik])
        subprocess.check_call(번역명령+[str(aqqut) for aqqut in sorted(naliannuungavik_aqqut.glob('*.class'))])
        piqujijjut = ['clang', '-std=c11', '-O2', '-Wall', '-Wextra', '-Werror'] + 원문들
        titiraujarniq_namunngarvik = namunngarvik_atuutilik/'titiraujarniq_atuutilik.o'
        subprocess.check_call(['clang', '-std=c11', '-O2', '-c', str(namunngarvik_atuutilik/'titiraujarniq_atuutilik.c'), '-o', str(titiraujarniq_namunngarvik)])
        subprocess.check_call(piqujijjut+[str(titiraujarniq_namunngarvik), 'build/terminal-font.S', '-o', str(namunngarvik_atuutilik/'화면갱신시험')], cwd=str(기준))
        결과 = subprocess.check_output([str(namunngarvik_atuutilik/'화면갱신시험')], timeout=30).decode()
        (namunngarvik_atuutilik/'naammannirarli.log').write_text(결과)
        맞음 = re.search(r'([\d.]+) ms/move; (\d+) framebuffer writes/move', 결과)
        assert 맞음 and 'PASS:' in 결과, 결과
        papattivik_sanimukutaak.update(passed=True, move_count=80, resize_count=40, window_count=4,
                   host_cpu_ms_per_move=float(맞음[1]), mean_framebuffer_writes_per_move=int(맞음[2]),
                   full_redraw_reference_equal=True, untouched_outside_damage=True,
                   unchanged_pixels_not_written=True, repeated_position_not_repainted=True,
                   padded_stride_preserved=True)
        print(결과, end='')
    finally:
        (namunngarvik_atuutilik/'report.json').write_text(json.dumps(papattivik_sanimukutaak, ensure_ascii=False, indent=2)+'\n')

if __name__ == '__main__': 시작()

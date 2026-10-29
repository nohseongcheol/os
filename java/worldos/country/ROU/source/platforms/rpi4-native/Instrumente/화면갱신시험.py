#!/usr/bin/env python3
"""real_date nucleu_VALUE 그리기 코드를 gazdă Memorie_date 화면에 연결해 부분 갱신을 검증한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

Project_rădăcină = Path(__file__).resolve().parents[1]

def Pornește():
    sursă_Fișiere = ['시험/화면갱신.c', 'mașină/화면그림.c', 'mașină/Terminal.c', 'mașină/widget.c']
    검증원문들 = sursă_Fișiere + ['SURSĂ/화면합성.java', 'SURSĂ/Avizier.java', '../../compiler/자바도구/기계어미리번역.java']
    destinație_VALUE = Project_rădăcină/'build/verification/redraw'; destinație_VALUE.mkdir(parents=True, exist_ok=True)
    LOG_RECORD = {'passed': False, 'test_environment': 'host CPU, Java AOT framebuffer composition and native terminal/widgets with memory framebuffer',
          'kernel_sha256': hashlib.sha256((Project_rădăcină/'build/kernel8.img').read_bytes()).hexdigest(),
          'source_sha256': {Nume: hashlib.sha256((Project_rădăcină/Nume).read_bytes()).hexdigest() for Nume in 검증원문들}}
    try:
        Clasă_cale = destinație_VALUE/'classes'; Clasă_cale.mkdir(exist_ok=True)
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(Clasă_cale),
            str(Project_rădăcină/'SURSĂ/화면합성.java'), str(Project_rădăcină/'SURSĂ/Avizier.java')])
        exporta_tabel = {'jdraw_prepare': 'Pregătiți', 'jdraw_width': '너비얻기', 'jdraw_height': '높이얻기',
            'jdraw_count_low': '기록아래얻기', 'jdraw_count_high': '기록위얻기', 'jdraw_clip': 'clip',
            'jdraw_clip_value': 'clip_VALUE', 'jdraw_begin': 'Pornește', 'jdraw_end': 'sfârșit',
            'jdraw_pixel': 'element_imagine', 'jdraw_rectangle': 'dreptunghi_umple', 'jdraw_pointer': 'cursor'}
        번역명령 = ['sh', str(Project_rădăcină.parents[1]/'compiler/미리번역.sh'), '--entry', '화면합성.너비얻기', '-o', str(destinație_VALUE/'desen_VALUE.c')]
        for Conectează, funcție_VALUE in exporta_tabel.items(): 번역명령.extend(['--export', Conectează+'=화면합성.'+funcție_VALUE])
        subprocess.check_call(번역명령+[str(Cale) for Cale in sorted(Clasă_cale.glob('*.class'))])
        Comandă = ['clang', '-std=c11', '-O2', '-Wall', '-Wextra', '-Werror'] + sursă_Fișiere
        desen_destinație = destinație_VALUE/'desen_VALUE.o'
        subprocess.check_call(['clang', '-std=c11', '-O2', '-c', str(destinație_VALUE/'desen_VALUE.c'), '-o', str(desen_destinație)])
        subprocess.check_call(Comandă+[str(desen_destinație), 'build/terminal-font.S', '-o', str(destinație_VALUE/'화면갱신시험')], cwd=str(Project_rădăcină))
        KR = subprocess.check_output([str(destinație_VALUE/'화면갱신시험')], timeout=30).decode()
        (destinație_VALUE/'valida.log').write_text(KR)
        맞음 = re.search(r'([\d.]+) ms/move; (\d+) framebuffer writes/move', KR)
        assert 맞음 and 'PASS:' in KR, KR
        LOG_RECORD.update(passed=True, move_count=80, resize_count=40, window_count=4,
                   host_cpu_ms_per_move=float(맞음[1]), mean_framebuffer_writes_per_move=int(맞음[2]),
                   full_redraw_reference_equal=True, untouched_outside_damage=True,
                   unchanged_pixels_not_written=True, repeated_position_not_repainted=True,
                   padded_stride_preserved=True)
        print(KR, end='')
    finally:
        (destinație_VALUE/'report.json').write_text(json.dumps(LOG_RECORD, ensure_ascii=False, indent=2)+'\n')

if __name__ == '__main__': Pornește()

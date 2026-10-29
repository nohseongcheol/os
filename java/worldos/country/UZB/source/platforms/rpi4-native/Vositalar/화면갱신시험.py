#!/usr/bin/env python3
"""real_ma_lumotlar o_zak_VALUE 그리기 코드를 tashkilotchi Xotira_ma_lumotlar 화면에 연결해 부분 갱신을 검증한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

Project_ildiz = Path(__file__).resolve().parents[1]

def Bajarish():
    manba_Fayllar = ['시험/화면갱신.c', '기계/화면그림.c', '기계/Terminal.c', '기계/vidjet.c']
    검증원문들 = manba_Fayllar + ['manba/화면합성.java', 'manba/yozuv_taxtasi.java', '../../compiler/자바도구/기계어미리번역.java']
    ko_chirish_joyi_VALUE = Project_ildiz/'build/verification/redraw'; ko_chirish_joyi_VALUE.mkdir(parents=True, exist_ok=True)
    LOG_satr = {'passed': False, 'test_environment': 'host CPU, Java AOT framebuffer composition and native terminal/widgets with memory framebuffer',
          'kernel_sha256': hashlib.sha256((Project_ildiz/'build/kernel8.img').read_bytes()).hexdigest(),
          'source_sha256': {Nomi: hashlib.sha256((Project_ildiz/Nomi).read_bytes()).hexdigest() for Nomi in 검증원문들}}
    try:
        Sinf_yo_l = ko_chirish_joyi_VALUE/'classes'; Sinf_yo_l.mkdir(exist_ok=True)
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(Sinf_yo_l),
            str(Project_ildiz/'manba/화면합성.java'), str(Project_ildiz/'manba/yozuv_taxtasi.java')])
        eksport_qilmoq_jadval = {'jdraw_prepare': 'Tayyorlamoq', 'jdraw_width': '너비얻기', 'jdraw_height': '높이얻기',
            'jdraw_count_low': '기록아래얻기', 'jdraw_count_high': '기록위얻기', 'jdraw_clip': 'klip',
            'jdraw_clip_value': 'klip_VALUE', 'jdraw_begin': 'Bajarish', 'jdraw_end': 'Tugatmoq',
            'jdraw_pixel': 'piksel', 'jdraw_rectangle': '사각그림', 'jdraw_pointer': 'kursor'}
        번역명령 = ['sh', str(Project_ildiz.parents[1]/'compiler/미리번역.sh'), '--entry', '화면합성.너비얻기', '-o', str(ko_chirish_joyi_VALUE/'chizish_VALUE.c')]
        for Ulanish, FUNCTION_VALUE in eksport_qilmoq_jadval.items(): 번역명령.extend(['--export', Ulanish+'=화면합성.'+FUNCTION_VALUE])
        subprocess.check_call(번역명령+[str(yo_l) for yo_l in sorted(Sinf_yo_l.glob('*.class'))])
        Buyruq = ['clang', '-std=c11', '-O2', '-Wall', '-Wextra', '-Werror'] + manba_Fayllar
        chizish_ko_chirish_joyi = ko_chirish_joyi_VALUE/'chizish_VALUE.o'
        subprocess.check_call(['clang', '-std=c11', '-O2', '-c', str(ko_chirish_joyi_VALUE/'chizish_VALUE.c'), '-o', str(chizish_ko_chirish_joyi)])
        subprocess.check_call(Buyruq+[str(chizish_ko_chirish_joyi), 'build/terminal-font.S', '-o', str(ko_chirish_joyi_VALUE/'화면갱신시험')], cwd=str(Project_ildiz))
        o_lchov = subprocess.check_output([str(ko_chirish_joyi_VALUE/'화면갱신시험')], timeout=30).decode()
        (ko_chirish_joyi_VALUE/'tasdiqlash.log').write_text(o_lchov)
        맞음 = re.search(r'([\d.]+) ms/move; (\d+) framebuffer writes/move', o_lchov)
        assert 맞음 and 'PASS:' in o_lchov, o_lchov
        LOG_satr.update(passed=True, move_count=80, resize_count=40, window_count=4,
                   host_cpu_ms_per_move=float(맞음[1]), mean_framebuffer_writes_per_move=int(맞음[2]),
                   full_redraw_reference_equal=True, untouched_outside_damage=True,
                   unchanged_pixels_not_written=True, repeated_position_not_repainted=True,
                   padded_stride_preserved=True)
        print(o_lchov, end='')
    finally:
        (ko_chirish_joyi_VALUE/'report.json').write_text(json.dumps(LOG_satr, ensure_ascii=False, indent=2)+'\n')

if __name__ == '__main__': Bajarish()

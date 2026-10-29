#!/usr/bin/env python3
"""faktisk_data kerne_VÆRDI Paint_skærmbillede 코드를 vært Hukommelse_data 화면에 연결해 부분 갱신을 검증한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

To_do_rod = Path(__file__).resolve().parents[1]

def Kør_2():
    kilde_Filer = ['시험/opdatere_skærmbillede.c', 'maskine/skærmbillede_tegning.c', 'maskine/Terminal.c', 'maskine/widget.c']
    검증원문들 = kilde_Filer + ['KILDE/화면합성.java', 'KILDE/Tavle.java', '../../compiler/자바도구/기계어미리번역.java']
    destination_VÆRDI = To_do_rod/'build/verification/redraw'; destination_VÆRDI.mkdir(parents=True, exist_ok=True)
    LOG_post = {'passed': False, 'test_environment': 'host CPU, Java AOT framebuffer composition and native terminal/widgets with memory framebuffer',
          'kernel_sha256': hashlib.sha256((To_do_rod/'build/kernel8.img').read_bytes()).hexdigest(),
          'source_sha256': {Navn: hashlib.sha256((To_do_rod/Navn).read_bytes()).hexdigest() for Navn in 검증원문들}}
    try:
        Hold_sti = destination_VÆRDI/'classes'; Hold_sti.mkdir(exist_ok=True)
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(Hold_sti),
            str(To_do_rod/'KILDE/화면합성.java'), str(To_do_rod/'KILDE/Tavle.java')])
        eksportere_tabel = {'jdraw_prepare': 'Tilrettelæg', 'jdraw_width': '너비얻기', 'jdraw_height': '높이얻기',
            'jdraw_count_low': '기록아래얻기', 'jdraw_count_high': '기록위얻기', 'jdraw_clip': 'klippe',
            'jdraw_clip_value': 'klippe_VÆRDI', 'jdraw_begin': 'Kør_2', 'jdraw_end': 'Udfør',
            'jdraw_pixel': 'pixel', 'jdraw_rectangle': 'rektangel_udfyld', 'jdraw_pointer': 'markør'}
        번역명령 = ['sh', str(To_do_rod.parents[1]/'compiler/미리번역.sh'), '--entry', '화면합성.너비얻기', '-o', str(destination_VÆRDI/'tegning_VÆRDI.c')]
        for Tilslut, FUNKTION_VÆRDI in eksportere_tabel.items(): 번역명령.extend(['--export', Tilslut+'=화면합성.'+FUNKTION_VÆRDI])
        subprocess.check_call(번역명령+[str(Sti) for Sti in sorted(Hold_sti.glob('*.class'))])
        Kommando = ['clang', '-std=c11', '-O2', '-Wall', '-Wextra', '-Werror'] + kilde_Filer
        tegning_destination = destination_VÆRDI/'tegning_VÆRDI.o'
        subprocess.check_call(['clang', '-std=c11', '-O2', '-c', str(destination_VÆRDI/'tegning_VÆRDI.c'), '-o', str(tegning_destination)])
        subprocess.check_call(Kommando+[str(tegning_destination), 'build/terminal-font.S', '-o', str(destination_VÆRDI/'skærmbillede_opdatere_test')], cwd=str(To_do_rod))
        KR = subprocess.check_output([str(destination_VÆRDI/'skærmbillede_opdatere_test')], timeout=30).decode()
        (destination_VÆRDI/'bekræfte_5fb2b747.log').write_text(KR)
        맞음 = re.search(r'([\d.]+) ms/move; (\d+) framebuffer writes/move', KR)
        assert 맞음 and 'PASS:' in KR, KR
        LOG_post.update(passed=True, move_count=80, resize_count=40, window_count=4,
                   host_cpu_ms_per_move=float(맞음[1]), mean_framebuffer_writes_per_move=int(맞음[2]),
                   full_redraw_reference_equal=True, untouched_outside_damage=True,
                   unchanged_pixels_not_written=True, repeated_position_not_repainted=True,
                   padded_stride_preserved=True)
        print(KR, end='')
    finally:
        (destination_VÆRDI/'report.json').write_text(json.dumps(LOG_post, ensure_ascii=False, indent=2)+'\n')

if __name__ == '__main__': Kør_2()

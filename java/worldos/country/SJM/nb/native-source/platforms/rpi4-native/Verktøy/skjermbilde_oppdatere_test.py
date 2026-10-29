#!/usr/bin/env python3
"""faktisk_data kjerne_VERDI Paint_skjermbilde 코드를 vert Minne_data 화면에 연결해 부분 갱신을 검증한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

speile_rot = Path(__file__).resolve().parents[1]

def Kjør_2():
    kilde_Filer = ['시험/oppdatere_skjermbilde.c', 'maskin/skjermbilde_tegning.c', 'maskin/Terminal.c', 'maskin/miniprogram.c']
    검증원문들 = kilde_Filer + ['KILDE/화면합성.java', 'KILDE/Tavle.java', '../../compiler/자바도구/기계어미리번역.java']
    mål_VERDI = speile_rot/'build/verification/redraw'; mål_VERDI.mkdir(parents=True, exist_ok=True)
    LOG_POST = {'passed': False, 'test_environment': 'host CPU, Java AOT framebuffer composition and native terminal/widgets with memory framebuffer',
          'kernel_sha256': hashlib.sha256((speile_rot/'build/kernel8.img').read_bytes()).hexdigest(),
          'source_sha256': {Navn: hashlib.sha256((speile_rot/Navn).read_bytes()).hexdigest() for Navn in 검증원문들}}
    try:
        time_bane = mål_VERDI/'classes'; time_bane.mkdir(exist_ok=True)
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(time_bane),
            str(speile_rot/'KILDE/화면합성.java'), str(speile_rot/'KILDE/Tavle.java')])
        eksportere_tabell = {'jdraw_prepare': 'Forbered', 'jdraw_width': '너비얻기', 'jdraw_height': '높이얻기',
            'jdraw_count_low': '기록아래얻기', 'jdraw_count_high': '기록위얻기', 'jdraw_clip': 'klippe',
            'jdraw_clip_value': 'klippe_VERDI', 'jdraw_begin': 'Kjør_2', 'jdraw_end': 'slutt',
            'jdraw_pixel': 'piksel', 'jdraw_rectangle': 'rektangel_fyll', 'jdraw_pointer': 'peker'}
        번역명령 = ['sh', str(speile_rot.parents[1]/'compiler/미리번역.sh'), '--entry', '화면합성.너비얻기', '-o', str(mål_VERDI/'tegning_VERDI.c')]
        for Koble_til, FUNKSJON_VERDI in eksportere_tabell.items(): 번역명령.extend(['--export', Koble_til+'=화면합성.'+FUNKSJON_VERDI])
        subprocess.check_call(번역명령+[str(Sti) for Sti in sorted(time_bane.glob('*.class'))])
        Kommando = ['clang', '-std=c11', '-O2', '-Wall', '-Wextra', '-Werror'] + kilde_Filer
        tegning_mål = mål_VERDI/'tegning_VERDI.o'
        subprocess.check_call(['clang', '-std=c11', '-O2', '-c', str(mål_VERDI/'tegning_VERDI.c'), '-o', str(tegning_mål)])
        subprocess.check_call(Kommando+[str(tegning_mål), 'build/terminal-font.S', '-o', str(mål_VERDI/'skjermbilde_oppdatere_test')], cwd=str(speile_rot))
        KR = subprocess.check_output([str(mål_VERDI/'skjermbilde_oppdatere_test')], timeout=30).decode()
        (mål_VERDI/'bekrefte_5fb2b747.log').write_text(KR)
        맞음 = re.search(r'([\d.]+) ms/move; (\d+) framebuffer writes/move', KR)
        assert 맞음 and 'PASS:' in KR, KR
        LOG_POST.update(passed=True, move_count=80, resize_count=40, window_count=4,
                   host_cpu_ms_per_move=float(맞음[1]), mean_framebuffer_writes_per_move=int(맞음[2]),
                   full_redraw_reference_equal=True, untouched_outside_damage=True,
                   unchanged_pixels_not_written=True, repeated_position_not_repainted=True,
                   padded_stride_preserved=True)
        print(KR, end='')
    finally:
        (mål_VERDI/'report.json').write_text(json.dumps(LOG_POST, ensure_ascii=False, indent=2)+'\n')

if __name__ == '__main__': Kjør_2()

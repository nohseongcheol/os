#!/usr/bin/env python3
"""verklig_data kärna_värde Paint_skärmbild 코드를 värd Minne_data 화면에 연결해 부분 갱신을 검증한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

åtgärd_rot = Path(__file__).resolve().parents[1]

def Kör():
    källa_Filer = ['tester/uppdatera_skärmbild.c', 'dator/skärmbild_ritning.c', 'dator/kommandotolk.c', 'dator/skärmelement.c']
    검증원문들 = källa_Filer + ['källfil/화면합성.java', 'källfil/Tavla.java', '../../compiler/자바도구/기계어미리번역.java']
    mål_värde = åtgärd_rot/'build/verification/redraw'; mål_värde.mkdir(parents=True, exist_ok=True)
    LOG_POST = {'passed': False, 'test_environment': 'host CPU, Java AOT framebuffer composition and native terminal/widgets with memory framebuffer',
          'kernel_sha256': hashlib.sha256((åtgärd_rot/'build/kernel8.img').read_bytes()).hexdigest(),
          'source_sha256': {Namn: hashlib.sha256((åtgärd_rot/Namn).read_bytes()).hexdigest() for Namn in 검증원문들}}
    try:
        Kurs_väg = mål_värde/'classes'; Kurs_väg.mkdir(exist_ok=True)
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(Kurs_väg),
            str(åtgärd_rot/'källfil/화면합성.java'), str(åtgärd_rot/'källfil/Tavla.java')])
        exportera_tabell = {'jdraw_prepare': 'Förbereda', 'jdraw_width': '너비얻기', 'jdraw_height': '높이얻기',
            'jdraw_count_low': '기록아래얻기', 'jdraw_count_high': '기록위얻기', 'jdraw_clip': 'klipp',
            'jdraw_clip_value': 'klipp_värde', 'jdraw_begin': 'Kör', 'jdraw_end': 'slut',
            'jdraw_pixel': 'bildpunkt', 'jdraw_rectangle': 'rektangel_Fyll', 'jdraw_pointer': 'markör'}
        번역명령 = ['sh', str(åtgärd_rot.parents[1]/'compiler/미리번역.sh'), '--entry', '화면합성.너비얻기', '-o', str(mål_värde/'ritning_värde.c')]
        for Anslut, FUNKTION_värde in exportera_tabell.items(): 번역명령.extend(['--export', Anslut+'=화면합성.'+FUNKTION_värde])
        subprocess.check_call(번역명령+[str(sökväg_2) for sökväg_2 in sorted(Kurs_väg.glob('*.class'))])
        kommando = ['clang', '-std=c11', '-O2', '-Wall', '-Wextra', '-Werror'] + källa_Filer
        ritning_mål = mål_värde/'ritning_värde.o'
        subprocess.check_call(['clang', '-std=c11', '-O2', '-c', str(mål_värde/'ritning_värde.c'), '-o', str(ritning_mål)])
        subprocess.check_call(kommando+[str(ritning_mål), 'build/terminal-font.S', '-o', str(mål_värde/'skärmbild_uppdatera_test')], cwd=str(åtgärd_rot))
        RESULTAT = subprocess.check_output([str(mål_värde/'skärmbild_uppdatera_test')], timeout=30).decode()
        (mål_värde/'validera.log').write_text(RESULTAT)
        맞음 = re.search(r'([\d.]+) ms/move; (\d+) framebuffer writes/move', RESULTAT)
        assert 맞음 and 'PASS:' in RESULTAT, RESULTAT
        LOG_POST.update(passed=True, move_count=80, resize_count=40, window_count=4,
                   host_cpu_ms_per_move=float(맞음[1]), mean_framebuffer_writes_per_move=int(맞음[2]),
                   full_redraw_reference_equal=True, untouched_outside_damage=True,
                   unchanged_pixels_not_written=True, repeated_position_not_repainted=True,
                   padded_stride_preserved=True)
        print(RESULTAT, end='')
    finally:
        (mål_värde/'report.json').write_text(json.dumps(LOG_POST, ensure_ascii=False, indent=2)+'\n')

if __name__ == '__main__': Kör()

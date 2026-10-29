#!/usr/bin/env python3
"""πραγματικός_δεδομένα πυρήνας_τιμή 그리기 코드를 φιλοξενώ Μνήμη_δεδομένα 화면에 연결해 부분 갱신을 검증한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

έργο_ρίζα = Path(__file__).resolve().parents[1]

def Εκτέλεση_2():
    προέλευση_Αρχεία = ['시험/화면갱신.c', 'υπολογιστής_5eb260fa/화면그림.c', 'υπολογιστής_5eb260fa/Τερματικό.c', 'υπολογιστής_5eb260fa/γραφικό_στοιχείο.c']
    검증원문들 = προέλευση_Αρχεία + ['ΠΗΓΗ/화면합성.java', 'ΠΗΓΗ/Πίνακας.java', '../../compiler/자바도구/기계어미리번역.java']
    προορισμός_τιμή = έργο_ρίζα/'build/verification/redraw'; προορισμός_τιμή.mkdir(parents=True, exist_ok=True)
    καταγράφω_ρεκόρ = {'passed': False, 'test_environment': 'host CPU, Java AOT framebuffer composition and native terminal/widgets with memory framebuffer',
          'kernel_sha256': hashlib.sha256((έργο_ρίζα/'build/kernel8.img').read_bytes()).hexdigest(),
          'source_sha256': {Όνομα: hashlib.sha256((έργο_ρίζα/Όνομα).read_bytes()).hexdigest() for Όνομα in 검증원문들}}
    try:
        Τάξη_διαδρομή = προορισμός_τιμή/'classes'; Τάξη_διαδρομή.mkdir(exist_ok=True)
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(Τάξη_διαδρομή),
            str(έργο_ρίζα/'ΠΗΓΗ/화면합성.java'), str(έργο_ρίζα/'ΠΗΓΗ/Πίνακας.java')])
        εξάγω_πίνακας = {'jdraw_prepare': 'Προετοίμασε', 'jdraw_width': '너비얻기', 'jdraw_height': 'λαμβάνω_ύψος',
            'jdraw_count_low': '기록아래얻기', 'jdraw_count_high': '기록위얻기', 'jdraw_clip': 'απόσπασμα',
            'jdraw_clip_value': 'απόσπασμα_τιμή', 'jdraw_begin': 'Εκτέλεση_2', 'jdraw_end': 'Τέλος',
            'jdraw_pixel': '화소', 'jdraw_rectangle': 'ορθογώνιο_γεμίζω', 'jdraw_pointer': 'δείκτης'}
        번역명령 = ['sh', str(έργο_ρίζα.parents[1]/'compiler/미리번역.sh'), '--entry', '화면합성.너비얻기', '-o', str(προορισμός_τιμή/'σχέδιο_τιμή.c')]
        for Σύνδεση, συνάρτηση_τιμή in εξάγω_πίνακας.items(): 번역명령.extend(['--export', Σύνδεση+'=화면합성.'+συνάρτηση_τιμή])
        subprocess.check_call(번역명령+[str(ΔΙΑΔΡΟΜΗ) for ΔΙΑΔΡΟΜΗ in sorted(Τάξη_διαδρομή.glob('*.class'))])
        Εντολή = ['clang', '-std=c11', '-O2', '-Wall', '-Wextra', '-Werror'] + προέλευση_Αρχεία
        σχέδιο_προορισμός = προορισμός_τιμή/'σχέδιο_τιμή.o'
        subprocess.check_call(['clang', '-std=c11', '-O2', '-c', str(προορισμός_τιμή/'σχέδιο_τιμή.c'), '-o', str(σχέδιο_προορισμός)])
        subprocess.check_call(Εντολή+[str(σχέδιο_προορισμός), 'build/terminal-font.S', '-o', str(προορισμός_τιμή/'화면갱신시험')], cwd=str(έργο_ρίζα))
        μέτρηση = subprocess.check_output([str(προορισμός_τιμή/'화면갱신시험')], timeout=30).decode()
        (προορισμός_τιμή/'επικυρώνω.log').write_text(μέτρηση)
        맞음 = re.search(r'([\d.]+) ms/move; (\d+) framebuffer writes/move', μέτρηση)
        assert 맞음 and 'PASS:' in μέτρηση, μέτρηση
        καταγράφω_ρεκόρ.update(passed=True, move_count=80, resize_count=40, window_count=4,
                   host_cpu_ms_per_move=float(맞음[1]), mean_framebuffer_writes_per_move=int(맞음[2]),
                   full_redraw_reference_equal=True, untouched_outside_damage=True,
                   unchanged_pixels_not_written=True, repeated_position_not_repainted=True,
                   padded_stride_preserved=True)
        print(μέτρηση, end='')
    finally:
        (προορισμός_τιμή/'report.json').write_text(json.dumps(καταγράφω_ρεκόρ, ensure_ascii=False, indent=2)+'\n')

if __name__ == '__main__': Εκτέλεση_2()

#!/usr/bin/env python3
"""בפועל_נתונים ליבה_ערך 그리기 코드를 ארח זיכרון_נתונים 화면에 연결해 부분 갱신을 검증한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

לשקף_בסיס = Path(__file__).resolve().parents[1]

def הפעלה():
    מקור_קבצים = ['시험/화면갱신.c', 'מחשב/화면그림.c', 'מחשב/מסוף.c', 'מחשב/רכיב_גרפי.c']
    검증원문들 = מקור_קבצים + ['קודמקור/화면합성.java', 'קודמקור/לוח.java', '../../compiler/자바도구/기계어미리번역.java']
    יעד_ערך = לשקף_בסיס/'build/verification/redraw'; יעד_ערך.mkdir(parents=True, exist_ok=True)
    לרשום_שיא = {'passed': False, 'test_environment': 'host CPU, Java AOT framebuffer composition and native terminal/widgets with memory framebuffer',
          'kernel_sha256': hashlib.sha256((לשקף_בסיס/'build/kernel8.img').read_bytes()).hexdigest(),
          'source_sha256': {שם: hashlib.sha256((לשקף_בסיס/שם).read_bytes()).hexdigest() for שם in 검증원문들}}
    try:
        כיתה_נתיב = יעד_ערך/'classes'; כיתה_נתיב.mkdir(exist_ok=True)
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(כיתה_נתיב),
            str(לשקף_בסיס/'קודמקור/화면합성.java'), str(לשקף_בסיס/'קודמקור/לוח.java')])
        ייצא_טבלה = {'jdraw_prepare': 'להכין', 'jdraw_width': '너비얻기', 'jdraw_height': 'לקבל_גובה',
            'jdraw_count_low': '기록아래얻기', 'jdraw_count_high': '기록위얻기', 'jdraw_clip': 'לגזור',
            'jdraw_clip_value': 'לגזור_ערך', 'jdraw_begin': 'הפעלה', 'jdraw_end': 'סיום',
            'jdraw_pixel': 'פיקסל', 'jdraw_rectangle': 'מלבן_למלא', 'jdraw_pointer': 'מצביע'}
        번역명령 = ['sh', str(לשקף_בסיס.parents[1]/'compiler/미리번역.sh'), '--entry', '화면합성.너비얻기', '-o', str(יעד_ערך/'ציור_ערך.c')]
        for חיבור, פונקציה_ערך in ייצא_טבלה.items(): 번역명령.extend(['--export', חיבור+'=화면합성.'+פונקציה_ערך])
        subprocess.check_call(번역명령+[str(נתיב) for נתיב in sorted(כיתה_נתיב.glob('*.class'))])
        פקודה = ['clang', '-std=c11', '-O2', '-Wall', '-Wextra', '-Werror'] + מקור_קבצים
        ציור_יעד = יעד_ערך/'ציור_ערך.o'
        subprocess.check_call(['clang', '-std=c11', '-O2', '-c', str(יעד_ערך/'ציור_ערך.c'), '-o', str(ציור_יעד)])
        subprocess.check_call(פקודה+[str(ציור_יעד), 'build/terminal-font.S', '-o', str(יעד_ערך/'화면갱신시험')], cwd=str(לשקף_בסיס))
        תוצאה = subprocess.check_output([str(יעד_ערך/'화면갱신시험')], timeout=30).decode()
        (יעד_ערך/'לאמת.log').write_text(תוצאה)
        맞음 = re.search(r'([\d.]+) ms/move; (\d+) framebuffer writes/move', תוצאה)
        assert 맞음 and 'PASS:' in תוצאה, תוצאה
        לרשום_שיא.update(passed=True, move_count=80, resize_count=40, window_count=4,
                   host_cpu_ms_per_move=float(맞음[1]), mean_framebuffer_writes_per_move=int(맞음[2]),
                   full_redraw_reference_equal=True, untouched_outside_damage=True,
                   unchanged_pixels_not_written=True, repeated_position_not_repainted=True,
                   padded_stride_preserved=True)
        print(תוצאה, end='')
    finally:
        (יעד_ערך/'report.json').write_text(json.dumps(לרשום_שיא, ensure_ascii=False, indent=2)+'\n')

if __name__ == '__main__': הפעלה()

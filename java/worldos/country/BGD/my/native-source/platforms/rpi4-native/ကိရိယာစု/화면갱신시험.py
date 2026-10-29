#!/usr/bin/env python3
"""တကယ့်ဒေတာ အူတိုင်တန်ဖိုး မျက်နှာပြင်ဆေးခြယ် 코드를 အိမ်ရှင် မှတ်ဉာဏ်ဒေတာ 화면에 연결해 အစိတ်အပိုင်းတန်ဖိုး 갱신을 검증한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

စီမံကိန်းအမြစ် = Path(__file__).resolve().parents[1]

def လုပ်ဆောင်():
    မူရင်းကုဒ်ဖိုင်များ = ['စမ်းသပ်မှု/화면갱신.c', 'စက်/မျက်နှာပြင်ပုံရေးဆွဲမှု.c', 'စက်/အဆုံးသုံးမျက်နှာပြင်.c', 'စက်/မြင်ကွင်းအစိတ်အပိုင်း.c']
    검증원문들 = မူရင်းကုဒ်ဖိုင်များ + ['မူရင်းကုဒ်/မျက်နှာပြင်ပေါင်းစပ်.java', 'မူရင်းကုဒ်/ဆားကစ်ပြား.java', '../../compiler/Javaကိရိယာ/ကြိုတင်ဘာသာပြန်.java']
    ဦးတည်ရာတန်ဖိုး = စီမံကိန်းအမြစ်/'build/verification/redraw'; ဦးတည်ရာတန်ဖိုး.mkdir(parents=True, exist_ok=True)
    မှတ်တမ်းမှတ်တမ်းတစ်ခု = {'passed': False, 'test_environment': 'host CPU, Java AOT framebuffer composition and native terminal/widgets with memory framebuffer',
          'kernel_sha256': hashlib.sha256((စီမံကိန်းအမြစ်/'build/kernel8.img').read_bytes()).hexdigest(),
          'source_sha256': {အမည်: hashlib.sha256((စီမံကိန်းအမြစ်/အမည်).read_bytes()).hexdigest() for အမည် in 검증원문들}}
    try:
        အတန်းလမ်းကြောင်း = ဦးတည်ရာတန်ဖိုး/'classes'; အတန်းလမ်းကြောင်း.mkdir(exist_ok=True)
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(အတန်းလမ်းကြောင်း),
            str(စီမံကိန်းအမြစ်/'မူရင်းကုဒ်/မျက်နှာပြင်ပေါင်းစပ်.java'), str(စီမံကိန်းအမြစ်/'မူရင်းကုဒ်/ဆားကစ်ပြား.java')])
        တင်ပို့ဇယား = {'jdraw_prepare': 'ပြင်ဆင်', 'jdraw_width': 'အနံယူ', 'jdraw_height': 'အမြင့်ယူ',
            'jdraw_count_low': 'ရေတွက်သူနိမ့်ယူ', 'jdraw_count_high': 'ရေတွက်သူမြင့်ယူ', 'jdraw_clip': 'ဖြတ်နယ်ပယ်',
            'jdraw_clip_value': 'ဖြတ်နယ်ပယ်တန်ဖိုး', 'jdraw_begin': 'လုပ်ဆောင်', 'jdraw_end': 'ပြီးဆုံး',
            'jdraw_pixel': 'ပုံမှတ်', 'jdraw_rectangle': 'စတုဂံဖြည့်', 'jdraw_pointer': 'ညွှန်တံ'}
        ဘာသာပြန်မှုအမိန့် = ['sh', str(စီမံကိန်းအမြစ်.parents[1]/'compiler/미리번역.sh'), '--entry', 'မျက်နှာပြင်ပေါင်းစပ်.အနံယူ', '-o', str(ဦးတည်ရာတန်ဖိုး/'ပုံဆွဲမှု.c')]
        for ချိတ်ဆက်, လုပ်ဆောင်ချက် in တင်ပို့ဇယား.items(): ဘာသာပြန်မှုအမိန့်.extend(['--export', ချိတ်ဆက်+'=မျက်နှာပြင်ပေါင်းစပ်.'+လုပ်ဆောင်ချက်])
        subprocess.check_call(ဘာသာပြန်မှုအမိန့်+[str(လမ်း) for လမ်း in sorted(အတန်းလမ်းကြောင်း.glob('*.class'))])
        အမိန့် = ['clang', '-std=c11', '-O2', '-Wall', '-Wextra', '-Werror'] + မူရင်းကုဒ်ဖိုင်များ
        ပုံရေးဆွဲမှုဦးတည်ရာ = ဦးတည်ရာတန်ဖိုး/'ပုံဆွဲမှု.o'
        subprocess.check_call(['clang', '-std=c11', '-O2', '-c', str(ဦးတည်ရာတန်ဖိုး/'ပုံဆွဲမှု.c'), '-o', str(ပုံရေးဆွဲမှုဦးတည်ရာ)])
        subprocess.check_call(အမိန့်+[str(ပုံရေးဆွဲမှုဦးတည်ရာ), 'build/terminal-font.S', '-o', str(ဦးတည်ရာတန်ဖိုး/'화면갱신시험')], cwd=str(စီမံကိန်းအမြစ်))
        ရလဒ် = subprocess.check_output([str(ဦးတည်ရာတန်ဖိုး/'화면갱신시험')], timeout=30).decode()
        (ဦးတည်ရာတန်ဖိုး/'မှန်ကန်ကြောင်းစစ်.log').write_text(ရလဒ်)
        맞음 = re.search(r'([\d.]+) ms/move; (\d+) framebuffer writes/move', ရလဒ်)
        assert 맞음 and 'PASS:' in ရလဒ်, ရလဒ်
        မှတ်တမ်းမှတ်တမ်းတစ်ခု.update(passed=True, move_count=80, resize_count=40, window_count=4,
                   host_cpu_ms_per_move=float(맞음[1]), mean_framebuffer_writes_per_move=int(맞음[2]),
                   full_redraw_reference_equal=True, untouched_outside_damage=True,
                   unchanged_pixels_not_written=True, repeated_position_not_repainted=True,
                   padded_stride_preserved=True)
        print(ရလဒ်, end='')
    finally:
        (ဦးတည်ရာတန်ဖိုး/'report.json').write_text(json.dumps(မှတ်တမ်းမှတ်တမ်းတစ်ခု, ensure_ascii=False, indent=2)+'\n')

if __name__ == '__main__': လုပ်ဆောင်()

#!/usr/bin/env python3
"""ယခင်အချက်အလက်တစ်ခု Python 경로를 Java 미리 번역기에 연결한다. မူရင်းကုဒ်ဘာသာပြန်ဆို 구현은 Javaကိရိယာ/에 있다."""
from pathlib import Path
import subprocess
import sys
import tempfile
from ဘာသာပြန်စက် import ဘာသာပြန်မှုအမှား

စီမံကိန်းအမြစ် = Path(__file__).resolve().parent

class စက်ကုဒ်ဘာသာပြန်စက်:
    def __init__(자신, အဝင်အတန်းများ, လုပ်ဆောင်မှုဦးတည်ချက်='kernel', ပုံတင်မှတ်ဉာဏ်စကားလုံးအရေအတွက်=262144):
        자신.လမ်းများ = [ဒေတာ.လမ်း for ဒေတာ in အဝင်အတန်းများ]
        자신.လုပ်ဆောင်မှုဦးတည်ချက် = လုပ်ဆောင်မှုဦးတည်ချက်
        자신.ပုံတင်မှတ်ဉာဏ်စကားလုံးအရေအတွက် = ပုံတင်မှတ်ဉာဏ်စကားလုံးအရေအတွက်

    def ထုတ်လုပ်(자신, အချက်အမှတ်တစ်ခု, ထုတ်ပေးစာရင်း, 범용문자표기=False):
        with tempfile.TemporaryDirectory(prefix='java-aot-') as အလုပ်:
            ရလဒ်လမ်းကြောင်း = Path(အလုပ်)/'generated.c'
            အမိန့် = ['sh', str(စီမံကိန်းအမြစ်/'미리번역.sh'), '--entry', အချက်အမှတ်တစ်ခု,
                    '--profile', 자신.လုပ်ဆောင်မှုဦးတည်ချက်, '--heap-words', str(자신.ပုံတင်မှတ်ဉာဏ်စကားလုံးအရေအတွက်), '-o', str(ရလဒ်လမ်းကြောင်း)]
            if 범용문자표기: အမိန့်.append('--ucn')
            for သတ်မှတ်ပေးတန်ဖိုး in ထုတ်ပေးစာရင်း: အမိန့်.extend(['--export', သတ်မှတ်ပေးတန်ဖိုး])
            အမိန့်.extend(str(လမ်း) for လမ်း in 자신.လမ်းများ)
            ရလဒ် = subprocess.run(အမိန့်, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if ရလဒ်.returncode: raise ဘာသာပြန်မှုအမှား(ရလဒ်.stderr.decode('utf-8', 'replace'))
            return ရလဒ်လမ်းကြောင်း.read_text()

def လုပ်ဆောင်():
    raise SystemExit(subprocess.call(['sh', str(စီမံကိန်းအမြစ်/'미리번역.sh')] + sys.argv[1:]))

if __name__ == '__main__': လုပ်ဆောင်()

#!/usr/bin/env python3
"""အချက်နောက်တွဲ Python 패키지 없이 မြန်မာ Java 메서드의 결과를 받는다."""
import argparse
import os
from pathlib import Path
import subprocess


def ကုဒ်အမှတ်တစ်ခုအရေအတွက်(အကြောင်းအရာတန်ဖိုး, စာကြည့်တိုက်, အတန်းဖိုင်တွဲ):
    ရလဒ် = subprocess.run(
        ['java', '-Dfile.encoding=UTF-8', '-cp',
         os.pathsep.join([str(စာကြည့်တိုက်), str(အတန်းဖိုင်တွဲ)]), 'စာသားအမိန့်', အကြောင်းအရာတန်ဖိုး],
        check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        encoding='utf-8', timeout=60)
    return int(ရလဒ်.stdout.strip())


if __name__ == '__main__':
    ပေးအချက်များသဒ္ဒါခွဲခြမ်း = argparse.ArgumentParser(description=__doc__)
    ပေးအချက်များသဒ္ဒါခွဲခြမ်း.add_argument('--jar', type=Path, default=Path('/opt/jkoros/lib/မြန်မာJava.jar'))
    ပေးအချက်များသဒ္ဒါခွဲခြမ်း.add_argument('--classes', type=Path, default=Path(__file__).resolve().parent / 'classes')
    ပေးအချက်များသဒ္ဒါခွဲခြမ်း.add_argument('--text', default='한글 😀')
    အချက်များ = ပေးအချက်များသဒ္ဒါခွဲခြမ်း.parse_args()
    print('Python → မြန်မာ.Java.အက္ခရာ.ကုဒ်အမှတ်တစ်ခုအရေအတွက်:',
          ကုဒ်အမှတ်တစ်ခုအရေအတွက်(အချက်များ.text, အချက်များ.jar, အချက်များ.classes))

#!/usr/bin/env python3
"""기존 လမ်း 호환 အချက်အမှတ်တစ်ခု. တကယ့်ဒေတာ အကောင်အထည်ဖော်မှု: ../ကိရိယာစု/ဟန်ဂုအဝင်စမ်းသပ်.py"""
import importlib as တန်ဖိုးယူ
import sys as လည်ပတ်မှုစနစ်တန်ဖိုး
from pathlib import Path as လမ်း
လည်ပတ်မှုစနစ်တန်ဖိုး.path.insert(0, str(လမ်း(__file__).resolve().parents[1] / 'ကိရိယာစု'))
if __name__ == '__main__':
    import runpy as ပရိုဂရမ်စက်နှိုးကိရိယာ
    ပရိုဂရမ်စက်နှိုးကိရိယာ.run_module('ဟန်ဂုအဝင်စမ်းသပ်', run_name='__main__', alter_sys=True)
else:
    အကောင်အထည်ဖော်မှု = တန်ဖိုးယူ.import_module('ဟန်ဂုအဝင်စမ်းသပ်')
    ချိတ်ဆက်ပုံတန်ဖိုး = {'expected': '예상결과', 'Keyboard': 'လက်ကွက်', 'press': '글쇠누르기', 'self': '자신', 'test_modes_repeat_and_commit': 'test_전환반복확정', 'keys': '누름열', 'test_paste_and_unicode': 'test_붙이기유니코드', 'data': 'ဒေတာ', 'key': '누름값', 'send': 'ပို့', 'test_words': 'စကားလုံးများစမ်းသပ်', 'InputTests': 'ဟန်ဂုအဝင်စမ်းသပ်', 'test_backspace': 'test_앞글자지우기', 'symbol': 'သင်္ကေတတန်ဖိုး', 'char': 'အက္ခရာဒေတာ', 'type': 'ပုံစံအမျိုးအစား'}
    for ယခင်အချက်အလက်တစ်ခု, လက်ရှိအချက်အလက်တစ်ခု in ချိတ်ဆက်ပုံတန်ဖိုး.items():
        if hasattr(အကောင်အထည်ဖော်မှု, လက်ရှိအချက်အလက်တစ်ခု): globals()[ယခင်အချက်အလက်တစ်ခု] = getattr(အကောင်အထည်ဖော်မှု, လက်ရှိအချက်အလက်တစ်ခု)

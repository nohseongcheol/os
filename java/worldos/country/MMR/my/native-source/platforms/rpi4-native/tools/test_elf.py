#!/usr/bin/env python3
"""기존 လမ်း 호환 အချက်အမှတ်တစ်ခု. တကယ့်ဒေတာ အကောင်အထည်ဖော်မှု: ../ကိရိယာစု/ELFစမ်းသပ်.py"""
import importlib as တန်ဖိုးယူ
import sys as လည်ပတ်မှုစနစ်တန်ဖိုး
from pathlib import Path as လမ်း
လည်ပတ်မှုစနစ်တန်ဖိုး.path.insert(0, str(လမ်း(__file__).resolve().parents[1] / 'ကိရိယာစု'))
if __name__ == '__main__':
    import runpy as ပရိုဂရမ်စက်နှိုးကိရိယာ
    ပရိုဂရမ်စက်နှိုးကိရိယာ.run_module('ELFစမ်းသပ်', run_name='__main__', alter_sys=True)
else:
    အကောင်အထည်ဖော်မှု = တန်ဖိုးယူ.import_module('ELFစမ်းသပ်')
    ချိတ်ဆက်ပုံတန်ဖိုး = {'out': 'ရလဒ်ဒေတာ', 'expected': '예상결과', 'phoff': 'ပရိုဂရမ်ခေါင်းစီးအရွေ့', 'offset': 'အရွေ့တန်ဖိုး', 'invalid': 'မမှန်ကန်ဒေတာ', 'path': 'လမ်း', 'executable': 'စက်ဖိုင်စက်ပုံရိပ်', 'rejected': '거부결과', 'linux_example': '리눅스예제', 'original': 'မူရင်း', 'result': 'ရလဒ်', 'format_': '형식지정', 'main': 'လုပ်ဆောင်', 'content': 'အကြောင်းအရာတန်ဖိုး', 'source': 'မူရင်းဒေတာ', 'name': 'အမည်', 'reference': '비교기준', 'ROOT': 'စီမံကိန်းအမြစ်', 'value': 'တန်ဖိုး', 'report': '검증기록'}
    for ယခင်အချက်အလက်တစ်ခု, လက်ရှိအချက်အလက်တစ်ခု in ချိတ်ဆက်ပုံတန်ဖိုး.items():
        if hasattr(အကောင်အထည်ဖော်မှု, လက်ရှိအချက်အလက်တစ်ခု): globals()[ယခင်အချက်အလက်တစ်ခု] = getattr(အကောင်အထည်ဖော်မှု, လက်ရှိအချက်အလက်တစ်ခု)

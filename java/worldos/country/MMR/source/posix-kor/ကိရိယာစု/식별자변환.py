#!/usr/bin/env python3
"""မြန်မာ C 식별자만 UCN으로 옮긴다. အက္ခရာစဉ်·အက္ခရာ·주석·include 파일명은 보존한다."""
import argparse
from pathlib import Path
import re

သင်္ကေတစကားလုံးတန်ဖိုး = re.compile(r'(?P<보존>//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|^[ \t]*#[ \t]*include[ \t]*<[^>]*>)|(?P<သတ်မှတ်နံပါတ်တန်ဖိုး>[^\W\d]\w*)', re.S | re.M)

def တန်ဖိုးပြောင်းလဲ(မူရင်းကုဒ်):
    def တန်ဖိုးအစားထိုး(ဖြစ်သောညီ):
        if ဖြစ်သောညီ.lastgroup == '보존':
            return ဖြစ်သောညီ[0]
        return ''.join(အက္ခရာတန်ဖိုး if ord(အက္ခရာတန်ဖိုး) < 128 else
                       ('\\u%04x' if ord(အက္ခရာတန်ဖိုး) <= 65535 else '\\U%08x') % ord(အက္ခရာတန်ဖိုး)
                       for အက္ခရာတန်ဖိုး in ဖြစ်သောညီ[0])
    return သင်္ကေတစကားလုံးတန်ဖိုး.sub(တန်ဖိုးအစားထိုး, မူရင်းကုဒ်)

def စက်မောင်း():
    해석기 = argparse.ArgumentParser()
    해석기.add_argument('မူရင်း', type=Path)
    해석기.add_argument('အထွက်', type=Path)
    အချက်များ = 해석기.parse_args()
    for ဖိုင် in sorted(အချက်များ.မူရင်း.rglob('*')):
        if ဖိုင်.suffix not in ('.c', '.h'):
            continue
        အထွက် = အချက်များ.အထွက် / ဖိုင်.relative_to(အချက်များ.မူရင်း)
        အထွက်.parent.mkdir(parents=True, exist_ok=True)
        အသစ်မူရင်းကုဒ် = တန်ဖိုးပြောင်းလဲ(ဖိုင်.read_text())
        if not အထွက်.exists() or အထွက်.read_text() != အသစ်မူရင်းကုဒ်:
            အထွက်.write_text(အသစ်မူရင်းကုဒ်)

if __name__ == '__main__':
    စက်မောင်း()

#!/usr/bin/env python3
"""명시한 Java မူရင်းကုဒ်အပင်ဖွဲ့စည်းပုံ/အတန်းတန်ဖိုး 파일을 စက်တင် 시 RAM 파일체계로 가져온다."""
import argparse
from pathlib import Path
import re
import struct


def စက်ဖိုင်ထုပ်ပိုး(항목들):
    ဖိုင်အချက်များ = []
    အမည်များစာရင်း = {'Hello.java'}
    명시 = set()
    for အချက်တန်ဖိုး in 항목들:
        if '=' not in အချက်တန်ဖိုး:
            raise ValueError('expected NAME=PATH: ' + အချက်တန်ဖိုး)
        အမည်, လမ်း = အချက်တန်ဖိုး.split('=', 1)
        if not re.fullmatch(r'[A-Za-z0-9_-][A-Za-z0-9_.-]{0,62}', အမည်) or အမည် in 명시:
            raise ValueError('invalid or duplicate file name: ' + အမည်)
        명시.add(အမည်)
        အမည်များစာရင်း.add(အမည်)
        ဒေတာ = Path(လမ်း).read_bytes()
        if len(ဒေတာ) > 16384:
            raise ValueError('file exceeds 16384 bytes: ' + အမည်)
        ဖိုင်အချက်များ.append((အမည်.encode('ascii'), ဒေတာ))
    if len(အမည်များစာရင်း) > 8:
        raise ValueError('RAM file limit: 8 files including the default Hello.java')
    ရလဒ် = bytearray(struct.pack('<4sI', b'JKJF', len(ဖိုင်အချက်များ)))
    ရလဒ်.extend(bytes(72 * len(ဖိုင်အချက်များ)))
    for ကိန်းတန်ဖိုး, (အမည်, ဒေတာ) in enumerate(ဖိုင်အချက်များ):
        struct.pack_into('<64sII', ရလဒ်, 8 + ကိန်းတန်ဖိုး * 72, အမည်, len(ရလဒ်), len(ဒေတာ))
        ရလဒ်.extend(ဒေတာ)
    return bytes(ရလဒ်)


if __name__ == '__main__':
    တန်ဖိုးသဒ္ဒါခွဲခြမ်း = argparse.ArgumentParser(description=__doc__)
    တန်ဖိုးသဒ္ဒါခွဲခြမ်း.add_argument('-o', required=True)
    တန်ဖိုးသဒ္ဒါခွဲခြမ်း.add_argument('files', nargs='*', help='NAME=PATH')
    အချက်များ = တန်ဖိုးသဒ္ဒါခွဲခြမ်း.parse_args()
    try:
        ဒေတာ = စက်ဖိုင်ထုပ်ပိုး(အချက်များ.files)
        ဦးတည်ရာတန်ဖိုး = Path(အချက်များ.o)
        if not ဦးတည်ရာတန်ဖိုး.exists() or ဦးတည်ရာတန်ဖိုး.read_bytes() != ဒေတာ:
            ယာယီတန်ဖိုး = ဦးတည်ရာတန်ဖိုး.with_name(ဦးတည်ရာတန်ဖိုး.name + '.tmp')
            ယာယီတန်ဖိုး.write_bytes(ဒေတာ)
            ယာယီတန်ဖိုး.replace(ဦးတည်ရာတန်ဖိုး)
    except (ValueError, OSError) as အမှား:
        တန်ဖိုးသဒ္ဒါခွဲခြမ်း.error(str(အမှား))

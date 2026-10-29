#!/usr/bin/env python3
"""명시한 သုံးစွဲသူ ELF만 ဖတ် 전용 JKAP 묶음에 넣는다. 기존 디스크는 사용하지 않는다."""
import argparse
from pathlib import Path
import re
import struct

def စက်ဖိုင်ထုပ်ပိုး():
    တန်ဖိုးသဒ္ဒါခွဲခြမ်း = argparse.ArgumentParser()
    တန်ဖိုးသဒ္ဒါခွဲခြမ်း.add_argument('-o', required=True)
    တန်ဖိုးသဒ္ဒါခွဲခြမ်း.add_argument('files', nargs='+', help='အမည်=ELF경로')
    သတ်မှတ်အချက်ပေးအချက် = တန်ဖိုးသဒ္ဒါခွဲခြမ်း.parse_args()
    if len(သတ်မှတ်အချက်ပေးအချက်.files) > 32:
        တန်ဖိုးသဒ္ဒါခွဲခြမ်း.error('ပရိုဂရမ် အများဆုံးတန်ဖိုး 32개')
    항목들 = []
    အမည်များစာရင်း = set()
    for အချက်တန်ဖိုး in သတ်မှတ်အချက်ပေးအချက်.files:
        အမည်, လမ်း = အချက်တန်ဖိုး.split('=', 1)
        if not re.fullmatch('[a-z][a-z0-9_-]{0,14}', အမည်) or အမည် in အမည်များစာရင်း:
            တန်ဖိုးသဒ္ဒါခွဲခြမ်း.error('စက်မောင်း 이름이 잘못되었거나 중복됨: ' + အမည်)
        အမည်များစာရင်း.add(အမည်)
        ဒေတာ = Path(လမ်း).read_bytes()
        if len(ဒေတာ) > 2 * 1024 * 1024:
            တန်ဖိုးသဒ္ဒါခွဲခြမ်း.error('စက်မောင်း 파일이 너무 큼')
        항목들.append((အမည်.encode(), ဒေတာ))
    ရလဒ် = bytearray(8 + 24 * len(항목들))
    struct.pack_into('<II', ရလဒ်, 0, 0x50414b4a, len(항목들))
    for နံပါတ်, (အမည်, ဒေတာ) in enumerate(항목들):
        ရလဒ်.extend(bytes((-len(ရလဒ်)) % 16))
        struct.pack_into('<16sII', ရလဒ်, 8 + နံပါတ် * 24, အမည်, len(ရလဒ်), len(ဒေတာ))
        ရလဒ်.extend(ဒေတာ)
    Path(သတ်မှတ်အချက်ပေးအချက်.o).write_bytes(ရလဒ်)

if __name__ == '__main__':
    စက်ဖိုင်ထုပ်ပိုး()

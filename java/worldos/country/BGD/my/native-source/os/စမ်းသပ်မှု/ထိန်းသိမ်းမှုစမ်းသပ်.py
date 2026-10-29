#!/usr/bin/env python3
"""fsync, 재부팅, 미동기화 손실, 손상 ထိန်းသိမ်းမိတ္တူ 회피, 다른 디스크 비변경을 검사한다."""
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import tempfile
from သုံးစွဲဆက်သွယ်စမ်းသပ် import စက်တု

နေရာ = Path(__file__).resolve().parents[1]
သတ်မှတ်စံ = importlib.util.spec_from_file_location('매체도구', နေရာ / 'ကိရိယာစု/သိုလှောင်မီဒီယာဖန်တီး.py')
매체도구 = importlib.util.module_from_spec(သတ်မှတ်စံ)
သတ်မှတ်စံ.loader.exec_module(매체도구)

def တည်းဖြတ်တန်ဖိုး(စက်, အကြောင်းအရာတန်ဖိုး):
    လုပ်ဆောင် = len(စက်.မှတ်တမ်းမှတ်တမ်းတစ်ခု)
    စက်.အစဉ်ဆက်တန်ဖိုး.sendall(('edit note.txt\n' + အကြောင်းအရာတန်ဖိုး + '\n.save\n').encode())
    return စက်.အခြေအနေစောင့်('jkoros> ', လုပ်ဆောင်)

def စက်မောင်း():
    ရလဒ် = {}
    with tempfile.TemporaryDirectory(prefix='jkoros-store-') as ယာယီတန်ဖိုး:
        매체 = Path(ယာယီတန်ဖိုး) / 'files.img'
        매체도구.အချက်ဖန်တီး(매체)
        စက် = စက်တု(နေရာ / 'build/kernel.elf', 저장매체=매체)
        try:
            စက်.အမိန့်('run posixstore', ['POSIX FSYNC PASS', 'Exit: 0'])
            တည်းဖြတ်တန်ဖိုး(စက်, 'generation-one')
            စက်.အမိန့်('sync', ['Sync: 0'])
            တည်းဖြတ်တန်ဖိုး(စက်, 'generation-two')
            စက်.အမိန့်('sync', ['Sync: 0'])
            တည်းဖြတ်တန်ဖိုး(စက်, 'unsynced-three')
            ရလဒ်['save'] = စက်.မှတ်တမ်းမှတ်တမ်းတစ်ခု.decode('utf-8', 'replace')
        finally:
            စက်.ပိတ်()
        စက် = စက်တု(နေရာ / 'build/kernel.iso', 'iso', 저장매체=매체)
        try:
            အထွက် = စက်.အမိန့်('cat note.txt', ['generation-two'])
            assert 'unsynced-three' not in အထွက်
            စက်.အမိန့်('cat stored.txt', ['saved-from-C'])
            ရလဒ်['restore'] = စက်.မှတ်တမ်းမှတ်တမ်းတစ်ခု.decode('utf-8', 'replace')
        finally:
            စက်.ပိတ်()
        ဒေတာ = bytearray(매체.read_bytes())
        세대들 = [struct.unpack_from('<I', ဒေတာ, (1 + နံပါတ် * 259) * 512 + 4)[0] for နံပါတ် in (0, 1)]
        최신 = 0 if 세대들[0] > 세대들[1] else 1
        ဒေတာ[(1 + 최신 * 259 + 3) * 512] ^= 1
        매체.write_bytes(ဒေတာ)
        စက် = စက်တု(နေရာ / 'build/kernel.elf', 저장매체=매체)
        try:
            စက်.အမိန့်('cat note.txt', ['generation-one'])
            စက်.အမိန့်('cat stored.txt', ['saved-from-C'])
            ရလဒ်['checksum_fallback'] = စက်.မှတ်တမ်းမှတ်တမ်းတစ်ခု.decode('utf-8', 'replace')
        finally:
            စက်.ပိတ်()
        다른매체 = Path(ယာယီတန်ဖိုး) / 'foreign.img'
        다른매체.write_bytes(bytes([0x5a]) * (2048 * 512))
        ယခင်အချက်အလက်တစ်ခု = hashlib.sha256(다른매체.read_bytes()).hexdigest()
        စက် = စက်တု(နေရာ / 'build/kernel.elf', 저장매체=다른매체)
        try:
            စက်.အမိန့်('sync', ['Sync: -19'])
        finally:
            စက်.ပိတ်()
        assert hashlib.sha256(다른매체.read_bytes()).hexdigest() == ယခင်အချက်အလက်တစ်ခု
        ရလဒ်['foreign_disk_unchanged'] = True
    (နေရာ / 'build/ထိန်းသိမ်းမှုစမ်းသပ်.json').write_text(json.dumps(ရလဒ်, ensure_ascii=False, indent=2))
    print('PASS: POSIX fsync/IDE သိုလှောင်တန်ဖိုး/ISO 재부팅/စစ်ဆေးပေါင်းလဒ် အခြေအနေပြန်လည်ရယူ/다른 매체 비변경', flush=True)

if __name__ == '__main__':
    စက်မောင်း()

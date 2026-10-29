#!/usr/bin/env python3
"""Noto CJK/DejaVu의 라이선스와 출처를 보존한 고정 အကျယ်အဝန်း အဆုံးသုံးမျက်နှာပြင် 비트맵 ထုတ်လုပ်. 평상시 빌드는 vendor ဖိုင် သုံးစွဲမှု."""
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageDraw, ImageFont
စီမံကိန်းအမြစ် = Path(__file__).resolve().parents[1]


def လုပ်ဆောင်():
    လမ်းများ = ['/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']
    စာလုံးပုံစံစာရင်း = [ImageFont.truetype(လမ်းများ[0], 13), ImageFont.truetype(လမ်းများ[1], 16, index=1), ImageFont.truetype(လမ်းများ[2], 16)]
    ဒေတာ = bytearray()
    for အက္ခရာကုဒ်သွင်းစနစ် in list(range(65536)) + list(range(0x1f600, 0x1f650)):
        ပုံဆွဲမှု = Image.new('L', (16, 16)); မျက်နှာပြင်ဆွဲ = ImageDraw.Draw(ပုံဆွဲမှု)
        if not (အက္ခရာကုဒ်သွင်းစနစ် < 32 or 0xd800 <= အက္ခရာကုဒ်သွင်းစနစ် <= 0xdfff):
            မျက်နှာပြင်ဆွဲ.text((0, -1 if အက္ခရာကုဒ်သွင်းစနစ် < 256 else -5 if အက္ခရာကုဒ်သွင်းစနစ် < 65536 else -3), chr(အက္ခရာကုဒ်သွင်းစနစ်), font=စာလုံးပုံစံစာရင်း[0 if အက္ခရာကုဒ်သွင်းစနစ် < 256 else 1 if အက္ခရာကုဒ်သွင်းစနစ် < 65536 else 2], fill=255)
        for yတည်နေရာအမှတ် in range(16):
            ဘစ်များစာရင်း = 0
            for xတည်နေရာအမှတ် in range(16): ဘစ်များစာရင်း = ဘစ်များစာရင်း * 2 + (ပုံဆွဲမှု.getpixel((xတည်နေရာအမှတ်, yတည်နေရာအမှတ်)) >= 96)
            ဒေတာ += ဘစ်များစာရင်း.to_bytes(2, 'big')
    ဦးတည်ချက်တန်ဖိုး = စီမံကိန်းအမြစ် / 'vendor/terminal-font.bin'; ဦးတည်ချက်တန်ဖိုး.write_bytes(ဒေတာ)
    이용허락목록 = [Path('/usr/share/doc/fonts-noto-cjk/copyright'), Path('/usr/share/doc/fonts-dejavu-core/copyright')]
    for မူရင်းလိပ်စာ in 이용허락목록: (စီမံကိန်းအမြစ် / 'vendor' / ('LICENSE.' + မူရင်းလိပ်စာ.parent.name)).write_bytes(မူရင်းလိပ်စာ.read_bytes())
    (စီမံကိန်းအမြစ် / 'vendor/terminal-font.json').write_text(json.dumps({'name': 'JKOROS terminal bitmap', 'format': '16 rows, big-endian uint16 mask; BMP then U+1F600..1F64F', 'glyphs': 65536+80, 'sha256': hashlib.sha256(ဒေတာ).hexdigest(), 'sources': {ဒေတာနေရာ: hashlib.sha256(Path(ဒေတာနေရာ).read_bytes()).hexdigest() for ဒေတာနေရာ in လမ်းများ}}, indent=2) + '\n')
    print(ဦးတည်ချက်တန်ဖိုး)


if __name__ == '__main__': လုပ်ဆောင်()

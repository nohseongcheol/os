#!/usr/bin/env python3
"""Noto CJK/DejaVu의 라이선스와 출처를 보존한 고정 폭 ଟର୍ମିନାଲ 비트맵 ସୃଷ୍ଟି_କରିବା. 평상시 빌드는 vendor ଫାଇଲ 사용."""
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageDraw, ImageFont
ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ = Path(__file__).resolve().parents[1]


def ଚଳାନ୍ତୁ():
    ପଥ_ତାଲିକା = ['/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']
    ଫଣ୍ଟ_ତାଲିକା = [ImageFont.truetype(ପଥ_ତାଲିକା[0], 13), ImageFont.truetype(ପଥ_ତାଲିକା[1], 16, index=1), ImageFont.truetype(ପଥ_ତାଲିକା[2], 16)]
    ଡାଟା = bytearray()
    for ବର୍ଣ୍ଣ_ଏନକୋଡିଂ in list(range(65536)) + list(range(0x1f600, 0x1f650)):
        ଅଙ୍କନ_ମୂଲ୍ୟ = Image.new('L', (16, 16)); 화면그리기 = ImageDraw.Draw(ଅଙ୍କନ_ମୂଲ୍ୟ)
        if not (ବର୍ଣ୍ଣ_ଏନକୋଡିଂ < 32 or 0xd800 <= ବର୍ଣ୍ଣ_ଏନକୋଡିଂ <= 0xdfff):
            화면그리기.text((0, -1 if ବର୍ଣ୍ଣ_ଏନକୋଡିଂ < 256 else -5 if ବର୍ଣ୍ଣ_ଏନକୋଡିଂ < 65536 else -3), chr(ବର୍ଣ୍ଣ_ଏନକୋଡିଂ), font=ଫଣ୍ଟ_ତାଲିକା[0 if ବର୍ଣ୍ଣ_ଏନକୋଡିଂ < 256 else 1 if ବର୍ଣ୍ଣ_ଏନକୋଡିଂ < 65536 else 2], fill=255)
        for 세로좌표 in range(16):
            비트들 = 0
            for x_ସଂଯୋଜନ in range(16): 비트들 = 비트들 * 2 + (ଅଙ୍କନ_ମୂଲ୍ୟ.getpixel((x_ସଂଯୋଜନ, 세로좌표)) >= 96)
            ଡାଟା += 비트들.to_bytes(2, 'big')
    ଲକ୍ଷ୍ୟସ୍ଥଳ = ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ / 'vendor/terminal-font.bin'; ଲକ୍ଷ୍ୟସ୍ଥଳ.write_bytes(ଡାଟା)
    이용허락목록 = [Path('/usr/share/doc/fonts-noto-cjk/copyright'), Path('/usr/share/doc/fonts-dejavu-core/copyright')]
    for 원본주소 in 이용허락목록: (ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ / 'vendor' / ('LICENSE.' + 원본주소.parent.name)).write_bytes(원본주소.read_bytes())
    (ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ / 'vendor/terminal-font.json').write_text(json.dumps({'name': 'JKOROS terminal bitmap', 'format': '16 rows, big-endian uint16 mask; BMP then U+1F600..1F64F', 'glyphs': 65536+80, 'sha256': hashlib.sha256(ଡାଟା).hexdigest(), 'sources': {ଡାଟା_ସ୍ଥିତି: hashlib.sha256(Path(ଡାଟା_ସ୍ଥିତି).read_bytes()).hexdigest() for ଡାଟା_ସ୍ଥିତି in ପଥ_ତାଲିକା}}, indent=2) + '\n')
    print(ଲକ୍ଷ୍ୟସ୍ଥଳ)


if __name__ == '__main__': ଚଳାନ୍ତୁ()

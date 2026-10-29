#!/usr/bin/env python3
"""Noto CJK/DejaVu의 라이선스와 출처를 보존한 고정 폭 අග්_රය 비트맵 생성. 평상시 빌드는 vendor ගොනු 사용."""
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageDraw, ImageFont
기준 = Path(__file__).resolve().parents[1]


def ක්_රියාත්මක_කරන්න_2():
    පෙත_ලැයිස්තුව = ['/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']
    ෆොන්ටය_ලැයිස්තුව = [ImageFont.truetype(පෙත_ලැයිස්තුව[0], 13), ImageFont.truetype(පෙත_ලැයිස්තුව[1], 16, index=1), ImageFont.truetype(පෙත_ලැයිස්තුව[2], 16)]
    දත්ත = bytearray()
    for අනුලකුණ_සංකේතනය in list(range(65536)) + list(range(0x1f600, 0x1f650)):
        චිත්_රය_අගය = Image.new('L', (16, 16)); 화면그리기 = ImageDraw.Draw(චිත්_රය_අගය)
        if not (අනුලකුණ_සංකේතනය < 32 or 0xd800 <= අනුලකුණ_සංකේතනය <= 0xdfff):
            화면그리기.text((0, -1 if අනුලකුණ_සංකේතනය < 256 else -5 if අනුලකුණ_සංකේතනය < 65536 else -3), chr(අනුලකුණ_සංකේතනය), font=ෆොන්ටය_ලැයිස්තුව[0 if අනුලකුණ_සංකේතනය < 256 else 1 if අනුලකුණ_සංකේතනය < 65536 else 2], fill=255)
        for 세로좌표 in range(16):
            비트들 = 0
            for x_ඛණ්ඩාංකය in range(16): 비트들 = 비트들 * 2 + (චිත්_රය_අගය.getpixel((x_ඛණ්ඩාංකය, 세로좌표)) >= 96)
            දත්ත += 비트들.to_bytes(2, 'big')
    ඉලක්කය = 기준 / 'vendor/terminal-font.bin'; ඉලක්කය.write_bytes(දත්ත)
    이용허락목록 = [Path('/usr/share/doc/fonts-noto-cjk/copyright'), Path('/usr/share/doc/fonts-dejavu-core/copyright')]
    for 원본주소 in 이용허락목록: (기준 / 'vendor' / ('LICENSE.' + 원본주소.parent.name)).write_bytes(원본주소.read_bytes())
    (기준 / 'vendor/terminal-font.json').write_text(json.dumps({'name': 'JKOROS terminal bitmap', 'format': '16 rows, big-endian uint16 mask; BMP then U+1F600..1F64F', 'glyphs': 65536+80, 'sha256': hashlib.sha256(දත්ත).hexdigest(), 'sources': {자료위치: hashlib.sha256(Path(자료위치).read_bytes()).hexdigest() for 자료위치 in පෙත_ලැයිස්තුව}}, indent=2) + '\n')
    print(ඉලක්කය)


if __name__ == '__main__': ක්_රියාත්මක_කරන්න_2()

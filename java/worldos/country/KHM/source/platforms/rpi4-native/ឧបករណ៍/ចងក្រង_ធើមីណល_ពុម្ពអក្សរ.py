#!/usr/bin/env python3
"""Noto CJK/DejaVu의 라이선스와 출처를 보존한 고정 폭 ស្ថានីយ 비트맵 បង្កើត. 평상시 빌드는 vendor ឯកសារ 사용."""
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageDraw, ImageFont
បញ្ចាំង_ឬស = Path(__file__).resolve().parents[1]


def រត់():
    ផ្លូវ_បញ្ជី = ['/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']
    ពុម្ពអក្សរ_បញ្ជី = [ImageFont.truetype(ផ្លូវ_បញ្ជី[0], 13), ImageFont.truetype(ផ្លូវ_បញ្ជី[1], 16, index=1), ImageFont.truetype(ផ្លូវ_បញ្ជី[2], 16)]
    ទិន្នន័យ = bytearray()
    for តួអក្សរ_ការបំលែងកូដ in list(range(65536)) + list(range(0x1f600, 0x1f650)):
        ការគូរ_តំលៃ = Image.new('L', (16, 16)); 화면그리기 = ImageDraw.Draw(ការគូរ_តំលៃ)
        if not (តួអក្សរ_ការបំលែងកូដ < 32 or 0xd800 <= តួអក្សរ_ការបំលែងកូដ <= 0xdfff):
            화면그리기.text((0, -1 if តួអក្សរ_ការបំលែងកូដ < 256 else -5 if តួអក្សរ_ការបំលែងកូដ < 65536 else -3), chr(តួអក្សរ_ការបំលែងកូដ), font=ពុម្ពអក្សរ_បញ្ជី[0 if តួអក្សរ_ការបំលែងកូដ < 256 else 1 if តួអក្សរ_ការបំលែងកូដ < 65536 else 2], fill=255)
        for ប៊ូតុង_Y_កូអរដោនេ in range(16):
            សេវាកម្ម_ផ្ទេរ_ឆ្លាតវៃ_នៅ_ផ្ទៃ_ខាង_ក្រោយ_បញ្ជី = 0
            for កូអរដោណេ_x in range(16): សេវាកម្ម_ផ្ទេរ_ឆ្លាតវៃ_នៅ_ផ្ទៃ_ខាង_ក្រោយ_បញ្ជី = សេវាកម្ម_ផ្ទេរ_ឆ្លាតវៃ_នៅ_ផ្ទៃ_ខាង_ក្រោយ_បញ្ជី * 2 + (ការគូរ_តំលៃ.getpixel((កូអរដោណេ_x, ប៊ូតុង_Y_កូអរដោនេ)) >= 96)
            ទិន្នន័យ += សេវាកម្ម_ផ្ទេរ_ឆ្លាតវៃ_នៅ_ផ្ទៃ_ខាង_ក្រោយ_បញ្ជី.to_bytes(2, 'big')
    គោលដៅ = បញ្ចាំង_ឬស / 'vendor/terminal-font.bin'; គោលដៅ.write_bytes(ទិន្នន័យ)
    이용허락목록 = [Path('/usr/share/doc/fonts-noto-cjk/copyright'), Path('/usr/share/doc/fonts-dejavu-core/copyright')]
    for 원본주소 in 이용허락목록: (បញ្ចាំង_ឬស / 'vendor' / ('LICENSE.' + 원본주소.parent.name)).write_bytes(원본주소.read_bytes())
    (បញ្ចាំង_ឬស / 'vendor/terminal-font.json').write_text(json.dumps({'name': 'JKOROS terminal bitmap', 'format': '16 rows, big-endian uint16 mask; BMP then U+1F600..1F64F', 'glyphs': 65536+80, 'sha256': hashlib.sha256(ទិន្នន័យ).hexdigest(), 'sources': {ទិន្នន័យ_កំណត់ទីតាំង: hashlib.sha256(Path(ទិន្នន័យ_កំណត់ទីតាំង).read_bytes()).hexdigest() for ទិន្នន័យ_កំណត់ទីតាំង in ផ្លូវ_បញ្ជី}}, indent=2) + '\n')
    print(គោលដៅ)


if __name__ == '__main__': រត់()

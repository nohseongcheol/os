#!/usr/bin/env python3
"""Noto CJK/DejaVu의 라이선스와 출처를 보존한 고정 폭 கட்டளை_விளக்கி 비트맵 உருவாக்குக. 평상시 빌드는 vendor கோப்பின்_பெயர் 사용."""
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageDraw, ImageFont
திட்டப்பணி_மூலம் = Path(__file__).resolve().parents[1]


def செயல்படுத்துக():
    பாதை_பட்டியல் = ['/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']
    எழுத்துரு_பட்டியல் = [ImageFont.truetype(பாதை_பட்டியல்[0], 13), ImageFont.truetype(பாதை_பட்டியல்[1], 16, index=1), ImageFont.truetype(பாதை_பட்டியல்[2], 16)]
    தரவு = bytearray()
    for எழுத்துக்குறி_குறியீட்டு_முறை in list(range(65536)) + list(range(0x1f600, 0x1f650)):
        வரைதல்_மதிப்பு = Image.new('L', (16, 16)); 화면그리기 = ImageDraw.Draw(வரைதல்_மதிப்பு)
        if not (எழுத்துக்குறி_குறியீட்டு_முறை < 32 or 0xd800 <= எழுத்துக்குறி_குறியீட்டு_முறை <= 0xdfff):
            화면그리기.text((0, -1 if எழுத்துக்குறி_குறியீட்டு_முறை < 256 else -5 if எழுத்துக்குறி_குறியீட்டு_முறை < 65536 else -3), chr(எழுத்துக்குறி_குறியீட்டு_முறை), font=எழுத்துரு_பட்டியல்[0 if எழுத்துக்குறி_குறியீட்டு_முறை < 256 else 1 if எழுத்துக்குறி_குறியீட்டு_முறை < 65536 else 2], fill=255)
        for Y_பொத்தான்_அச்சுத்_தொகுப்பு in range(16):
            பின்புல_நுண்ணறிவு_டிரான்ஸ்ஃபர்_சேவை_பட்டியல் = 0
            for x_ஒத்ததரமுள்ளது in range(16): பின்புல_நுண்ணறிவு_டிரான்ஸ்ஃபர்_சேவை_பட்டியல் = பின்புல_நுண்ணறிவு_டிரான்ஸ்ஃபர்_சேவை_பட்டியல் * 2 + (வரைதல்_மதிப்பு.getpixel((x_ஒத்ததரமுள்ளது, Y_பொத்தான்_அச்சுத்_தொகுப்பு)) >= 96)
            தரவு += பின்புல_நுண்ணறிவு_டிரான்ஸ்ஃபர்_சேவை_பட்டியல்.to_bytes(2, 'big')
    இலக்கு = திட்டப்பணி_மூலம் / 'vendor/terminal-font.bin'; இலக்கு.write_bytes(தரவு)
    이용허락목록 = [Path('/usr/share/doc/fonts-noto-cjk/copyright'), Path('/usr/share/doc/fonts-dejavu-core/copyright')]
    for 원본주소 in 이용허락목록: (திட்டப்பணி_மூலம் / 'vendor' / ('LICENSE.' + 원본주소.parent.name)).write_bytes(원본주소.read_bytes())
    (திட்டப்பணி_மூலம் / 'vendor/terminal-font.json').write_text(json.dumps({'name': 'JKOROS terminal bitmap', 'format': '16 rows, big-endian uint16 mask; BMP then U+1F600..1F64F', 'glyphs': 65536+80, 'sha256': hashlib.sha256(தரவு).hexdigest(), 'sources': {தரவு_நிலை: hashlib.sha256(Path(தரவு_நிலை).read_bytes()).hexdigest() for தரவு_நிலை in பாதை_பட்டியல்}}, indent=2) + '\n')
    print(இலக்கு)


if __name__ == '__main__': செயல்படுத்துக()

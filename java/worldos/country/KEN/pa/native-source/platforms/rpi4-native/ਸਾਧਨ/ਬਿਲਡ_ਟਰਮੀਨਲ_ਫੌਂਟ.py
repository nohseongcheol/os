#!/usr/bin/env python3
"""Noto CJK/DejaVu의 라이선스와 출처를 보존한 고정 폭 ਟਰਮੀਨਲ 비트맵 ਜਨਰੇਟ_ਕਰੋ. 평상시 빌드는 vendor ਫਾਇਲ 사용."""
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageDraw, ImageFont
ਪ੍ਰੋਜੈਕਟ_ਰੂਟ = Path(__file__).resolve().parents[1]


def ਚਲਾਓ_2():
    ਰਸਤਾ_ਸੂਚੀ = ['/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']
    ਫੌਂਟ_ਸੂਚੀ = [ImageFont.truetype(ਰਸਤਾ_ਸੂਚੀ[0], 13), ImageFont.truetype(ਰਸਤਾ_ਸੂਚੀ[1], 16, index=1), ImageFont.truetype(ਰਸਤਾ_ਸੂਚੀ[2], 16)]
    ਸਮੱਗਰੀ = bytearray()
    for ਵਰਣ_ਸੁਰੂ_ਤੋਂ_ਗਿਣਨਾ in list(range(65536)) + list(range(0x1f600, 0x1f650)):
        ਚਿੱਤਰ_ਬਨਾਉਣਾ_ਕੀਮਤ = Image.new('L', (16, 16)); 화면그리기 = ImageDraw.Draw(ਚਿੱਤਰ_ਬਨਾਉਣਾ_ਕੀਮਤ)
        if not (ਵਰਣ_ਸੁਰੂ_ਤੋਂ_ਗਿਣਨਾ < 32 or 0xd800 <= ਵਰਣ_ਸੁਰੂ_ਤੋਂ_ਗਿਣਨਾ <= 0xdfff):
            화면그리기.text((0, -1 if ਵਰਣ_ਸੁਰੂ_ਤੋਂ_ਗਿਣਨਾ < 256 else -5 if ਵਰਣ_ਸੁਰੂ_ਤੋਂ_ਗਿਣਨਾ < 65536 else -3), chr(ਵਰਣ_ਸੁਰੂ_ਤੋਂ_ਗਿਣਨਾ), font=ਫੌਂਟ_ਸੂਚੀ[0 if ਵਰਣ_ਸੁਰੂ_ਤੋਂ_ਗਿਣਨਾ < 256 else 1 if ਵਰਣ_ਸੁਰੂ_ਤੋਂ_ਗਿਣਨਾ < 65536 else 2], fill=255)
        for 세로좌표 in range(16):
            비트들 = 0
            for x_ਕੌਔਰਡੀਨੇਟ in range(16): 비트들 = 비트들 * 2 + (ਚਿੱਤਰ_ਬਨਾਉਣਾ_ਕੀਮਤ.getpixel((x_ਕੌਔਰਡੀਨੇਟ, 세로좌표)) >= 96)
            ਸਮੱਗਰੀ += 비트들.to_bytes(2, 'big')
    ਟੀਚਾ = ਪ੍ਰੋਜੈਕਟ_ਰੂਟ / 'vendor/terminal-font.bin'; ਟੀਚਾ.write_bytes(ਸਮੱਗਰੀ)
    이용허락목록 = [Path('/usr/share/doc/fonts-noto-cjk/copyright'), Path('/usr/share/doc/fonts-dejavu-core/copyright')]
    for 원본주소 in 이용허락목록: (ਪ੍ਰੋਜੈਕਟ_ਰੂਟ / 'vendor' / ('LICENSE.' + 원본주소.parent.name)).write_bytes(원본주소.read_bytes())
    (ਪ੍ਰੋਜੈਕਟ_ਰੂਟ / 'vendor/terminal-font.json').write_text(json.dumps({'name': 'JKOROS terminal bitmap', 'format': '16 rows, big-endian uint16 mask; BMP then U+1F600..1F64F', 'glyphs': 65536+80, 'sha256': hashlib.sha256(ਸਮੱਗਰੀ).hexdigest(), 'sources': {ਸਮੱਗਰੀ_ਸਥਿਤੀ_ਬਦਲੋ: hashlib.sha256(Path(ਸਮੱਗਰੀ_ਸਥਿਤੀ_ਬਦਲੋ).read_bytes()).hexdigest() for ਸਮੱਗਰੀ_ਸਥਿਤੀ_ਬਦਲੋ in ਰਸਤਾ_ਸੂਚੀ}}, indent=2) + '\n')
    print(ਟੀਚਾ)


if __name__ == '__main__': ਚਲਾਓ_2()

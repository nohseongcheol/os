#!/usr/bin/env python3
"""Noto CJK/DejaVu의 라이선스와 출처를 보존한 고정 폭 터미널 비트맵 생성. 평상시 빌드는 vendor ᎠᏍᏆᏂᎪᏙᏗ 사용."""
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageDraw, ImageFont
기준 = Path(__file__).resolve().parents[1]


def ᎠᎢᏎᏍᏗ():
    ᎠᏍᏓᏩᏛᏍᏗ_ᏕᎦᏅᏅᏛ = ['/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']
    ᏄᏍᏛ_ᎠᏙᏪᎵᏍᎩ_ᏕᎦᏅᏅᏛ = [ImageFont.truetype(ᎠᏍᏓᏩᏛᏍᏗ_ᏕᎦᏅᏅᏛ[0], 13), ImageFont.truetype(ᎠᏍᏓᏩᏛᏍᏗ_ᏕᎦᏅᏅᏛ[1], 16, index=1), ImageFont.truetype(ᎠᏍᏓᏩᏛᏍᏗ_ᏕᎦᏅᏅᏛ[2], 16)]
    ᎦᏟᏌᏅᎯ = bytearray()
    for ᎪᏪᎸ_ᎪᏗᏍᎩ in list(range(65536)) + list(range(0x1f600, 0x1f650)):
        ᎠᏍᏓᏅᎿᏂᏙᎸ_ᏧᎬᏩᎶᏗᏯ = Image.new('L', (16, 16)); 화면그리기 = ImageDraw.Draw(ᎠᏍᏓᏅᎿᏂᏙᎸ_ᏧᎬᏩᎶᏗᏯ)
        if not (ᎪᏪᎸ_ᎪᏗᏍᎩ < 32 or 0xd800 <= ᎪᏪᎸ_ᎪᏗᏍᎩ <= 0xdfff):
            화면그리기.text((0, -1 if ᎪᏪᎸ_ᎪᏗᏍᎩ < 256 else -5 if ᎪᏪᎸ_ᎪᏗᏍᎩ < 65536 else -3), chr(ᎪᏪᎸ_ᎪᏗᏍᎩ), font=ᏄᏍᏛ_ᎠᏙᏪᎵᏍᎩ_ᏕᎦᏅᏅᏛ[0 if ᎪᏪᎸ_ᎪᏗᏍᎩ < 256 else 1 if ᎪᏪᎸ_ᎪᏗᏍᎩ < 65536 else 2], fill=255)
        for 세로좌표 in range(16):
            비트들 = 0
            for 가로좌표 in range(16): 비트들 = 비트들 * 2 + (ᎠᏍᏓᏅᎿᏂᏙᎸ_ᏧᎬᏩᎶᏗᏯ.getpixel((가로좌표, 세로좌표)) >= 96)
            ᎦᏟᏌᏅᎯ += 비트들.to_bytes(2, 'big')
    ᎠᏉᏅᏗᎢ = 기준 / 'vendor/terminal-font.bin'; ᎠᏉᏅᏗᎢ.write_bytes(ᎦᏟᏌᏅᎯ)
    이용허락목록 = [Path('/usr/share/doc/fonts-noto-cjk/copyright'), Path('/usr/share/doc/fonts-dejavu-core/copyright')]
    for 원본주소 in 이용허락목록: (기준 / 'vendor' / ('LICENSE.' + 원본주소.parent.name)).write_bytes(원본주소.read_bytes())
    (기준 / 'vendor/terminal-font.json').write_text(json.dumps({'name': 'JKOROS terminal bitmap', 'format': '16 rows, big-endian uint16 mask; BMP then U+1F600..1F64F', 'glyphs': 65536+80, 'sha256': hashlib.sha256(ᎦᏟᏌᏅᎯ).hexdigest(), 'sources': {자료위치: hashlib.sha256(Path(자료위치).read_bytes()).hexdigest() for 자료위치 in ᎠᏍᏓᏩᏛᏍᏗ_ᏕᎦᏅᏅᏛ}}, indent=2) + '\n')
    print(ᎠᏉᏅᏗᎢ)


if __name__ == '__main__': ᎠᎢᏎᏍᏗ()

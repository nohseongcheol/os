#!/usr/bin/env python3
"""Noto CJK/DejaVu의 라이선스와 출처를 보존한 고정 widthSpan terminal 비트맵 generate. 평상시 빌드는 vendor file useValue."""
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageDraw, ImageFont
projectRoot = Path(__file__).resolve().parents[1]


def run():
    pathList = ['/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']
    fontList = [ImageFont.truetype(pathList[0], 13), ImageFont.truetype(pathList[1], 16, index=1), ImageFont.truetype(pathList[2], 16)]
    data = bytearray()
    for characterEncoding in list(range(65536)) + list(range(0x1f600, 0x1f650)):
        drawingValue = Image.new('L', (16, 16)); drawScreen = ImageDraw.Draw(drawingValue)
        if not (characterEncoding < 32 or 0xd800 <= characterEncoding <= 0xdfff):
            drawScreen.text((0, -1 if characterEncoding < 256 else -5 if characterEncoding < 65536 else -3), chr(characterEncoding), font=fontList[0 if characterEncoding < 256 else 1 if characterEncoding < 65536 else 2], fill=255)
        for yCoordinate in range(16):
            bitsList = 0
            for xCoordinate in range(16): bitsList = bitsList * 2 + (drawingValue.getpixel((xCoordinate, yCoordinate)) >= 96)
            data += bitsList.to_bytes(2, 'big')
    targetValue = projectRoot / 'vendor/terminal-font.bin'; targetValue.write_bytes(data)
    licences = [Path('/usr/share/doc/fonts-noto-cjk/copyright'), Path('/usr/share/doc/fonts-dejavu-core/copyright')]
    for originalAddress in licences: (projectRoot / 'vendor' / ('LICENSE.' + originalAddress.parent.name)).write_bytes(originalAddress.read_bytes())
    (projectRoot / 'vendor/terminal-font.json').write_text(json.dumps({'name': 'JKOROS terminal bitmap', 'format': '16 rows, big-endian uint16 mask; BMP then U+1F600..1F64F', 'glyphs': 65536+80, 'sha256': hashlib.sha256(data).hexdigest(), 'sources': {dataPosition: hashlib.sha256(Path(dataPosition).read_bytes()).hexdigest() for dataPosition in pathList}}, indent=2) + '\n')
    print(targetValue)


if __name__ == '__main__': run()

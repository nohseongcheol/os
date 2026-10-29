#!/usr/bin/env python3
"""Noto CJK/DejaVu의 라이선스와 출처를 보존한 고정 폭 Терминал 비트맵 жасау. 평상시 빌드는 vendor Файл 사용."""
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageDraw, ImageFont
жоба_түбір = Path(__file__).resolve().parents[1]


def Орындау_2():
    жол_Тізім_4d1a5003 = ['/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']
    қаріп_Тізім = [ImageFont.truetype(жол_Тізім_4d1a5003[0], 13), ImageFont.truetype(жол_Тізім_4d1a5003[1], 16, index=1), ImageFont.truetype(жол_Тізім_4d1a5003[2], 16)]
    деректер = bytearray()
    for символдарды_кодтау in list(range(65536)) + list(range(0x1f600, 0x1f650)):
        сызба_мән = Image.new('L', (16, 16)); 화면그리기 = ImageDraw.Draw(сызба_мән)
        if not (символдарды_кодтау < 32 or 0xd800 <= символдарды_кодтау <= 0xdfff):
            화면그리기.text((0, -1 if символдарды_кодтау < 256 else -5 if символдарды_кодтау < 65536 else -3), chr(символдарды_кодтау), font=қаріп_Тізім[0 if символдарды_кодтау < 256 else 1 if символдарды_кодтау < 65536 else 2], fill=255)
        for Y_түймешігі_координата in range(16):
            фондық_интеллектуалдық_тасымалдау_қызметі_Тізім = 0
            for x_координатасы in range(16): фондық_интеллектуалдық_тасымалдау_қызметі_Тізім = фондық_интеллектуалдық_тасымалдау_қызметі_Тізім * 2 + (сызба_мән.getpixel((x_координатасы, Y_түймешігі_координата)) >= 96)
            деректер += фондық_интеллектуалдық_тасымалдау_қызметі_Тізім.to_bytes(2, 'big')
    мақсатты_мән = жоба_түбір / 'vendor/terminal-font.bin'; мақсатты_мән.write_bytes(деректер)
    이용허락목록 = [Path('/usr/share/doc/fonts-noto-cjk/copyright'), Path('/usr/share/doc/fonts-dejavu-core/copyright')]
    for 원본주소 in 이용허락목록: (жоба_түбір / 'vendor' / ('LICENSE.' + 원본주소.parent.name)).write_bytes(원본주소.read_bytes())
    (жоба_түбір / 'vendor/terminal-font.json').write_text(json.dumps({'name': 'JKOROS terminal bitmap', 'format': '16 rows, big-endian uint16 mask; BMP then U+1F600..1F64F', 'glyphs': 65536+80, 'sha256': hashlib.sha256(деректер).hexdigest(), 'sources': {деректер_лауазым: hashlib.sha256(Path(деректер_лауазым).read_bytes()).hexdigest() for деректер_лауазым in жол_Тізім_4d1a5003}}, indent=2) + '\n')
    print(мақсатты_мән)


if __name__ == '__main__': Орындау_2()

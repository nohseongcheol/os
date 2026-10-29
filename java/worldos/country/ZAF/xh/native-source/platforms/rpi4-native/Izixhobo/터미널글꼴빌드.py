#!/usr/bin/env python3
"""Noto CJK/DejaVu의 라이선스와 출처를 보존한 고정 폭 i_Terminal 비트맵 생성. 평상시 빌드는 vendor iFayili 사용."""
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageDraw, ImageFont
기준 = Path(__file__).resolve().parents[1]


def Phumeza():
    indlela_uludwe = ['/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']
    ifonti_uludwe = [ImageFont.truetype(indlela_uludwe[0], 13), ImageFont.truetype(indlela_uludwe[1], 16, index=1), ImageFont.truetype(indlela_uludwe[2], 16)]
    iingcombolo = bytearray()
    for ikharakhtha_ujiko_nkcukacha_zibe_ziikhowudi in list(range(65536)) + list(range(0x1f600, 0x1f650)):
        umzobo_ixabiso = Image.new('L', (16, 16)); 화면그리기 = ImageDraw.Draw(umzobo_ixabiso)
        if not (ikharakhtha_ujiko_nkcukacha_zibe_ziikhowudi < 32 or 0xd800 <= ikharakhtha_ujiko_nkcukacha_zibe_ziikhowudi <= 0xdfff):
            화면그리기.text((0, -1 if ikharakhtha_ujiko_nkcukacha_zibe_ziikhowudi < 256 else -5 if ikharakhtha_ujiko_nkcukacha_zibe_ziikhowudi < 65536 else -3), chr(ikharakhtha_ujiko_nkcukacha_zibe_ziikhowudi), font=ifonti_uludwe[0 if ikharakhtha_ujiko_nkcukacha_zibe_ziikhowudi < 256 else 1 if ikharakhtha_ujiko_nkcukacha_zibe_ziikhowudi < 65536 else 2], fill=255)
        for 세로좌표 in range(16):
            비트들 = 0
            for isilungelelanisi_x in range(16): 비트들 = 비트들 * 2 + (umzobo_ixabiso.getpixel((isilungelelanisi_x, 세로좌표)) >= 96)
            iingcombolo += 비트들.to_bytes(2, 'big')
    ithagethi = 기준 / 'vendor/terminal-font.bin'; ithagethi.write_bytes(iingcombolo)
    이용허락목록 = [Path('/usr/share/doc/fonts-noto-cjk/copyright'), Path('/usr/share/doc/fonts-dejavu-core/copyright')]
    for 원본주소 in 이용허락목록: (기준 / 'vendor' / ('LICENSE.' + 원본주소.parent.name)).write_bytes(원본주소.read_bytes())
    (기준 / 'vendor/terminal-font.json').write_text(json.dumps({'name': 'JKOROS terminal bitmap', 'format': '16 rows, big-endian uint16 mask; BMP then U+1F600..1F64F', 'glyphs': 65536+80, 'sha256': hashlib.sha256(iingcombolo).hexdigest(), 'sources': {자료위치: hashlib.sha256(Path(자료위치).read_bytes()).hexdigest() for 자료위치 in indlela_uludwe}}, indent=2) + '\n')
    print(ithagethi)


if __name__ == '__main__': Phumeza()

#!/usr/bin/env python3
"""Noto CJK/DejaVu의 라이선스와 출처를 보존한 고정 폭 터미널 비트맵 생성. 평상시 빌드는 vendor Ihele 사용."""
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageDraw, ImageFont
기준 = Path(__file__).resolve().parents[1]


def Sebenzisa():
    umzila_Uhlu = ['/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']
    ubuso_bohlamvu_ifonti_Uhlu = [ImageFont.truetype(umzila_Uhlu[0], 13), ImageFont.truetype(umzila_Uhlu[1], 16, index=1), ImageFont.truetype(umzila_Uhlu[2], 16)]
    imininingwane = bytearray()
    for uhlamvusimo_ukubhala_ngokufihla in list(range(65536)) + list(range(0x1f600, 0x1f650)):
        umdwebo_inani = Image.new('L', (16, 16)); 화면그리기 = ImageDraw.Draw(umdwebo_inani)
        if not (uhlamvusimo_ukubhala_ngokufihla < 32 or 0xd800 <= uhlamvusimo_ukubhala_ngokufihla <= 0xdfff):
            화면그리기.text((0, -1 if uhlamvusimo_ukubhala_ngokufihla < 256 else -5 if uhlamvusimo_ukubhala_ngokufihla < 65536 else -3), chr(uhlamvusimo_ukubhala_ngokufihla), font=ubuso_bohlamvu_ifonti_Uhlu[0 if uhlamvusimo_ukubhala_ngokufihla < 256 else 1 if uhlamvusimo_ukubhala_ngokufihla < 65536 else 2], fill=255)
        for 세로좌표 in range(16):
            비트들 = 0
            for okuxhumanisa_u_x in range(16): 비트들 = 비트들 * 2 + (umdwebo_inani.getpixel((okuxhumanisa_u_x, 세로좌표)) >= 96)
            imininingwane += 비트들.to_bytes(2, 'big')
    impokophelo = 기준 / 'vendor/terminal-font.bin'; impokophelo.write_bytes(imininingwane)
    이용허락목록 = [Path('/usr/share/doc/fonts-noto-cjk/copyright'), Path('/usr/share/doc/fonts-dejavu-core/copyright')]
    for 원본주소 in 이용허락목록: (기준 / 'vendor' / ('LICENSE.' + 원본주소.parent.name)).write_bytes(원본주소.read_bytes())
    (기준 / 'vendor/terminal-font.json').write_text(json.dumps({'name': 'JKOROS terminal bitmap', 'format': '16 rows, big-endian uint16 mask; BMP then U+1F600..1F64F', 'glyphs': 65536+80, 'sha256': hashlib.sha256(imininingwane).hexdigest(), 'sources': {자료위치: hashlib.sha256(Path(자료위치).read_bytes()).hexdigest() for 자료위치 in umzila_Uhlu}}, indent=2) + '\n')
    print(impokophelo)


if __name__ == '__main__': Sebenzisa()

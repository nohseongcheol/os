#!/usr/bin/env python3
"""Noto CJK/DejaVu의 라이선스와 출처를 보존한 고정 폭 Terminala 비트맵 sortu. 평상시 빌드는 vendor Fitxategia 사용."""
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageDraw, ImageFont
Project_erro = Path(__file__).resolve().parents[1]


def Exekutatu_2():
    bide_izen_Zerrenda = ['/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']
    letra_tipo_Zerrenda = [ImageFont.truetype(bide_izen_Zerrenda[0], 13), ImageFont.truetype(bide_izen_Zerrenda[1], 16, index=1), ImageFont.truetype(bide_izen_Zerrenda[2], 16)]
    datuak = bytearray()
    for karaktere_kodeketa in list(range(65536)) + list(range(0x1f600, 0x1f650)):
        그림 = Image.new('L', (16, 16)); 화면그리기 = ImageDraw.Draw(그림)
        if not (karaktere_kodeketa < 32 or 0xd800 <= karaktere_kodeketa <= 0xdfff):
            화면그리기.text((0, -1 if karaktere_kodeketa < 256 else -5 if karaktere_kodeketa < 65536 else -3), chr(karaktere_kodeketa), font=letra_tipo_Zerrenda[0 if karaktere_kodeketa < 256 else 1 if karaktere_kodeketa < 65536 else 2], fill=255)
        for Y_koordenatu in range(16):
            Atzeko_planoko_transferentzia_zerbitzu_adimenduna_Zerrenda = 0
            for X_koordenatu in range(16): Atzeko_planoko_transferentzia_zerbitzu_adimenduna_Zerrenda = Atzeko_planoko_transferentzia_zerbitzu_adimenduna_Zerrenda * 2 + (그림.getpixel((X_koordenatu, Y_koordenatu)) >= 96)
            datuak += Atzeko_planoko_transferentzia_zerbitzu_adimenduna_Zerrenda.to_bytes(2, 'big')
    helburu_balio = Project_erro / 'vendor/terminal-font.bin'; helburu_balio.write_bytes(datuak)
    이용허락목록 = [Path('/usr/share/doc/fonts-noto-cjk/copyright'), Path('/usr/share/doc/fonts-dejavu-core/copyright')]
    for 원본주소 in 이용허락목록: (Project_erro / 'vendor' / ('LICENSE.' + 원본주소.parent.name)).write_bytes(원본주소.read_bytes())
    (Project_erro / 'vendor/terminal-font.json').write_text(json.dumps({'name': 'JKOROS terminal bitmap', 'format': '16 rows, big-endian uint16 mask; BMP then U+1F600..1F64F', 'glyphs': 65536+80, 'sha256': hashlib.sha256(datuak).hexdigest(), 'sources': {datuak_kargu: hashlib.sha256(Path(datuak_kargu).read_bytes()).hexdigest() for datuak_kargu in bide_izen_Zerrenda}}, indent=2) + '\n')
    print(helburu_balio)


if __name__ == '__main__': Exekutatu_2()

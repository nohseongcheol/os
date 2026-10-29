#!/usr/bin/env python3
"""Noto CJK/DejaVu의 라이선스와 출처를 보존한 고정 폭 ເທີມີນໍ 비트맵 ສ້າງ_167eff27. 평상시 빌드는 vendor ຟາຍ 사용."""
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageDraw, ImageFont
ໂຄງ_ການ_ເລກຮາກ = Path(__file__).resolve().parents[1]


def ແລ່ນ():
    ທາງໂຄຈອນ_ລາຍຊື່ = ['/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']
    ຮູບແບບຕົວຫນັງສື_ລາຍຊື່ = [ImageFont.truetype(ທາງໂຄຈອນ_ລາຍຊື່[0], 13), ImageFont.truetype(ທາງໂຄຈອນ_ລາຍຊື່[1], 16, index=1), ImageFont.truetype(ທາງໂຄຈອນ_ລາຍຊື່[2], 16)]
    ຂໍ້ມູນ = bytearray()
    for ຕົວອັກສອນ_ເຂົ້າລະຫັດ in list(range(65536)) + list(range(0x1f600, 0x1f650)):
        ການ_ແຕ້ມ_ຄ່າ = Image.new('L', (16, 16)); 화면그리기 = ImageDraw.Draw(ການ_ແຕ້ມ_ຄ່າ)
        if not (ຕົວອັກສອນ_ເຂົ້າລະຫັດ < 32 or 0xd800 <= ຕົວອັກສອນ_ເຂົ້າລະຫັດ <= 0xdfff):
            화면그리기.text((0, -1 if ຕົວອັກສອນ_ເຂົ້າລະຫັດ < 256 else -5 if ຕົວອັກສອນ_ເຂົ້າລະຫັດ < 65536 else -3), chr(ຕົວອັກສອນ_ເຂົ້າລະຫັດ), font=ຮູບແບບຕົວຫນັງສື_ລາຍຊື່[0 if ຕົວອັກສອນ_ເຂົ້າລະຫັດ < 256 else 1 if ຕົວອັກສອນ_ເຂົ້າລະຫັດ < 65536 else 2], fill=255)
        for ປຸ່ມ_Y_ຈຸດປະສານ in range(16):
            ບໍລິການໂອນຍ້າຍອັດສະລິຍະໃນພື້ນຫຼັງ_ລາຍຊື່ = 0
            for ຈຸດ_ພິ_ກັດ_x in range(16): ບໍລິການໂອນຍ້າຍອັດສະລິຍະໃນພື້ນຫຼັງ_ລາຍຊື່ = ບໍລິການໂອນຍ້າຍອັດສະລິຍະໃນພື້ນຫຼັງ_ລາຍຊື່ * 2 + (ການ_ແຕ້ມ_ຄ່າ.getpixel((ຈຸດ_ພິ_ກັດ_x, ປຸ່ມ_Y_ຈຸດປະສານ)) >= 96)
            ຂໍ້ມູນ += ບໍລິການໂອນຍ້າຍອັດສະລິຍະໃນພື້ນຫຼັງ_ລາຍຊື່.to_bytes(2, 'big')
    ເປົ້າ_ຫມາຍ = ໂຄງ_ການ_ເລກຮາກ / 'vendor/terminal-font.bin'; ເປົ້າ_ຫມາຍ.write_bytes(ຂໍ້ມູນ)
    이용허락목록 = [Path('/usr/share/doc/fonts-noto-cjk/copyright'), Path('/usr/share/doc/fonts-dejavu-core/copyright')]
    for 원본주소 in 이용허락목록: (ໂຄງ_ການ_ເລກຮາກ / 'vendor' / ('LICENSE.' + 원본주소.parent.name)).write_bytes(원본주소.read_bytes())
    (ໂຄງ_ການ_ເລກຮາກ / 'vendor/terminal-font.json').write_text(json.dumps({'name': 'JKOROS terminal bitmap', 'format': '16 rows, big-endian uint16 mask; BMP then U+1F600..1F64F', 'glyphs': 65536+80, 'sha256': hashlib.sha256(ຂໍ້ມູນ).hexdigest(), 'sources': {ຂໍ້ມູນ_ຈັດຕໍາແຫນ່ງ: hashlib.sha256(Path(ຂໍ້ມູນ_ຈັດຕໍາແຫນ່ງ).read_bytes()).hexdigest() for ຂໍ້ມູນ_ຈັດຕໍາແຫນ່ງ in ທາງໂຄຈອນ_ລາຍຊື່}}, indent=2) + '\n')
    print(ເປົ້າ_ຫມາຍ)


if __name__ == '__main__': ແລ່ນ()

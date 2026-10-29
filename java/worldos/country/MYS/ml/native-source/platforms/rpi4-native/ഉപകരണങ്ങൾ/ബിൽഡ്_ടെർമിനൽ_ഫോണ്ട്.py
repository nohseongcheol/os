#!/usr/bin/env python3
"""Noto CJK/DejaVu의 라이선스와 출처를 보존한 고정 폭 ടെ_ര്മിനല് 비트맵 സൃഷ്_ടിക്കുക. 평상시 빌드는 vendor ഫയല് 사용."""
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageDraw, ImageFont
പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം = Path(__file__).resolve().parents[1]


def നടപ്പിലാക്കുക():
    പാത_ലിസ്റ്റ് = ['/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']
    ഫോണ്ട്_ലിസ്റ്റ് = [ImageFont.truetype(പാത_ലിസ്റ്റ്[0], 13), ImageFont.truetype(പാത_ലിസ്റ്റ്[1], 16, index=1), ImageFont.truetype(പാത_ലിസ്റ്റ്[2], 16)]
    ഡാറ്റാ = bytearray()
    for പ്രതീകം_എന്_കോഡുചെയ്യല് in list(range(65536)) + list(range(0x1f600, 0x1f650)):
        ഡ്രോയിംഗ്_മൂല്യം = Image.new('L', (16, 16)); 화면그리기 = ImageDraw.Draw(ഡ്രോയിംഗ്_മൂല്യം)
        if not (പ്രതീകം_എന്_കോഡുചെയ്യല് < 32 or 0xd800 <= പ്രതീകം_എന്_കോഡുചെയ്യല് <= 0xdfff):
            화면그리기.text((0, -1 if പ്രതീകം_എന്_കോഡുചെയ്യല് < 256 else -5 if പ്രതീകം_എന്_കോഡുചെയ്യല് < 65536 else -3), chr(പ്രതീകം_എന്_കോഡുചെയ്യല്), font=ഫോണ്ട്_ലിസ്റ്റ്[0 if പ്രതീകം_എന്_കോഡുചെയ്യല് < 256 else 1 if പ്രതീകം_എന്_കോഡുചെയ്യല് < 65536 else 2], fill=255)
        for Y_ബട്ടൺ_ഏകോപനം in range(16):
            ബാക്_ഗ്രൗണ്ട്_ഇന്റലിജന്റ്_ട്രാൻസ്_ഫർ_സർവീസ്_ലിസ്റ്റ് = 0
            for x_ഏകോപനം in range(16): ബാക്_ഗ്രൗണ്ട്_ഇന്റലിജന്റ്_ട്രാൻസ്_ഫർ_സർവീസ്_ലിസ്റ്റ് = ബാക്_ഗ്രൗണ്ട്_ഇന്റലിജന്റ്_ട്രാൻസ്_ഫർ_സർവീസ്_ലിസ്റ്റ് * 2 + (ഡ്രോയിംഗ്_മൂല്യം.getpixel((x_ഏകോപനം, Y_ബട്ടൺ_ഏകോപനം)) >= 96)
            ഡാറ്റാ += ബാക്_ഗ്രൗണ്ട്_ഇന്റലിജന്റ്_ട്രാൻസ്_ഫർ_സർവീസ്_ലിസ്റ്റ്.to_bytes(2, 'big')
    ലക്_ഷ്യം = പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം / 'vendor/terminal-font.bin'; ലക്_ഷ്യം.write_bytes(ഡാറ്റാ)
    이용허락목록 = [Path('/usr/share/doc/fonts-noto-cjk/copyright'), Path('/usr/share/doc/fonts-dejavu-core/copyright')]
    for 원본주소 in 이용허락목록: (പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം / 'vendor' / ('LICENSE.' + 원본주소.parent.name)).write_bytes(원본주소.read_bytes())
    (പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം / 'vendor/terminal-font.json').write_text(json.dumps({'name': 'JKOROS terminal bitmap', 'format': '16 rows, big-endian uint16 mask; BMP then U+1F600..1F64F', 'glyphs': 65536+80, 'sha256': hashlib.sha256(ഡാറ്റാ).hexdigest(), 'sources': {ഡാറ്റാ_പദവി: hashlib.sha256(Path(ഡാറ്റാ_പദവി).read_bytes()).hexdigest() for ഡാറ്റാ_പദവി in പാത_ലിസ്റ്റ്}}, indent=2) + '\n')
    print(ലക്_ഷ്യം)


if __name__ == '__main__': നടപ്പിലാക്കുക()

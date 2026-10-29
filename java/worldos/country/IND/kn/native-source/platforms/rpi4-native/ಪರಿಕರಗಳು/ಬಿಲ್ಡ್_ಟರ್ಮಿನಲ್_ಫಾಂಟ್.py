#!/usr/bin/env python3
"""Noto CJK/DejaVu의 라이선스와 출처를 보존한 고정 폭 ಟರ್ಮಿನಲ್ 비트맵 ರಚಿಸಿ. 평상시 빌드는 vendor ಕಡತ 사용."""
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageDraw, ImageFont
ಬಿಂಬಿಸು_ಮೂಲ = Path(__file__).resolve().parents[1]


def ಚಲಾಯಿಸು_2():
    ಹಾದಿ_ಪಟ್ಟಿ = ['/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']
    ಫಾಂಟ್_ಪಟ್ಟಿ = [ImageFont.truetype(ಹಾದಿ_ಪಟ್ಟಿ[0], 13), ImageFont.truetype(ಹಾದಿ_ಪಟ್ಟಿ[1], 16, index=1), ImageFont.truetype(ಹಾದಿ_ಪಟ್ಟಿ[2], 16)]
    ಡೇಟಾ = bytearray()
    for ಅಕ್ಷರ_ಎನ್ಕೋಡಿಂಗ್ in list(range(65536)) + list(range(0x1f600, 0x1f650)):
        ಚಿತ್ರರಚನೆ_ಮೌಲ್ಯ = Image.new('L', (16, 16)); 화면그리기 = ImageDraw.Draw(ಚಿತ್ರರಚನೆ_ಮೌಲ್ಯ)
        if not (ಅಕ್ಷರ_ಎನ್ಕೋಡಿಂಗ್ < 32 or 0xd800 <= ಅಕ್ಷರ_ಎನ್ಕೋಡಿಂಗ್ <= 0xdfff):
            화면그리기.text((0, -1 if ಅಕ್ಷರ_ಎನ್ಕೋಡಿಂಗ್ < 256 else -5 if ಅಕ್ಷರ_ಎನ್ಕೋಡಿಂಗ್ < 65536 else -3), chr(ಅಕ್ಷರ_ಎನ್ಕೋಡಿಂಗ್), font=ಫಾಂಟ್_ಪಟ್ಟಿ[0 if ಅಕ್ಷರ_ಎನ್ಕೋಡಿಂಗ್ < 256 else 1 if ಅಕ್ಷರ_ಎನ್ಕೋಡಿಂಗ್ < 65536 else 2], fill=255)
        for Y_ಬಟನ್_ಸಮನ್ವಯ in range(16):
            ಹಿನ್ನೆಲೆ_ಬುದ್ಧಿವಂತಿಕೆಯ_ವರ್ಗಾವಣೆ_ಸೇವೆ_ಪಟ್ಟಿ = 0
            for x_ಸಮಭಾಜಕ in range(16): ಹಿನ್ನೆಲೆ_ಬುದ್ಧಿವಂತಿಕೆಯ_ವರ್ಗಾವಣೆ_ಸೇವೆ_ಪಟ್ಟಿ = ಹಿನ್ನೆಲೆ_ಬುದ್ಧಿವಂತಿಕೆಯ_ವರ್ಗಾವಣೆ_ಸೇವೆ_ಪಟ್ಟಿ * 2 + (ಚಿತ್ರರಚನೆ_ಮೌಲ್ಯ.getpixel((x_ಸಮಭಾಜಕ, Y_ಬಟನ್_ಸಮನ್ವಯ)) >= 96)
            ಡೇಟಾ += ಹಿನ್ನೆಲೆ_ಬುದ್ಧಿವಂತಿಕೆಯ_ವರ್ಗಾವಣೆ_ಸೇವೆ_ಪಟ್ಟಿ.to_bytes(2, 'big')
    ಲಕ್ಷ್ಯ = ಬಿಂಬಿಸು_ಮೂಲ / 'vendor/terminal-font.bin'; ಲಕ್ಷ್ಯ.write_bytes(ಡೇಟಾ)
    이용허락목록 = [Path('/usr/share/doc/fonts-noto-cjk/copyright'), Path('/usr/share/doc/fonts-dejavu-core/copyright')]
    for 원본주소 in 이용허락목록: (ಬಿಂಬಿಸು_ಮೂಲ / 'vendor' / ('LICENSE.' + 원본주소.parent.name)).write_bytes(원본주소.read_bytes())
    (ಬಿಂಬಿಸು_ಮೂಲ / 'vendor/terminal-font.json').write_text(json.dumps({'name': 'JKOROS terminal bitmap', 'format': '16 rows, big-endian uint16 mask; BMP then U+1F600..1F64F', 'glyphs': 65536+80, 'sha256': hashlib.sha256(ಡೇಟಾ).hexdigest(), 'sources': {ಡೇಟಾ_ಹುದ್ದೆ: hashlib.sha256(Path(ಡೇಟಾ_ಹುದ್ದೆ).read_bytes()).hexdigest() for ಡೇಟಾ_ಹುದ್ದೆ in ಹಾದಿ_ಪಟ್ಟಿ}}, indent=2) + '\n')
    print(ಲಕ್ಷ್ಯ)


if __name__ == '__main__': ಚಲಾಯಿಸು_2()

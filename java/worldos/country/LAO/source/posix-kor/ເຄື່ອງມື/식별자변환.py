#!/usr/bin/env python3
"""한국어 C 식별자만 UCN으로 옮긴다. ສະຕຣິງ_ຄ່າ·문자·주석·include 파일명은 보존한다."""
import argparse
from pathlib import Path
import re

ໂທເຄນ_ຄ່າ = re.compile(r'(?P<보존>//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|^[ \t]*#[ \t]*include[ \t]*<[^>]*>)|(?P<ຕົວ_ກໍາ_ນົດ_ຄ່າ>[^\W\d]\w*)', re.S | re.M)

def 변환(ແຫຼ່ງທີ່ມາ):
    def 바꾸기(일치):
        if 일치.lastgroup == '보존':
            return 일치[0]
        return ''.join(ຕົວອັກສອນ_ຄ່າ if ord(ຕົວອັກສອນ_ຄ່າ) < 128 else
                       ('\\u%04x' if ord(ຕົວອັກສອນ_ຄ່າ) <= 65535 else '\\U%08x') % ord(ຕົວອັກສອນ_ຄ່າ)
                       for ຕົວອັກສອນ_ຄ່າ in 일치[0])
    return ໂທເຄນ_ຄ່າ.sub(바꾸기, ແຫຼ່ງທີ່ມາ)

def ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ():
    ຕົວແຍກວິເຄາະ_48ee4b1b = argparse.ArgumentParser()
    ຕົວແຍກວິເຄາະ_48ee4b1b.add_argument('원본', type=Path)
    ຕົວແຍກວິເຄາະ_48ee4b1b.add_argument('출력', type=Path)
    인수 = ຕົວແຍກວິເຄາະ_48ee4b1b.parse_args()
    for ຟາຍ in sorted(인수.원본.rglob('*')):
        if ຟາຍ.suffix not in ('.c', '.h'):
            continue
        출력 = 인수.출력 / ຟາຍ.relative_to(인수.원본)
        출력.parent.mkdir(parents=True, exist_ok=True)
        새원문 = 변환(ຟາຍ.read_text())
        if not 출력.exists() or 출력.read_text() != 새원문:
            출력.write_text(새원문)

if __name__ == '__main__':
    ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ()

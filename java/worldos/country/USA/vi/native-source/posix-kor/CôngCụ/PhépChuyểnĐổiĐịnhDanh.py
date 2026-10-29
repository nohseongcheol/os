#!/usr/bin/env python3
"""tiếngViệt C 식별자만 UCN으로 옮긴다. ChuỗiKýTự·KýTự·주석·include 파일명은 보존한다."""
import argparse
from pathlib import Path
import re

giáTrịTừTố = re.compile(r'(?P<보존>//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|^[ \t]*#[ \t]*include[ \t]*<[^>]*>)|(?P<giáTrịĐịnhDanh>[^\W\d]\w*)', re.S | re.M)

def chuyểnĐổiGiáTrị(mãNguồn):
    def thayGiáTrị(làBằng):
        if làBằng.lastgroup == '보존':
            return làBằng[0]
        return ''.join(giáTrịKýTự if ord(giáTrịKýTự) < 128 else
                       ('\\u%04x' if ord(giáTrịKýTự) <= 65535 else '\\U%08x') % ord(giáTrịKýTự)
                       for giáTrịKýTự in làBằng[0])
    return giáTrịTừTố.sub(thayGiáTrị, mãNguồn)

def thựcThiLệnh():
    BộPhânTích = argparse.ArgumentParser()
    BộPhânTích.add_argument('nguyênBản', type=Path)
    BộPhânTích.add_argument('ĐầuRa', type=Path)
    cácĐốiSố = BộPhânTích.parse_args()
    for Tệp in sorted(cácĐốiSố.nguyênBản.rglob('*')):
        if Tệp.suffix not in ('.c', '.h'):
            continue
        ĐầuRa = cácĐốiSố.ĐầuRa / Tệp.relative_to(cácĐốiSố.nguyênBản)
        ĐầuRa.parent.mkdir(parents=True, exist_ok=True)
        nguồnMới = chuyểnĐổiGiáTrị(Tệp.read_text())
        if not ĐầuRa.exists() or ĐầuRa.read_text() != nguồnMới:
            ĐầuRa.write_text(nguồnMới)

if __name__ == '__main__':
    thựcThiLệnh()

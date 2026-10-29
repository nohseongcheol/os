#!/usr/bin/env python3
"""tựThân Java phạmViCụcBộ 이름을 바꾼다. ChuỗiKýTự·주석·giáTrịBênNgoài 멤버 이름은 보존한다."""
import json
import re
from pathlib import Path

gốcCâyDựÁn = Path(__file__).resolve().parents[1]
giáTrịPhépÁnhXạ = json.loads((gốcCâyDựÁn / 'cáchĐặtTên/cácTênJava.json').read_text())
biểuThứcMảnh = re.compile(r'//[^\n]*|/\*[\s\S]*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|[\w$]+|[^\w\s]', re.UNICODE)
bảnGhiNhậtKý = []
for giáTrịThưMục in ('mãNguồn', 'NgườiDùng/Java', 'JavaTiếngViệt'):
    for đườngDẫn in sorted((gốcCâyDựÁn / giáTrịThưMục).rglob('*.java')):
        mãNguồn = đườngDẫn.read_text()
        danhSáchCácMảnh = list(biểuThứcMảnh.finditer(mãNguồn))
        tênĐãDùng = {mụcMảnh.group() for mụcMảnh in danhSáchCácMảnh if re.search('[toánHạngĐầuTiên-힣]', mụcMảnh.group())}
        phépÁnhXạTệp = {}
        for phầnMụcTrướcĐó, giáTrịSau in giáTrịPhépÁnhXạ.items():
            # A pre-existing Korean binding must never be shadowed by renaming.
            tênMới = giáTrịSau
            while tênMới in tênĐãDùng: tênMới = 'phạmViCụcBộ' + tênMới
            phépÁnhXạTệp[phầnMụcTrướcĐó] = tênMới
        chỉnhSửaGiáTrị = []
        mảnhTrướcĐó = ''
        for mụcMảnh in danhSáchCácMảnh:
            từTừVựng = mụcMảnh.group()
            if từTừVựng.startswith(('//', '/*', '"', "'")): continue
            if từTừVựng in phépÁnhXạTệp and mảnhTrướcĐó != '.':
                chỉnhSửaGiáTrị.append((mụcMảnh.start(), mụcMảnh.end(), phépÁnhXạTệp[từTừVựng]))
                bảnGhiNhậtKý.append((str(đườngDẫn.relative_to(gốcCâyDựÁn)), từTừVựng, phépÁnhXạTệp[từTừVựng]))
            mảnhTrướcĐó = từTừVựng
        for chạy, phầnKết, tênMới in reversed(chỉnhSửaGiáTrị): mãNguồn = mãNguồn[:chạy] + tênMới + mãNguồn[phầnKết:]
        if chỉnhSửaGiáTrị: đườngDẫn.write_text(mãNguồn)
(gốcCâyDựÁn / 'cáchĐặtTên/phépÁnhXạTênJava.tsv').write_text('Tệp\t이전\t이후\n' + ''.join('\t'.join(giáTrịMục)+'\n' for giáTrịMục in sorted(set(bảnGhiNhậtKý))))
print('Java tên thamChiếu đổiGiáTrị:', len(bảnGhiNhậtKý))

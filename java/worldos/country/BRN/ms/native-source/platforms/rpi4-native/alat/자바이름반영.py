#!/usr/bin/env python3
"""Asli Java setempat_Skop 이름을 바꾼다. rentetan_VALUE·주석·외부 멤버 이름은 보존한다."""
import json
import re
from pathlib import Path

projek_akar = Path(__file__).resolve().parents[1]
대응 = json.loads((projek_akar / '명명/자바이름.json').read_text())
cebis_ungkapan = re.compile(r'//[^\n]*|/\*[\s\S]*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|[\w$]+|[^\w\s]', re.UNICODE)
LOG_baris = []
for direktori_VALUE in ('SUMBER', 'ruang_pengguna/자바', '한국어자바'):
    for LALUAN in sorted((projek_akar / direktori_VALUE).rglob('*.java')):
        SUMBER = LALUAN.read_text()
        토막들 = list(cebis_ungkapan.finditer(SUMBER))
        사용이름 = {cebis_pemasukan.group() for cebis_pemasukan in 토막들 if re.search('[가-힣]', cebis_pemasukan.group())}
        pemetaan_fail = {}
        for 이전, 이후 in 대응.items():
            # A pre-existing Korean binding must never be shadowed by renaming.
            새이름 = 이후
            while 새이름 in 사용이름: 새이름 = 'setempat_Skop' + 새이름
            pemetaan_fail[이전] = 새이름
        수정 = []
        이전토막 = ''
        for cebis_pemasukan in 토막들:
            낱말 = cebis_pemasukan.group()
            if 낱말.startswith(('//', '/*', '"', "'")): continue
            if 낱말 in pemetaan_fail and 이전토막 != '.':
                수정.append((cebis_pemasukan.start(), cebis_pemasukan.end(), pemetaan_fail[낱말]))
                LOG_baris.append((str(LALUAN.relative_to(projek_akar)), 낱말, pemetaan_fail[낱말]))
            이전토막 = 낱말
        for Jalan, 끝, 새이름 in reversed(수정): SUMBER = SUMBER[:Jalan] + 새이름 + SUMBER[끝:]
        if 수정: LALUAN.write_text(SUMBER)
(projek_akar / '명명/자바이름대응.tsv').write_text('Fail\t이전\t이후\n' + ''.join('\t'.join(pemasukan_VALUE)+'\n' for pemasukan_VALUE in sorted(set(LOG_baris))))
print('Java Nama Rujukan ubah_VALUE:', len(LOG_baris))

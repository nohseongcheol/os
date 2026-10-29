#!/usr/bin/env python3
"""Asli Java lokal_Cakupan 이름을 바꾼다. string_VALUE·주석·eksternal_VALUE 멤버 이름은 보존한다."""
import json
import re
from pathlib import Path

Tugas_akar = Path(__file__).resolve().parents[1]
대응 = json.loads((Tugas_akar / '명명/자바이름.json').read_text())
gugus_ekspresi = re.compile(r'//[^\n]*|/\*[\s\S]*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|[\w$]+|[^\w\s]', re.UNICODE)
LOG_baris = []
for Direktori_VALUE in ('kodeSumber', 'ruang_pengguna/자바', '한국어자바'):
    for jalur in sorted((Tugas_akar / Direktori_VALUE).rglob('*.java')):
        kodeSumber = jalur.read_text()
        토막들 = list(gugus_ekspresi.finditer(kodeSumber))
        사용이름 = {gugus_entri.group() for gugus_entri in 토막들 if re.search('[가-힣]', gugus_entri.group())}
        pemetaan_file = {}
        for 이전, 이후 in 대응.items():
            # A pre-existing Korean binding must never be shadowed by renaming.
            새이름 = 이후
            while 새이름 in 사용이름: 새이름 = 'lokal_Cakupan' + 새이름
            pemetaan_file[이전] = 새이름
        수정 = []
        이전토막 = ''
        for gugus_entri in 토막들:
            낱말 = gugus_entri.group()
            if 낱말.startswith(('//', '/*', '"', "'")): continue
            if 낱말 in pemetaan_file and 이전토막 != '.':
                수정.append((gugus_entri.start(), gugus_entri.end(), pemetaan_file[낱말]))
                LOG_baris.append((str(jalur.relative_to(Tugas_akar)), 낱말, pemetaan_file[낱말]))
            이전토막 = 낱말
        for jalankan, 끝, 새이름 in reversed(수정): kodeSumber = kodeSumber[:jalankan] + 새이름 + kodeSumber[끝:]
        if 수정: jalur.write_text(kodeSumber)
(Tugas_akar / '명명/자바이름대응.tsv').write_text('berkas\t이전\t이후\n' + ''.join('\t'.join(entri_VALUE)+'\n' for entri_VALUE in sorted(set(LOG_baris))))
print('Java Nama_2 Referensi ubah_VALUE:', len(LOG_baris))

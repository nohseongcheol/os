#!/usr/bin/env python3
"""eget Java lokal_Omfang 이름을 바꾼다. streng_VERDI·주석·ekstern_VERDI 멤버 이름은 보존한다."""
import json
import re
from pathlib import Path

speile_rot = Path(__file__).resolve().parents[1]
tildeling_VERDI = json.loads((speile_rot / '명명/자바이름.json').read_text())
토막식 = re.compile(r'//[^\n]*|/\*[\s\S]*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|[\w$]+|[^\w\s]', re.UNICODE)
LOG_POST = []
for katalog_VERDI in ('KILDE', 'bruker/자바', '한국어자바'):
    for Sti in sorted((speile_rot / katalog_VERDI).rglob('*.java')):
        KILDE = Sti.read_text()
        토막들 = list(토막식.finditer(KILDE))
        사용이름 = {토막.group() for 토막 in 토막들 if re.search('[가-힣]', 토막.group())}
        Fil_tildeling = {}
        for Forrige_vare, 이후 in tildeling_VERDI.items():
            # A pre-existing Korean binding must never be shadowed by renaming.
            새이름 = 이후
            while 새이름 in 사용이름: 새이름 = 'lokal_Omfang' + 새이름
            Fil_tildeling[Forrige_vare] = 새이름
        수정 = []
        이전토막 = ''
        for 토막 in 토막들:
            낱말 = 토막.group()
            if 낱말.startswith(('//', '/*', '"', "'")): continue
            if 낱말 in Fil_tildeling and 이전토막 != '.':
                수정.append((토막.start(), 토막.end(), Fil_tildeling[낱말]))
                LOG_POST.append((str(Sti.relative_to(speile_rot)), 낱말, Fil_tildeling[낱말]))
            이전토막 = 낱말
        for Kjør_2, 끝, 새이름 in reversed(수정): KILDE = KILDE[:Kjør_2] + 새이름 + KILDE[끝:]
        if 수정: Sti.write_text(KILDE)
(speile_rot / '명명/자바이름대응.tsv').write_text('Fil\t이전\t이후\n' + ''.join('\t'.join(oppføring_VERDI)+'\n' for oppføring_VERDI in sorted(set(LOG_POST))))
print('Java Navn referere endre_VERDI:', len(LOG_POST))

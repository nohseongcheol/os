#!/usr/bin/env python3
"""자체 Java dënnd_nameef 이름을 바꾼다. araf_yu_bennoo_xëyma·주석·외부 멤버 이름은 보존한다."""
import json
import re
from pathlib import Path

기준 = Path(__file__).resolve().parents[1]
대응 = json.loads((기준 / '명명/자바이름.json').read_text())
토막식 = re.compile(r'//[^\n]*|/\*[\s\S]*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|[\w$]+|[^\w\s]', re.UNICODE)
làq_Dënk = []
for dàmb_xëyma in ('Cosaan', 'kiy_jariñoo_internet/자바', '한국어자바'):
    for Yoonu_jëmale in sorted((기준 / dàmb_xëyma).rglob('*.java')):
        Cosaan = Yoonu_jëmale.read_text()
        토막들 = list(토막식.finditer(Cosaan))
        사용이름 = {토막.group() for 토막 in 토막들 if re.search('[가-힣]', 토막.group())}
        이파일대응 = {}
        for 이전, 이후 in 대응.items():
            # A pre-existing Korean binding must never be shadowed by renaming.
            새이름 = 이후
            while 새이름 in 사용이름: 새이름 = 'dënnd_nameef' + 새이름
            이파일대응[이전] = 새이름
        수정 = []
        이전토막 = ''
        for 토막 in 토막들:
            낱말 = 토막.group()
            if 낱말.startswith(('//', '/*', '"', "'")): continue
            if 낱말 in 이파일대응 and 이전토막 != '.':
                수정.append((토막.start(), 토막.end(), 이파일대응[낱말]))
                làq_Dënk.append((str(Yoonu_jëmale.relative_to(기준)), 낱말, 이파일대응[낱말]))
            이전토막 = 낱말
        for daw, 끝, 새이름 in reversed(수정): Cosaan = Cosaan[:daw] + 새이름 + Cosaan[끝:]
        if 수정: Yoonu_jëmale.write_text(Cosaan)
(기준 / '명명/자바이름대응.tsv').write_text('bara_denc\t이전\t이후\n' + ''.join('\t'.join(dugal_xabaar_xëyma)+'\n' for dugal_xabaar_xëyma in sorted(set(làq_Dënk))))
print('Java tur_253d1510 Royukaay soppi_xëyma_16f64fe4:', len(làq_Dënk))

#!/usr/bin/env python3
"""eigin Java staðbundið_umfang 이름을 바꾼다. strengur_VALUE·주석·외부 멤버 이름은 보존한다."""
import json
import re
from pathlib import Path

verk_rót = Path(__file__).resolve().parents[1]
vörpun_VALUE = json.loads((verk_rót / '명명/자바이름.json').read_text())
토막식 = re.compile(r'//[^\n]*|/\*[\s\S]*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|[\w$]+|[^\w\s]', re.UNICODE)
LOG_lína = []
for skráasafn_VALUE in ('Uppruni', 'notandi/자바', '한국어자바'):
    for SLÓÐ in sorted((verk_rót / skráasafn_VALUE).rglob('*.java')):
        Uppruni = SLÓÐ.read_text()
        토막들 = list(토막식.finditer(Uppruni))
        사용이름 = {토막.group() for 토막 in 토막들 if re.search('[가-힣]', 토막.group())}
        skrá_vörpun = {}
        for 이전, 이후 in vörpun_VALUE.items():
            # A pre-existing Korean binding must never be shadowed by renaming.
            새이름 = 이후
            while 새이름 in 사용이름: 새이름 = 'staðbundið_umfang' + 새이름
            skrá_vörpun[이전] = 새이름
        수정 = []
        이전토막 = ''
        for 토막 in 토막들:
            낱말 = 토막.group()
            if 낱말.startswith(('//', '/*', '"', "'")): continue
            if 낱말 in skrá_vörpun and 이전토막 != '.':
                수정.append((토막.start(), 토막.end(), skrá_vörpun[낱말]))
                LOG_lína.append((str(SLÓÐ.relative_to(verk_rót)), 낱말, skrá_vörpun[낱말]))
            이전토막 = 낱말
        for Keyra_2, 끝, 새이름 in reversed(수정): Uppruni = Uppruni[:Keyra_2] + 새이름 + Uppruni[끝:]
        if 수정: SLÓÐ.write_text(Uppruni)
(verk_rót / '명명/자바이름대응.tsv').write_text('Skrá\t이전\t이후\n' + ''.join('\t'.join(færsla_VALUE)+'\n' for færsla_VALUE in sorted(set(LOG_lína))))
print('Java Heiti tilvísun breyta_VALUE_16f64fe4:', len(LOG_lína))

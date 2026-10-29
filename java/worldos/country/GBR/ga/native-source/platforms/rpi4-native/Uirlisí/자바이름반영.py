#!/usr/bin/env python3
"""자체 Java logánta_scóip 이름을 바꾼다. teaghrán_VALUE·주석·외부 멤버 이름은 보존한다."""
import json
import re
from pathlib import Path

teilgean_fréamh = Path(__file__).resolve().parents[1]
대응 = json.loads((teilgean_fréamh / '명명/자바이름.json').read_text())
토막식 = re.compile(r'//[^\n]*|/\*[\s\S]*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|[\w$]+|[^\w\s]', re.UNICODE)
LOG_ró = []
for eolaire_VALUE in ('FOINSE', 'úsáideoir/자바', '한국어자바'):
    for CONAIR in sorted((teilgean_fréamh / eolaire_VALUE).rglob('*.java')):
        FOINSE = CONAIR.read_text()
        토막들 = list(토막식.finditer(FOINSE))
        사용이름 = {토막.group() for 토막 in 토막들 if re.search('[가-힣]', 토막.group())}
        이파일대응 = {}
        for 이전, 이후 in 대응.items():
            # A pre-existing Korean binding must never be shadowed by renaming.
            새이름 = 이후
            while 새이름 in 사용이름: 새이름 = 'logánta_scóip' + 새이름
            이파일대응[이전] = 새이름
        수정 = []
        이전토막 = ''
        for 토막 in 토막들:
            낱말 = 토막.group()
            if 낱말.startswith(('//', '/*', '"', "'")): continue
            if 낱말 in 이파일대응 and 이전토막 != '.':
                수정.append((토막.start(), 토막.end(), 이파일대응[낱말]))
                LOG_ró.append((str(CONAIR.relative_to(teilgean_fréamh)), 낱말, 이파일대응[낱말]))
            이전토막 = 낱말
        for Rith_2, 끝, 새이름 in reversed(수정): FOINSE = FOINSE[:Rith_2] + 새이름 + FOINSE[끝:]
        if 수정: CONAIR.write_text(FOINSE)
(teilgean_fréamh / '명명/자바이름대응.tsv').write_text('Comhad\t이전\t이후\n' + ''.join('\t'.join(iontráil_VALUE)+'\n' for iontráil_VALUE in sorted(set(LOG_ró))))
print('Java Ainm Leabhair_thagartha athraigh_VALUE:', len(LOG_ró))

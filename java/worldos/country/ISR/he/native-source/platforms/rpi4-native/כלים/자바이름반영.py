#!/usr/bin/env python3
"""עצמי Java מקומי_היקף 이름을 바꾼다. מחרוזת_ערך·주석·חיצוני_ערך 멤버 이름은 보존한다."""
import json
import re
from pathlib import Path

לשקף_בסיס = Path(__file__).resolve().parents[1]
대응 = json.loads((לשקף_בסיס / '명명/자바이름.json').read_text())
토막식 = re.compile(r'//[^\n]*|/\*[\s\S]*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|[\w$]+|[^\w\s]', re.UNICODE)
לרשום_שיא = []
for מדריך_ערך in ('קודמקור', 'משתמש/자바', '한국어자바'):
    for נתיב in sorted((לשקף_בסיס / מדריך_ערך).rglob('*.java')):
        קודמקור = נתיב.read_text()
        토막들 = list(토막식.finditer(קודמקור))
        사용이름 = {토막.group() for 토막 in 토막들 if re.search('[가-힣]', 토막.group())}
        이파일대응 = {}
        for 이전, 이후 in 대응.items():
            # A pre-existing Korean binding must never be shadowed by renaming.
            새이름 = 이후
            while 새이름 in 사용이름: 새이름 = 'מקומי_היקף' + 새이름
            이파일대응[이전] = 새이름
        수정 = []
        이전토막 = ''
        for 토막 in 토막들:
            낱말 = 토막.group()
            if 낱말.startswith(('//', '/*', '"', "'")): continue
            if 낱말 in 이파일대응 and 이전토막 != '.':
                수정.append((토막.start(), 토막.end(), 이파일대응[낱말]))
                לרשום_שיא.append((str(נתיב.relative_to(לשקף_בסיס)), 낱말, 이파일대응[낱말]))
            이전토막 = 낱말
        for הפעלה, 끝, 새이름 in reversed(수정): קודמקור = קודמקור[:הפעלה] + 새이름 + קודמקור[끝:]
        if 수정: נתיב.write_text(קודמקור)
(לשקף_בסיס / '명명/자바이름대응.tsv').write_text('קובץ\t이전\t이후\n' + ''.join('\t'.join(ערך_ערך)+'\n' for ערך_ערך in sorted(set(לרשום_שיא))))
print('Java שם הפנה שנה_ערך:', len(לרשום_שיא))

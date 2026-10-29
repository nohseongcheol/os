#!/usr/bin/env python3
"""بومی Java محلی_محدوده 이름을 바꾼다. رشته_مقدار_6ca8363c·주석·외부 멤버 이름은 보존한다."""
import json
import re
from pathlib import Path

نمایش_دادن_جذر = Path(__file__).resolve().parents[1]
대응 = json.loads((نمایش_دادن_جذر / '명명/자바이름.json').read_text())
토막식 = re.compile(r'//[^\n]*|/\*[\s\S]*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|[\w$]+|[^\w\s]', re.UNICODE)
واقعه_نگار_ردیف = []
for فهرست_مقدار_e5561a2b in ('مبداء', 'کاربر/자바', '한국어자바'):
    for مسیر in sorted((نمایش_دادن_جذر / فهرست_مقدار_e5561a2b).rglob('*.java')):
        مبداء = مسیر.read_text()
        토막들 = list(토막식.finditer(مبداء))
        사용이름 = {토막.group() for 토막 in 토막들 if re.search('[가-힣]', 토막.group())}
        이파일대응 = {}
        for 이전, 이후 in 대응.items():
            # A pre-existing Korean binding must never be shadowed by renaming.
            새이름 = 이후
            while 새이름 in 사용이름: 새이름 = 'محلی_محدوده' + 새이름
            이파일대응[이전] = 새이름
        수정 = []
        이전토막 = ''
        for 토막 in 토막들:
            낱말 = 토막.group()
            if 낱말.startswith(('//', '/*', '"', "'")): continue
            if 낱말 in 이파일대응 and 이전토막 != '.':
                수정.append((토막.start(), 토막.end(), 이파일대응[낱말]))
                واقعه_نگار_ردیف.append((str(مسیر.relative_to(نمایش_دادن_جذر)), 낱말, 이파일대응[낱말]))
            이전토막 = 낱말
        for اجرا_2, 끝, 새이름 in reversed(수정): مبداء = مبداء[:اجرا_2] + 새이름 + مبداء[끝:]
        if 수정: مسیر.write_text(مبداء)
(نمایش_دادن_جذر / '명명/자바이름대응.tsv').write_text('پرونده\t이전\t이후\n' + ''.join('\t'.join(ورودی_مقدار)+'\n' for ورودی_مقدار in sorted(set(واقعه_نگار_ردیف))))
print('Java نام مرجع تغییر_مقدار:', len(واقعه_نگار_ردیف))

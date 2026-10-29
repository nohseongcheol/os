#!/usr/bin/env python3
"""اپنا Java مقامی_اسکوپ 이름을 바꾼다. سلک_قدر·주석·외부 멤버 이름은 보존한다."""
import json
import re
from pathlib import Path

عکس_ڈالنا_روٹ = Path(__file__).resolve().parents[1]
대응 = json.loads((عکس_ڈالنا_روٹ / '명명/자바이름.json').read_text())
토막식 = re.compile(r'//[^\n]*|/\*[\s\S]*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|[\w$]+|[^\w\s]', re.UNICODE)
لاگ_صف = []
for ڈائریکٹری_قدر in ('ماخذ_فائل', 'صارف/자바', '한국어자바'):
    for راستہ_2 in sorted((عکس_ڈالنا_روٹ / ڈائریکٹری_قدر).rglob('*.java')):
        ماخذ_فائل = راستہ_2.read_text()
        토막들 = list(토막식.finditer(ماخذ_فائل))
        사용이름 = {토막.group() for 토막 in 토막들 if re.search('[가-힣]', 토막.group())}
        이파일대응 = {}
        for 이전, 이후 in 대응.items():
            # A pre-existing Korean binding must never be shadowed by renaming.
            새이름 = 이후
            while 새이름 in 사용이름: 새이름 = 'مقامی_اسکوپ' + 새이름
            이파일대응[이전] = 새이름
        수정 = []
        이전토막 = ''
        for 토막 in 토막들:
            낱말 = 토막.group()
            if 낱말.startswith(('//', '/*', '"', "'")): continue
            if 낱말 in 이파일대응 and 이전토막 != '.':
                수정.append((토막.start(), 토막.end(), 이파일대응[낱말]))
                لاگ_صف.append((str(راستہ_2.relative_to(عکس_ڈالنا_روٹ)), 낱말, 이파일대응[낱말]))
            이전토막 = 낱말
        for چلائیں, 끝, 새이름 in reversed(수정): ماخذ_فائل = ماخذ_فائل[:چلائیں] + 새이름 + ماخذ_فائل[끝:]
        if 수정: راستہ_2.write_text(ماخذ_فائل)
(عکس_ڈالنا_روٹ / '명명/자바이름대응.tsv').write_text('فائل_کا_نام\t이전\t이후\n' + ''.join('\t'.join(اندراج_قدر)+'\n' for اندراج_قدر in sorted(set(لاگ_صف))))
print('Java نام حوالہ_جات تبدیل_کریں_قدر:', len(لاگ_صف))

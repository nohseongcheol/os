#!/usr/bin/env python3
"""ذاتي Java محلي_نطاق 이름을 바꾼다. سلسلة_قيمة·주석·خارجي_قيمة 멤버 이름은 보존한다."""
import json
import re
from pathlib import Path

يعرض_جذر = Path(__file__).resolve().parents[1]
대응 = json.loads((يعرض_جذر / '명명/자바이름.json').read_text())
مجموعة_تعبير = re.compile(r'//[^\n]*|/\*[\s\S]*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|[\w$]+|[^\w\s]', re.UNICODE)
سجل_سجل = []
for دليل_قيمة in ('مصدر', 'فضاء_المستخدم/자바', '한국어자바'):
    for مسار in sorted((يعرض_جذر / دليل_قيمة).rglob('*.java')):
        مصدر = مسار.read_text()
        토막들 = list(مجموعة_تعبير.finditer(مصدر))
        사용이름 = {مجموعة_إدخال.group() for مجموعة_إدخال in 토막들 if re.search('[가-힣]', مجموعة_إدخال.group())}
        تعيين_ملف = {}
        for 이전, 이후 in 대응.items():
            # A pre-existing Korean binding must never be shadowed by renaming.
            새이름 = 이후
            while 새이름 in 사용이름: 새이름 = 'محلي_نطاق' + 새이름
            تعيين_ملف[이전] = 새이름
        수정 = []
        이전토막 = ''
        for مجموعة_إدخال in 토막들:
            낱말 = مجموعة_إدخال.group()
            if 낱말.startswith(('//', '/*', '"', "'")): continue
            if 낱말 in تعيين_ملف and 이전토막 != '.':
                수정.append((مجموعة_إدخال.start(), مجموعة_إدخال.end(), تعيين_ملف[낱말]))
                سجل_سجل.append((str(مسار.relative_to(يعرض_جذر)), 낱말, تعيين_ملف[낱말]))
            이전토막 = 낱말
        for تشغيل, 끝, 새이름 in reversed(수정): مصدر = مصدر[:تشغيل] + 새이름 + مصدر[끝:]
        if 수정: مسار.write_text(مصدر)
(يعرض_جذر / '명명/자바이름대응.tsv').write_text('ملف\t이전\t이후\n' + ''.join('\t'.join(إدخال_قيمة_962f286b)+'\n' for إدخال_قيمة_962f286b in sorted(set(سجل_سجل))))
print('Java اسم مرجع يغيّر_قيمة:', len(سجل_سجل))

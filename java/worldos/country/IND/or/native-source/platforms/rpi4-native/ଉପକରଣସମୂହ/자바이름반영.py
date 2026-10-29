#!/usr/bin/env python3
"""자체 Java ସ୍ଥାନୀୟ_ପରିସର 이름을 바꾼다. ଷ୍ଟ୍ରିଂ_ମୂଲ୍ୟ·주석·외부 멤버 이름은 보존한다."""
import json
import re
from pathlib import Path

ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ = Path(__file__).resolve().parents[1]
대응 = json.loads((ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ / '명명/자바이름.json').read_text())
토막식 = re.compile(r'//[^\n]*|/\*[\s\S]*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|[\w$]+|[^\w\s]', re.UNICODE)
ଲଗ୍_ଧାଡ଼ି = []
for ଡିରେକ୍ଟୋରୀ_ମୂଲ୍ୟ in ('ଉତ୍ସ', 'ଉପଭୋକ୍ତା/자바', '한국어자바'):
    for ପଥ in sorted((ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ / ଡିରେକ୍ଟୋରୀ_ମୂଲ୍ୟ).rglob('*.java')):
        ଉତ୍ସ = ପଥ.read_text()
        토막들 = list(토막식.finditer(ଉତ୍ସ))
        사용이름 = {토막.group() for 토막 in 토막들 if re.search('[가-힣]', 토막.group())}
        이파일대응 = {}
        for 이전, 이후 in 대응.items():
            # A pre-existing Korean binding must never be shadowed by renaming.
            새이름 = 이후
            while 새이름 in 사용이름: 새이름 = 'ସ୍ଥାନୀୟ_ପରିସର' + 새이름
            이파일대응[이전] = 새이름
        수정 = []
        이전토막 = ''
        for 토막 in 토막들:
            낱말 = 토막.group()
            if 낱말.startswith(('//', '/*', '"', "'")): continue
            if 낱말 in 이파일대응 and 이전토막 != '.':
                수정.append((토막.start(), 토막.end(), 이파일대응[낱말]))
                ଲଗ୍_ଧାଡ଼ି.append((str(ପଥ.relative_to(ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍)), 낱말, 이파일대응[낱말]))
            이전토막 = 낱말
        for ଚଳାନ୍ତୁ, 끝, 새이름 in reversed(수정): ଉତ୍ସ = ଉତ୍ସ[:ଚଳାନ୍ତୁ] + 새이름 + ଉତ୍ସ[끝:]
        if 수정: ପଥ.write_text(ଉତ୍ସ)
(ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ / '명명/자바이름대응.tsv').write_text('ଫାଇଲ\t이전\t이후\n' + ''.join('\t'.join(ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ)+'\n' for ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ in sorted(set(ଲଗ୍_ଧାଡ଼ି))))
print('Java ନାମ ପ୍ରସଙ୍ଗ ପରିବର୍ତ୍ତନ_ମୂଲ୍ୟ:', len(ଲଗ୍_ଧାଡ଼ି))

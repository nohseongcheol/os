#!/usr/bin/env python3
"""eget Java lokal_scope 이름을 바꾼다. sträng_värde·주석·extern_värde 멤버 이름은 보존한다."""
import json
import re
from pathlib import Path

åtgärd_rot = Path(__file__).resolve().parents[1]
mappning_värde = json.loads((åtgärd_rot / '명명/자바이름.json').read_text())
segment_uttryck = re.compile(r'//[^\n]*|/\*[\s\S]*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|[\w$]+|[^\w\s]', re.UNICODE)
LOG_POST = []
for Katalog_värde in ('källfil', 'användarutrymme/자바', '한국어자바'):
    for sökväg_2 in sorted((åtgärd_rot / Katalog_värde).rglob('*.java')):
        källfil = sökväg_2.read_text()
        토막들 = list(segment_uttryck.finditer(källfil))
        사용이름 = {segment_post.group() for segment_post in 토막들 if re.search('[가-힣]', segment_post.group())}
        filmappning = {}
        for Föregående_objekt, 이후 in mappning_värde.items():
            # A pre-existing Korean binding must never be shadowed by renaming.
            새이름 = 이후
            while 새이름 in 사용이름: 새이름 = 'lokal_scope' + 새이름
            filmappning[Föregående_objekt] = 새이름
        수정 = []
        Föregående_segment = ''
        for segment_post in 토막들:
            낱말 = segment_post.group()
            if 낱말.startswith(('//', '/*', '"', "'")): continue
            if 낱말 in filmappning and Föregående_segment != '.':
                수정.append((segment_post.start(), segment_post.end(), filmappning[낱말]))
                LOG_POST.append((str(sökväg_2.relative_to(åtgärd_rot)), 낱말, filmappning[낱말]))
            Föregående_segment = 낱말
        for Kör, 끝, 새이름 in reversed(수정): källfil = källfil[:Kör] + 새이름 + källfil[끝:]
        if 수정: sökväg_2.write_text(källfil)
(åtgärd_rot / '명명/자바이름대응.tsv').write_text('filnamn\t이전\t이후\n' + ''.join('\t'.join(post_värde)+'\n' for post_värde in sorted(set(LOG_POST))))
print('Java Namn referens ändra_värde:', len(LOG_POST))

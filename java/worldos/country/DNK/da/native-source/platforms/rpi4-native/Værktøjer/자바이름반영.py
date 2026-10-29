#!/usr/bin/env python3
"""eget Java lokal_Omfang 이름을 바꾼다. streng_VÆRDI·주석·ekstern_VÆRDI 멤버 이름은 보존한다."""
import json
import re
from pathlib import Path

To_do_rod = Path(__file__).resolve().parents[1]
tilknytning_VÆRDI = json.loads((To_do_rod / '명명/자바이름.json').read_text())
del_udtryk = re.compile(r'//[^\n]*|/\*[\s\S]*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|[\w$]+|[^\w\s]', re.UNICODE)
LOG_post = []
for mappe_VÆRDI in ('KILDE', 'bruger/자바', '한국어자바'):
    for Sti in sorted((To_do_rod / mappe_VÆRDI).rglob('*.java')):
        KILDE = Sti.read_text()
        토막들 = list(del_udtryk.finditer(KILDE))
        사용이름 = {del_post.group() for del_post in 토막들 if re.search('[가-힣]', del_post.group())}
        filtilknytning = {}
        for Forrige_vare, 이후 in tilknytning_VÆRDI.items():
            # A pre-existing Korean binding must never be shadowed by renaming.
            새이름 = 이후
            while 새이름 in 사용이름: 새이름 = 'lokal_Omfang' + 새이름
            filtilknytning[Forrige_vare] = 새이름
        수정 = []
        Forrige_del = ''
        for del_post in 토막들:
            낱말 = del_post.group()
            if 낱말.startswith(('//', '/*', '"', "'")): continue
            if 낱말 in filtilknytning and Forrige_del != '.':
                수정.append((del_post.start(), del_post.end(), filtilknytning[낱말]))
                LOG_post.append((str(Sti.relative_to(To_do_rod)), 낱말, filtilknytning[낱말]))
            Forrige_del = 낱말
        for Kør_2, 끝, 새이름 in reversed(수정): KILDE = KILDE[:Kør_2] + 새이름 + KILDE[끝:]
        if 수정: Sti.write_text(KILDE)
(To_do_rod / '명명/자바이름대응.tsv').write_text('Fil\t이전\t이후\n' + ''.join('\t'.join(post_VÆRDI_962f286b)+'\n' for post_VÆRDI_962f286b in sorted(set(LOG_post))))
print('Java Navn referere ændre_VÆRDI:', len(LOG_post))

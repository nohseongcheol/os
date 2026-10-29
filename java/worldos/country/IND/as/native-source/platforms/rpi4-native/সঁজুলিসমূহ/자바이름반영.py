#!/usr/bin/env python3
"""자체 Java স্থানীয়_সুযোগ 이름을 바꾼다. ষ্ট্ৰিং_মান·주석·외부 멤버 이름은 보존한다."""
import json
import re
from pathlib import Path

기준 = Path(__file__).resolve().parents[1]
대응 = json.loads((기준 / '명명/자바이름.json').read_text())
토막식 = re.compile(r'//[^\n]*|/\*[\s\S]*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|[\w$]+|[^\w\s]', re.UNICODE)
লগ_শাৰী = []
for ডাইৰেক্টৰী_মান in ('উৎস', 'ব্যৱহাৰকৰ্তা/자바', '한국어자바'):
    for পথ in sorted((기준 / ডাইৰেক্টৰী_মান).rglob('*.java')):
        উৎস = পথ.read_text()
        토막들 = list(토막식.finditer(উৎস))
        사용이름 = {토막.group() for 토막 in 토막들 if re.search('[가-힣]', 토막.group())}
        이파일대응 = {}
        for 이전, 이후 in 대응.items():
            # A pre-existing Korean binding must never be shadowed by renaming.
            새이름 = 이후
            while 새이름 in 사용이름: 새이름 = 'স্থানীয়_সুযোগ' + 새이름
            이파일대응[이전] = 새이름
        수정 = []
        이전토막 = ''
        for 토막 in 토막들:
            낱말 = 토막.group()
            if 낱말.startswith(('//', '/*', '"', "'")): continue
            if 낱말 in 이파일대응 and 이전토막 != '.':
                수정.append((토막.start(), 토막.end(), 이파일대응[낱말]))
                লগ_শাৰী.append((str(পথ.relative_to(기준)), 낱말, 이파일대응[낱말]))
            이전토막 = 낱말
        for সঞ্চালন, 끝, 새이름 in reversed(수정): উৎস = উৎস[:সঞ্চালন] + 새이름 + উৎস[끝:]
        if 수정: পথ.write_text(উৎস)
(기준 / '명명/자바이름대응.tsv').write_text('নথিপত্ৰ\t이전\t이후\n' + ''.join('\t'.join(প্রবিষ্ট_মান)+'\n' for প্রবিষ্ট_মান in sorted(set(লগ_শাৰী))))
print('Java নাম 참조 পৰিবৰ্তন_কৰক_মান:', len(লগ_শাৰী))

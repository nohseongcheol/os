#!/usr/bin/env python3
"""নিজ Java স্থানীয়_সুযোগ 이름을 바꾼다. স্ট্রিং_মান·주석·외부 멤버 이름은 보존한다."""
import json
import re
from pathlib import Path

প্রকল্প_মূল = Path(__file__).resolve().parents[1]
대응 = json.loads((প্রকল্প_মূল / '명명/자바이름.json').read_text())
토막식 = re.compile(r'//[^\n]*|/\*[\s\S]*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|[\w$]+|[^\w\s]', re.UNICODE)
লগ_সারি = []
for ডিরেক্টরি_মান in ('উৎস_নথি', 'ব্যবহারকারী/자바', '한국어자바'):
    for পথ_2 in sorted((প্রকল্প_মূল / ডিরেক্টরি_মান).rglob('*.java')):
        উৎস_নথি = পথ_2.read_text()
        토막들 = list(토막식.finditer(উৎস_নথি))
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
                লগ_সারি.append((str(পথ_2.relative_to(প্রকল্প_মূল)), 낱말, 이파일대응[낱말]))
            이전토막 = 낱말
        for চালনা, 끝, 새이름 in reversed(수정): উৎস_নথি = উৎস_নথি[:চালনা] + 새이름 + উৎস_নথি[끝:]
        if 수정: পথ_2.write_text(উৎস_নথি)
(প্রকল্প_মূল / '명명/자바이름대응.tsv').write_text('নথির_নাম\t이전\t이후\n' + ''.join('\t'.join(ভুক্তি_মান)+'\n' for ভুক্তি_মান in sorted(set(লগ_সারি))))
print('Java নাম প্রসঙ্গ পরিবর্তন_করা_মান:', len(লগ_সারি))

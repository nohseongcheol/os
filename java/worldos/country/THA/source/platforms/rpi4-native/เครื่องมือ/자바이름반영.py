#!/usr/bin/env python3
"""เอง Java ท้องถิ่น_ขอบเขต 이름을 바꾼다. สตริง_ค่า·주석·ภายนอก_ค่า 멤버 이름은 보존한다."""
import json
import re
from pathlib import Path

แสดง_ราก = Path(__file__).resolve().parents[1]
การแมป_ค่า = json.loads((แสดง_ราก / '명명/자바이름.json').read_text())
토막식 = re.compile(r'//[^\n]*|/\*[\s\S]*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|[\w$]+|[^\w\s]', re.UNICODE)
บันทึก_สถิติ = []
for ไดเรกทอรี_ค่า in ('รหัสต้นฉบับ', 'ผู้ใช้/자바', '한국어자바'):
    for เส้นทาง in sorted((แสดง_ราก / ไดเรกทอรี_ค่า).rglob('*.java')):
        รหัสต้นฉบับ = เส้นทาง.read_text()
        토막들 = list(토막식.finditer(รหัสต้นฉบับ))
        사용이름 = {토막.group() for 토막 in 토막들 if re.search('[가-힣]', 토막.group())}
        แฟ้ม_การแมป = {}
        for 이전, 이후 in การแมป_ค่า.items():
            # A pre-existing Korean binding must never be shadowed by renaming.
            새이름 = 이후
            while 새이름 in 사용이름: 새이름 = 'ท้องถิ่น_ขอบเขต' + 새이름
            แฟ้ม_การแมป[이전] = 새이름
        수정 = []
        이전토막 = ''
        for 토막 in 토막들:
            낱말 = 토막.group()
            if 낱말.startswith(('//', '/*', '"', "'")): continue
            if 낱말 in แฟ้ม_การแมป and 이전토막 != '.':
                수정.append((토막.start(), 토막.end(), แฟ้ม_การแมป[낱말]))
                บันทึก_สถิติ.append((str(เส้นทาง.relative_to(แสดง_ราก)), 낱말, แฟ้ม_การแมป[낱말]))
            이전토막 = 낱말
        for เรียกใช้งาน, 끝, 새이름 in reversed(수정): รหัสต้นฉบับ = รหัสต้นฉบับ[:เรียกใช้งาน] + 새이름 + รหัสต้นฉบับ[끝:]
        if 수정: เส้นทาง.write_text(รหัสต้นฉบับ)
(แสดง_ราก / '명명/자바이름대응.tsv').write_text('แฟ้ม\t이전\t이후\n' + ''.join('\t'.join(รายการ_ค่า)+'\n' for รายการ_ค่า in sorted(set(บันทึก_สถิติ))))
print('Java ชื่อ อ้างอิง เปลี่ยนแปลง_ค่า:', len(บันทึก_สถิติ))

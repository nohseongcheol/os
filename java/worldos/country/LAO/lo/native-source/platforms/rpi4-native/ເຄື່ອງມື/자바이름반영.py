#!/usr/bin/env python3
"""자체 Java ໃນເຄື່ອງ_ຂອບ_ເຂດ 이름을 바꾼다. ສະຕຣິງ_ຄ່າ·주석·외부 멤버 이름은 보존한다."""
import json
import re
from pathlib import Path

ໂຄງ_ການ_ເລກຮາກ = Path(__file__).resolve().parents[1]
대응 = json.loads((ໂຄງ_ການ_ເລກຮາກ / '명명/자바이름.json').read_text())
토막식 = re.compile(r'//[^\n]*|/\*[\s\S]*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|[\w$]+|[^\w\s]', re.UNICODE)
ບັນທຶກ_ແຖວ = []
for ກຸ່ມຂໍ້ມູນ_ຄ່າ in ('ແຫຼ່ງທີ່ມາ', 'ຜູ້ໃຊ້/자바', '한국어자바'):
    for ທາງໂຄຈອນ in sorted((ໂຄງ_ການ_ເລກຮາກ / ກຸ່ມຂໍ້ມູນ_ຄ່າ).rglob('*.java')):
        ແຫຼ່ງທີ່ມາ = ທາງໂຄຈອນ.read_text()
        토막들 = list(토막식.finditer(ແຫຼ່ງທີ່ມາ))
        사용이름 = {토막.group() for 토막 in 토막들 if re.search('[가-힣]', 토막.group())}
        이파일대응 = {}
        for 이전, 이후 in 대응.items():
            # A pre-existing Korean binding must never be shadowed by renaming.
            새이름 = 이후
            while 새이름 in 사용이름: 새이름 = 'ໃນເຄື່ອງ_ຂອບ_ເຂດ' + 새이름
            이파일대응[이전] = 새이름
        수정 = []
        이전토막 = ''
        for 토막 in 토막들:
            낱말 = 토막.group()
            if 낱말.startswith(('//', '/*', '"', "'")): continue
            if 낱말 in 이파일대응 and 이전토막 != '.':
                수정.append((토막.start(), 토막.end(), 이파일대응[낱말]))
                ບັນທຶກ_ແຖວ.append((str(ທາງໂຄຈອນ.relative_to(ໂຄງ_ການ_ເລກຮາກ)), 낱말, 이파일대응[낱말]))
            이전토막 = 낱말
        for ແລ່ນ, 끝, 새이름 in reversed(수정): ແຫຼ່ງທີ່ມາ = ແຫຼ່ງທີ່ມາ[:ແລ່ນ] + 새이름 + ແຫຼ່ງທີ່ມາ[끝:]
        if 수정: ທາງໂຄຈອນ.write_text(ແຫຼ່ງທີ່ມາ)
(ໂຄງ_ການ_ເລກຮາກ / '명명/자바이름대응.tsv').write_text('ຟາຍ\t이전\t이후\n' + ''.join('\t'.join(ເຂົ້າໃນ_ຄ່າ)+'\n' for ເຂົ້າໃນ_ຄ່າ in sorted(set(ບັນທຶກ_ແຖວ))))
print('Java ຊື່ ການ_ອ້າງ_ອີງ ປ່ຽນ_ແປງ_ຄ່າ:', len(ບັນທຶກ_ແຖວ))

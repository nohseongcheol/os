#!/usr/bin/env python3
"""자체 Java local_Ámbito 이름을 바꾼다. cadea_VALOR·주석·externo_VALOR 멤버 이름은 보존한다."""
import json
import re
from pathlib import Path

Project_raíz = Path(__file__).resolve().parents[1]
대응 = json.loads((Project_raíz / '명명/자바이름.json').read_text())
토막식 = re.compile(r'//[^\n]*|/\*[\s\S]*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|[\w$]+|[^\w\s]', re.UNICODE)
LOG_fila = []
for directorio_VALOR in ('FONTE', 'usuario/자바', '한국어자바'):
    for CAMIÑO in sorted((Project_raíz / directorio_VALOR).rglob('*.java')):
        FONTE = CAMIÑO.read_text()
        토막들 = list(토막식.finditer(FONTE))
        사용이름 = {토막.group() for 토막 in 토막들 if re.search('[가-힣]', 토막.group())}
        이파일대응 = {}
        for 이전, 이후 in 대응.items():
            # A pre-existing Korean binding must never be shadowed by renaming.
            새이름 = 이후
            while 새이름 in 사용이름: 새이름 = 'local_Ámbito' + 새이름
            이파일대응[이전] = 새이름
        수정 = []
        이전토막 = ''
        for 토막 in 토막들:
            낱말 = 토막.group()
            if 낱말.startswith(('//', '/*', '"', "'")): continue
            if 낱말 in 이파일대응 and 이전토막 != '.':
                수정.append((토막.start(), 토막.end(), 이파일대응[낱말]))
                LOG_fila.append((str(CAMIÑO.relative_to(Project_raíz)), 낱말, 이파일대응[낱말]))
            이전토막 = 낱말
        for Executar_2, 끝, 새이름 in reversed(수정): FONTE = FONTE[:Executar_2] + 새이름 + FONTE[끝:]
        if 수정: CAMIÑO.write_text(FONTE)
(Project_raíz / '명명/자바이름대응.tsv').write_text('Ficheiro\t이전\t이후\n' + ''.join('\t'.join(introdución_VALOR)+'\n' for introdución_VALOR in sorted(set(LOG_fila))))
print('Java Nome Material_de_referencia modificar_VALOR:', len(LOG_fila))

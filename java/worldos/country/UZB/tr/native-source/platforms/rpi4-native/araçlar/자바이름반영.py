#!/usr/bin/env python3
"""Öz Java yerel_Scope 이름을 바꾼다. dize_değer·주석·dış_değer 멤버 이름은 보존한다."""
import json
import re
from pathlib import Path

işlem_kök = Path(__file__).resolve().parents[1]
eşleme_değer = json.loads((işlem_kök / '명명/자바이름.json').read_text())
öbek_ifade = re.compile(r'//[^\n]*|/\*[\s\S]*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|[\w$]+|[^\w\s]', re.UNICODE)
LOG_KAYIT = []
for dizin_değer in ('kaynakKod', 'kullanıcı_alanı/자바', '한국어자바'):
    for yol in sorted((işlem_kök / dizin_değer).rglob('*.java')):
        kaynakKod = yol.read_text()
        토막들 = list(öbek_ifade.finditer(kaynakKod))
        사용이름 = {öbek_girdi.group() for öbek_girdi in 토막들 if re.search('[가-힣]', öbek_girdi.group())}
        dosya_eşlemesi = {}
        for Önceki_öğe, 이후 in eşleme_değer.items():
            # A pre-existing Korean binding must never be shadowed by renaming.
            새이름 = 이후
            while 새이름 in 사용이름: 새이름 = 'yerel_Scope' + 새이름
            dosya_eşlemesi[Önceki_öğe] = 새이름
        수정 = []
        Önceki_öbek = ''
        for öbek_girdi in 토막들:
            낱말 = öbek_girdi.group()
            if 낱말.startswith(('//', '/*', '"', "'")): continue
            if 낱말 in dosya_eşlemesi and Önceki_öbek != '.':
                수정.append((öbek_girdi.start(), öbek_girdi.end(), dosya_eşlemesi[낱말]))
                LOG_KAYIT.append((str(yol.relative_to(işlem_kök)), 낱말, dosya_eşlemesi[낱말]))
            Önceki_öbek = 낱말
        for çalıştır, 끝, 새이름 in reversed(수정): kaynakKod = kaynakKod[:çalıştır] + 새이름 + kaynakKod[끝:]
        if 수정: yol.write_text(kaynakKod)
(işlem_kök / '명명/자바이름대응.tsv').write_text('dosya\t이전\t이후\n' + ''.join('\t'.join(girdi_değer)+'\n' for girdi_değer in sorted(set(LOG_KAYIT))))
print('Java İsim Başvuru değiştirmek_değer:', len(LOG_KAYIT))

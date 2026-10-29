#!/bin/sh
set -eu
# 외국어판의 이름을 한국어 전용 규칙으로 거부하지 않는다.
# 뜻·어원 검토 여부는 native-pending.tsv와 native-term-evidence.json에 기록한다.
python3 - <<'PY'
from pathlib import Path
import re
import unicodedata
for Ճանապարհ in Path('ժառանգված_աղբյուր').rglob('*.java'):
    Անուն = Ճանապարհ.stem
    if not Անուն.isidentifier() or unicodedata.normalize('NFC', Անուն) != Անուն:
        raise SystemExit('նույնացուցիչ_արժեք 또는 կարգավորել_արժեք Սխալ: ' + str(Ճանապարհ))
    ԱՂԲՅՈՒՐ = Ճանապարհ.read_text(encoding='utf-8')
    선언 = re.search(r'public\s+(?:(?:final|abstract)\s+)?(?:class|interface|enum)\s+([^\s<{]+)', ԱՂԲՅՈՒՐ)
    if 선언 and 선언.group(1) != Անուն:
        raise SystemExit('Ֆայլ·공개 ձեւաչափ_արժեք Անուն 불일치: ' + str(Ճանապարհ))
print('UTF-8 공개 ձեւաչափ_արժեք·Ֆայլ Անուն հաստատել 완료; 현지어 검토 상태는 국가판 명명 տվյալ Տեղեկատուներ')
PY

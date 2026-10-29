#!/bin/sh
set -eu
# 외국어판의 이름을 한국어 전용 규칙으로 거부하지 않는다.
# 뜻·어원 검토 여부는 native-pending.tsv와 native-term-evidence.json에 기록한다.
python3 - <<'PY'
from pathlib import Path
import re
import unicodedata
for വഴി in Path('പാരമ്പര്യ_ഉറവിടം').rglob('*.java'):
    പേരു് = വഴി.stem
    if not പേരു്.isidentifier() or unicodedata.normalize('NFC', പേരു്) != പേരു്:
        raise SystemExit('ఐడెంటిఫయర్_മൂല്യം 또는 ക്രമാനുസരണമാക്കുക_മൂല്യം പിശക്: ' + str(വഴി))
    ഉറവിടം = വഴി.read_text(encoding='utf-8')
    പ്രസ്താവം = re.search(r'public\s+(?:(?:final|abstract)\s+)?(?:class|interface|enum)\s+([^\s<{]+)', ഉറവിടം)
    if പ്രസ്താവം and പ്രസ്താവം.group(1) != പേരു്:
        raise SystemExit('ഫയല്·공개 ఫార్మాట్_മൂല്യം പേരു് 불일치: ' + str(വഴി))
print('UTF-8 공개 ఫార్మాట్_മൂല്യം·ഫയല് പേരു് പരിശോധിക്കുക 완료; 현지어 검토 상태는 국가판 명명 ഡാറ്റാ റഫറൻസ്')
PY

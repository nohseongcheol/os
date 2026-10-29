#!/bin/sh
set -eu
# 외국어판의 이름을 မြန်မာ 전용 규칙으로 거부하지 않는다.
# အဓိပ္ပာယ်·어원 검토 여부는 native-pending.tsv와 native-term-evidence.json에 기록한다.
python3 - <<'PY'
from pathlib import Path
import re
import unicodedata
for လမ်း in Path('အခြေခံကုဒ်').rglob('*.java'):
    အမည် = လမ်း.stem
    if not အမည်.isidentifier() or unicodedata.normalize('NFC', အမည်) != အမည်:
        raise SystemExit('သတ်မှတ်နံပါတ်တန်ဖိုး 또는 စံပုံစံပြောင်း အမှား: ' + str(လမ်း))
    မူရင်းကုဒ် = လမ်း.read_text(encoding='utf-8')
    ကြေညာချက် = re.search(r'public\s+(?:(?:final|abstract)\s+)?(?:class|interface|enum)\s+([^\s<{]+)', မူရင်းကုဒ်)
    if ကြေညာချက် and ကြေညာချက်.group(1) != အမည်:
        raise SystemExit('ဖိုင်·공개 ပုံစံတန်ဖိုး အမည် 불일치: ' + str(လမ်း))
print('UTF-8 공개 ပုံစံတန်ဖိုး·ဖိုင် အမည် အတည်ပြု ဖြစ်သောအပြည့်အစုံ; 현지어 검토 상태는 국가판 명명 ဒေတာ ကိုးကားချက်')
PY

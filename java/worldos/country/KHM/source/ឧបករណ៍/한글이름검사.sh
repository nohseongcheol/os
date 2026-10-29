#!/bin/sh
set -eu
# 외국어판의 이름을 한국어 전용 규칙으로 거부하지 않는다.
# 뜻·어원 검토 여부는 native-pending.tsv와 native-term-evidence.json에 기록한다.
python3 - <<'PY'
from pathlib import Path
import re
import unicodedata
for ផ្លូវ in Path('តាមច្បាប់_ប្រភព').rglob('*.java'):
    ឈ្មោះ = ផ្លូវ.stem
    if not ឈ្មោះ.isidentifier() or unicodedata.normalize('NFC', ឈ្មោះ) != ឈ្មោះ:
        raise SystemExit('អង្គសម្គាល់_តំលៃ 또는 ធ្វើអោយប្រក្រតី_តំលៃ កំហុស: ' + str(ផ្លូវ))
    ប្រភព = ផ្លូវ.read_text(encoding='utf-8')
    ការប្រកាស = re.search(r'public\s+(?:(?:final|abstract)\s+)?(?:class|interface|enum)\s+([^\s<{]+)', ប្រភព)
    if ការប្រកាស and ការប្រកាស.group(1) != ឈ្មោះ:
        raise SystemExit('ឯកសារ·공개 ទំរង់_តំលៃ ឈ្មោះ 불일치: ' + str(ផ្លូវ))
print('UTF-8 공개 ទំរង់_តំលៃ·ឯកសារ ឈ្មោះ ផ្ទៀងផ្ទាត់ 완료; 현지어 검토 상태는 국가판 명명 ទិន្នន័យ យោង')
PY

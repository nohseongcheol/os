#!/bin/sh
set -eu
# 외국어판의 이름을 한국어 전용 규칙으로 거부하지 않는다.
# 뜻·어원 검토 여부는 native-pending.tsv와 native-term-evidence.json에 기록한다.
python3 - <<'PY'
from pathlib import Path
import re
import unicodedata
for పాత్ in Path('లెగసి_మూలం').rglob('*.java'):
    పేరు = పాత్.stem
    if not పేరు.isidentifier() or unicodedata.normalize('NFC', పేరు) != పేరు:
        raise SystemExit('ఐడెంటిఫయర్_మూల్యం 또는 సాధారణీకరించు_మూల్యం దోషం: ' + str(పాత్))
    వనరు = పాత్.read_text(encoding='utf-8')
    ప్రకటన = re.search(r'public\s+(?:(?:final|abstract)\s+)?(?:class|interface|enum)\s+([^\s<{]+)', వనరు)
    if ప్రకటన and ప్రకటన.group(1) != పేరు:
        raise SystemExit('దస్త్రం·공개 ఆకృతి_మూల్యం పేరు 불일치: ' + str(పాత్))
print('UTF-8 공개 ఆకృతి_మూల్యం·దస్త్రం పేరు సరిచూడు 완료; 현지어 검토 상태는 국가판 명명 డేటా సూచన')
PY

#!/bin/sh
set -eu
# 외국어판의 이름을 Isi_Zulu 전용 규칙으로 거부하지 않는다.
# 뜻·어원 검토 여부는 native-pending.tsv와 native-term-evidence.json에 기록한다.
python3 - <<'PY'
from pathlib import Path
import re
import unicodedata
for Indlela_2 in Path('okumisiwe_umthombo').rglob('*.java'):
    Igama = Indlela_2.stem
    if not Igama.isidentifier() or unicodedata.normalize('NFC', Igama) != Igama:
        raise SystemExit('isivezi_inani 또는 beka_kujwayeleke_inani Iphutha: ' + str(Indlela_2))
    umthombo = Indlela_2.read_text(encoding='utf-8')
    선언 = re.search(r'public\s+(?:(?:final|abstract)\s+)?(?:class|interface|enum)\s+([^\s<{]+)', umthombo)
    if 선언 and 선언.group(1) != Igama:
        raise SystemExit('Ihele·공개 misa_inani Igama 불일치: ' + str(Indlela_2))
print('UTF-8 공개 misa_inani·Ihele Igama qiniseka 완료; 현지어 검토 상태는 국가판 명명 imininingwane Ireferensi')
PY

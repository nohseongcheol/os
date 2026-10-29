#!/bin/sh
set -eu
# 외국어판의 이름을 한국어 전용 규칙으로 거부하지 않는다.
# 뜻·어원 검토 여부는 native-pending.tsv와 native-term-evidence.json에 기록한다.
python3 - <<'PY'
from pathlib import Path
import re
import unicodedata
for ທາງໂຄຈອນ in Path('ດັ້ງເດີມ_ແຫຼ່ງທີ່ມາ').rglob('*.java'):
    ຊື່ = ທາງໂຄຈອນ.stem
    if not ຊື່.isidentifier() or unicodedata.normalize('NFC', ຊື່) != ຊື່:
        raise SystemExit('ຕົວ_ກໍາ_ນົດ_ຄ່າ 또는 ເຮັດ_ເປັນ_ທໍາ_ມະ_ດາ_ຄ່າ ຂໍ້ຜິດພາດ: ' + str(ທາງໂຄຈອນ))
    ແຫຼ່ງທີ່ມາ = ທາງໂຄຈອນ.read_text(encoding='utf-8')
    ການປະກາດ = re.search(r'public\s+(?:(?:final|abstract)\s+)?(?:class|interface|enum)\s+([^\s<{]+)', ແຫຼ່ງທີ່ມາ)
    if ການປະກາດ and ການປະກາດ.group(1) != ຊື່:
        raise SystemExit('ຟາຍ·공개 ຮູບແບບ_ຄ່າ_d1a42ea5 ຊື່ 불일치: ' + str(ທາງໂຄຈອນ))
print('UTF-8 공개 ຮູບແບບ_ຄ່າ_d1a42ea5·ຟາຍ ຊື່ 확인 완료; 현지어 검토 상태는 국가판 명명 ຂໍ້ມູນ ການ_ອ້າງ_ອີງ')
PY

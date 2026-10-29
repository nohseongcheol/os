#!/bin/sh
set -eu
# 외국어판의 이름을 ไทย 전용 규칙으로 거부하지 않는다.
# 뜻·어원 검토 여부는 native-pending.tsv와 native-term-evidence.json에 기록한다.
python3 - <<'PY'
from pathlib import Path
import re
import unicodedata
for เส้นทาง in Path('ดั้งเดิม_แหล่ง').rglob('*.java'):
    ชื่อ = เส้นทาง.stem
    if not ชื่อ.isidentifier() or unicodedata.normalize('NFC', ชื่อ) != ชื่อ:
        raise SystemExit('ตัวระบุ_ค่า 또는 นอร์มัลไลซ์_ค่า ข้อผิดพลาด: ' + str(เส้นทาง))
    รหัสต้นฉบับ = เส้นทาง.read_text(encoding='utf-8')
    การประกาศ = re.search(r'public\s+(?:(?:final|abstract)\s+)?(?:class|interface|enum)\s+([^\s<{]+)', รหัสต้นฉบับ)
    if การประกาศ and การประกาศ.group(1) != ชื่อ:
        raise SystemExit('แฟ้ม·공개 รูปแบบ_ค่า_d1a42ea5 ชื่อ 불일치: ' + str(เส้นทาง))
print('UTF-8 공개 รูปแบบ_ค่า_d1a42ea5·แฟ้ม ชื่อ ยืนยัน 완료; 현지어 검토 상태는 국가판 명명 ข้อมูล อ้างอิง')
PY

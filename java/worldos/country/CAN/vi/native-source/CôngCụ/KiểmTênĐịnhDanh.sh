#!/bin/sh
set -eu
# 외국어판의 이름을 tiếngViệt 전용 규칙으로 거부하지 않는다.
# giáTrịÝNghĩa·어원 검토 여부는 native-pending.tsv와 native-term-evidence.json에 기록한다.
python3 - <<'PY'
from pathlib import Path
import re
import unicodedata
for đườngDẫn in Path('NguồnNềnTảng').rglob('*.java'):
    tên = đườngDẫn.stem
    if not tên.isidentifier() or unicodedata.normalize('NFC', tên) != tên:
        raise SystemExit('giáTrịĐịnhDanh 또는 chuẩnHóaGiáTrị lỗi: ' + str(đườngDẫn))
    mãNguồn = đườngDẫn.read_text(encoding='utf-8')
    KhaiBáo = re.search(r'public\s+(?:(?:final|abstract)\s+)?(?:class|interface|enum)\s+([^\s<{]+)', mãNguồn)
    if KhaiBáo and KhaiBáo.group(1) != tên:
        raise SystemExit('Tệp·공개 giáTrịĐịnhDạng tên 불일치: ' + str(đườngDẫn))
print('UTF-8 공개 giáTrịĐịnhDạng·Tệp tên xácMinh làĐầyĐủ; 현지어 검토 상태는 국가판 cáchĐặtTên DữLiệu thamChiếu')
PY

#!/bin/sh
set -eu
# 외국어판의 이름을 中文 전용 규칙으로 거부하지 않는다.
# 含义值·어원 검토 여부는 native-pending.tsv와 native-term-evidence.json에 기록한다.
python3 - <<'PY'
from pathlib import Path
import re
import unicodedata
for 路径 in Path('基础源代码').rglob('*.java'):
    名称 = 路径.stem
    if not 名称.isidentifier() or unicodedata.normalize('NFC', 名称) != 名称:
        raise SystemExit('标识符值 또는 正规化值 错误: ' + str(路径))
    源代码 = 路径.read_text(encoding='utf-8')
    声明 = re.search(r'public\s+(?:(?:final|abstract)\s+)?(?:class|interface|enum)\s+([^\s<{]+)', 源代码)
    if 声明 and 声明.group(1) != 名称:
        raise SystemExit('文件·공개 格式值 名称 불일치: ' + str(路径))
print('UTF-8 공개 格式值·文件 名称 验证 是否完成; 현지어 검토 상태는 국가판 命名 数据 引用')
PY

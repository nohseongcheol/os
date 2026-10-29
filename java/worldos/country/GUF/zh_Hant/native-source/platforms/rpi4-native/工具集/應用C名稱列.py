#!/usr/bin/env python3
"""聲明 고유번호와 UTF-8 位元組值 위치로 內建 C 이름을 옮기는 일회성 이행 工具集.

外部值 구조체의 멤버, 字符串, C 표준 函數, 移植 규약은 보존한다.
입력은 更改值 之前值 소스에 대한 分析C名稱列.py 결과여야 한다.
"""
import json
import re
from collections import defaultdict
from pathlib import Path

項目根 = Path(__file__).resolve().parents[1]

def 執行命令():
    分析值 = json.loads((項目根/'build/한국어화/시언어분석.json').read_text())
    if 分析值['錯誤']: raise SystemExit('分析值 오류를 먼저 해결해야 합니다.')
    名稱表 = json.loads((項目根/'命名/C名稱列.json').read_text())
    標準定義 = set(json.loads((項目根/'命名/標準名稱列.json').read_text()))
    聲明表 = 分析值['聲明']
    聲明目標側替換 = {唯一值:名稱表[條目值['名稱']] for 唯一值,條目值 in 聲明表.items()
                if 條目值['名稱'] in 名稱表 and 條目值['名稱'] not in 標準定義}
    連接狀態表 = {條目值['名稱']:名稱表[條目值['名稱']] for 條目值 in 聲明表.values()
              if 條目值.get('連接')==4 and 條目值['種類值'] in (8,9)
              and 條目值['名稱'] in 名稱表 and 條目值['名稱'] not in 標準定義}
    # 生成 AOT C·어셈블리·공개 SDK가 공유하는 바이너리 連接 이름만 유지한다.
    頭值 = ['/* 中文 原始碼樹 이름과 기존 計算機 連接 契約值. 자동 生成: 命名/C名稱列.json */',
           '#ifndef 原生計算機連接名稱列標頭', '#define 原生計算機連接名稱列標頭']
    頭值 += ['#define '+新建名稱+' '+舊名稱 for 舊名稱,新建名稱 in sorted(連接狀態表.items())]
    頭值 += ['#endif','']
    (項目根/'命名/計算機連接名稱列.h').write_text('\n'.join(頭值))
    更改列列表 = defaultdict(dict)
    for 檔案,偏移值,名稱,唯一值 in 分析值['引用']:
        if 唯一值 in 聲明目標側替換:
            更改列列表[檔案][偏移值] = (名稱,聲明目標側替換[唯一值])
    日誌記錄 = ['檔案\t원래바이트위치\t이전이름\t한국어이름']
    忽略值 = []
    for 檔案,更改值 in 更改列列表.items():
        路徑 = Path(檔案); 原始 = 路徑.read_bytes(); 資料 = 原始
        for 偏移值,(舊名稱,新建名稱) in sorted(更改值.items(),reverse=True):
            結尾 = 偏移值+len(舊名稱.encode())
            if 原始[偏移值:結尾] != 舊名稱.encode():
                忽略值.append((str(路徑.relative_to(項目根)),偏移值,舊名稱));continue
            資料 = 資料[:偏移值]+新建名稱.encode()+資料[結尾:]
            日誌記錄.append('{}\t{}\t{}\t{}'.format(路徑.relative_to(項目根),偏移值,舊名稱,新建名稱))
        路徑.write_bytes(資料)
    # 預處理原始碼 매개변수는 AST의 선언으로 나타나지 않는다. 預處理原始碼 줄만 보완한다.
    詞法用機器字 = re.compile(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/|\b[A-Za-z_]\w*\b')
    宏值 = {條目值['名稱']:名稱表[條目值['名稱']] for 條目值 in 聲明表.values()
              if 條目值['種類值']==501 and 條目值['名稱'] in 名稱表 and 條目值['名稱'] not in 標準定義}
    for 路徑 in sorted({Path(條目值['檔案']) for 條目值 in 聲明表.values()}):
        多行內容 = 路徑.read_text().splitlines(True); 是否繼續狀態 = False
        for 編號,行 in enumerate(多行內容):
            預處理原始碼 = 是否繼續狀態 or bool(re.match(r'\s*#',行))
            是否繼續狀態 = 預處理原始碼 and 行.rstrip().endswith('\\')
            if 預處理原始碼:
                表 = 名稱表 if re.match(r'\s*#\s*define\b',行) or 是否繼續狀態 else 宏值
                多行內容[編號] = 詞法用機器字.sub(lambda 是否已匹配: 表.get(是否已匹配[0],是否已匹配[0]) if 是否已匹配[0] not in 標準定義 else 是否已匹配[0],行)
        路徑.write_text(''.join(多行內容))
    # 각 內建 翻譯原始碼 단위에만 연결표를 넣는다. 外部值 배포본에는 전파하지 않는다.
    for 路徑 in sorted({Path(條目值['檔案']) for 條目值 in 聲明表.values()}):
        if 路徑.suffix not in ('.c','.cpp'):continue
        對端值 = '../' * len(路徑.relative_to(項目根).parts[:-1]) + '命名/計算機連接名稱列.h'
        路徑.write_text('#include "'+對端值+'"\n'+路徑.read_text())
    (項目根/'命名/C名稱映射.tsv').write_text('\n'.join(日誌記錄)+'\n')
    (項目根/'build/한국어화/전처리참조.json').write_text(json.dumps(忽略值,ensure_ascii=False,indent=2)+'\n')
    print('更改值',len(日誌記錄)-1,'預處理原始碼 재검토',len(忽略值),'計算機 連接',len(連接狀態表))

if __name__=='__main__': 執行命令()

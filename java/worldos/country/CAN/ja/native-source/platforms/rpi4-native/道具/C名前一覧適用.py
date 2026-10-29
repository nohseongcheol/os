#!/usr/bin/env python3
"""宣言 고유번호와 UTF-8 バイト値 위치로 内蔵 C 이름을 옮기는 일회성 이행 道具.

外部値 구조체의 멤버, 文字列, C 표준 関数, 移植 규약은 보존한다.
입력은 値変更 直前側値 소스에 대한 C名前一覧分析.py 결과여야 한다.
"""
import json
import re
from collections import defaultdict
from pathlib import Path

計画根 = Path(__file__).resolve().parents[1]

def 命令実行():
    値分析 = json.loads((計画根/'build/한국어화/시언어분석.json').read_text())
    if 値分析['エラー']: raise SystemExit('値分析 오류를 먼저 해결해야 합니다.')
    名前表 = json.loads((計画根/'命名/C名前一覧.json').read_text())
    標準定義 = set(json.loads((計画根/'命名/標準名前一覧.json').read_text()))
    宣言表 = 値分析['宣言']
    宣言到達先置換 = {一意値:名前表[入口値['名前']] for 一意値,入口値 in 宣言表.items()
                if 入口値['名前'] in 名前表 and 入口値['名前'] not in 標準定義}
    接続状態表 = {入口値['名前']:名前表[入口値['名前']] for 入口値 in 宣言表.values()
              if 入口値.get('接続')==4 and 入口値['種別値'] in (8,9)
              and 入口値['名前'] in 名前表 and 入口値['名前'] not in 標準定義}
    # 生成 AOT C·어셈블리·공개 SDK가 공유하는 바이너리 接続 이름만 유지한다.
    先頭部値 = ['/* 日本語 ソース木 이름과 기존 機械 接続 契約値. 자동 生成: 命名/C名前一覧.json */',
           '#ifndef 自前機械連結名前一覧ヘッダー', '#define 自前機械連結名前一覧ヘッダー']
    先頭部値 += ['#define '+新規名前+' '+旧名前 for 旧名前,新規名前 in sorted(接続状態表.items())]
    先頭部値 += ['#endif','']
    (計画根/'命名/機械連結名前一覧.h').write_text('\n'.join(先頭部値))
    変更群一覧 = defaultdict(dict)
    for ファイル,変位量値,名前,一意値 in 値分析['参照']:
        if 一意値 in 宣言到達先置換:
            変更群一覧[ファイル][変位量値] = (名前,宣言到達先置換[一意値])
    履歴記録記録 = ['ファイル\t원래바이트위치\t이전이름\t한국어이름']
    値無視 = []
    for ファイル,値変更 in 変更群一覧.items():
        経路 = Path(ファイル); 原本 = 経路.read_bytes(); データ = 原本
        for 変位量値,(旧名前,新規名前) in sorted(値変更.items(),reverse=True):
            終端 = 変位量値+len(旧名前.encode())
            if 原本[変位量値:終端] != 旧名前.encode():
                値無視.append((str(経路.relative_to(計画根)),変位量値,旧名前));continue
            データ = データ[:変位量値]+新規名前.encode()+データ[終端:]
            履歴記録記録.append('{}\t{}\t{}\t{}'.format(経路.relative_to(計画根),変位量値,旧名前,新規名前))
        経路.write_bytes(データ)
    # 前処理ソース 매개변수는 AST의 선언으로 나타나지 않는다. 前処理ソース 줄만 보완한다.
    字句用語 = re.compile(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/|\b[A-Za-z_]\w*\b')
    マクロ値 = {入口値['名前']:名前表[入口値['名前']] for 入口値 in 宣言表.values()
              if 入口値['種別値']==501 and 入口値['名前'] in 名前表 and 入口値['名前'] not in 標準定義}
    for 経路 in sorted({Path(入口値['ファイル']) for 入口値 in 宣言表.values()}):
        行一覧 = 経路.read_text().splitlines(True); 判定継続状態 = False
        for 番号,行 in enumerate(行一覧):
            前処理ソース = 判定継続状態 or bool(re.match(r'\s*#',行))
            判定継続状態 = 前処理ソース and 行.rstrip().endswith('\\')
            if 前処理ソース:
                表 = 名前表 if re.match(r'\s*#\s*define\b',行) or 判定継続状態 else マクロ値
                行一覧[番号] = 字句用語.sub(lambda 判定照合済み: 表.get(判定照合済み[0],判定照合済み[0]) if 判定照合済み[0] not in 標準定義 else 判定照合済み[0],行)
        経路.write_text(''.join(行一覧))
    # 각 内蔵 ソース翻訳処理 단위에만 연결표를 넣는다. 外部値 배포본에는 전파하지 않는다.
    for 経路 in sorted({Path(入口値['ファイル']) for 入口値 in 宣言表.values()}):
        if 経路.suffix not in ('.c','.cpp'):continue
        通信相手値 = '../' * len(経路.relative_to(計画根).parts[:-1]) + '命名/機械連結名前一覧.h'
        経路.write_text('#include "'+通信相手値+'"\n'+経路.read_text())
    (計画根/'命名/C名前対応付け.tsv').write_text('\n'.join(履歴記録記録)+'\n')
    (計画根/'build/한국어화/전처리참조.json').write_text(json.dumps(値無視,ensure_ascii=False,indent=2)+'\n')
    print('値変更',len(履歴記録記録)-1,'前処理ソース 재검토',len(値無視),'機械 接続',len(接続状態表))

if __name__=='__main__': 命令実行()

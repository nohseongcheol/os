#!/usr/bin/env python3
"""命名 切抜き·例外·경로를 검사한다. --시언어는 libclang 宣言 분석도 수행한다."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess

計画根 = Path(__file__).resolve().parents[1]
保管庫根 = 計画根.parents[1]

def 起動処理():
    構文解析器 = argparse.ArgumentParser(description=__doc__)
    構文解析器.add_argument('--C言語', action='store_true')
    引数 = 構文解析器.parse_args()
    失敗一覧 = []
    契約値 = {'_', '__init__', '__enter__', '__exit__', 'setUp', 'handle'}
    ファイル個数 = 0
    仮引数表 = {}
    可変引数関数 = set()
    AST節点一覧 = {}
    共有コンパイラ群 = [保管庫根/'compiler/コンパイラ.py', 保管庫根/'compiler/事前用時間コンパイラ.py']
    for 経路 in list((計画根/'道具').glob('*.py')) + list((計画根/'用例').rglob('*.py')) + 共有コンパイラ群:
        if 経路.name.endswith(('이름반영.py', '이름분석.py')): continue
        ファイル個数 += 1
        AST節点 = ast.parse(経路.read_text()); AST節点一覧[経路] = AST節点
        for 入口値 in ast.walk(AST節点):
            if isinstance(入口値, ast.FunctionDef):
                仮引数表.setdefault(入口値.name, set()).update(仮引数引数.arg for 仮引数引数 in 入口値.args.args + 入口値.args.kwonlyargs)
                if 入口値.args.kwarg: 可変引数関数.add(入口値.name)
            if isinstance(入口値, ast.ClassDef):
                for 関数 in 入口値.body:
                    if isinstance(関数, ast.FunctionDef) and 関数.name == '__init__':
                        仮引数表.setdefault(入口値.name, set()).update(仮引数引数.arg for 仮引数引数 in 関数.args.args + 関数.args.kwonlyargs)
            名前 = ''
            if isinstance(入口値, (ast.FunctionDef, ast.ClassDef)): 名前 = 入口値.name
            elif isinstance(入口値, ast.Name) and isinstance(入口値.ctx, ast.Store): 名前 = 入口値.id
            elif isinstance(入口値, ast.arg): 名前 = 入口値.arg
            if 名前 and 名前 not in 契約値 and all(ord(文字値)<128 for 文字値 in 名前):
                失敗一覧.append('{}:{}: {}'.format(経路.relative_to(保管庫根), 入口値.lineno, 名前))
    for 経路, AST節点 in AST節点一覧.items():
        for 呼出 in ast.walk(AST節点):
            if not isinstance(呼出, ast.Call): continue
            名前 = 呼出.func.id if isinstance(呼出.func, ast.Name) else 呼出.func.attr if isinstance(呼出.func, ast.Attribute) else ''
            if 名前 not in 仮引数表 or 名前 in 可変引数関数 or not any(ord(文字値)>127 for 文字値 in 名前): continue
            for 仮引数引数 in 呼出.keywords:
                if 仮引数引数.arg and 仮引数引数.arg not in 仮引数表[名前]:
                    失敗一覧.append('{}:{}: {}의 매개변수 {}'.format(経路.relative_to(保管庫根), 呼出.lineno, 名前, 仮引数引数.arg))
    for 行 in (計画根/'命名/ファイル名前対応付け.tsv').read_text().splitlines()[1:]:
        前回項目, 現在項目, プロセス値入口 = 行.split('\t')
        if not (計画根/現在項目).is_file(): 失敗一覧.append('移動値 ファイル 未存在メソッド: '+現在項目)
        if プロセス値入口 == '호환진입점유지' and not (計画根/前回項目).is_file(): 失敗一覧.append('호환 入口点 未存在メソッド: '+前回項目)
    用例 = (計画根.parents[1]/'example/java/通信例.java').read_text()
    for 禁止呼出し一覧 in ('java.net.', '.getOutputStream(', '.getInputStream(', '.write(', '.read(', '.close('):
        if 禁止呼出し一覧 in 用例: 失敗一覧.append('네트워크 예제에 남은 표준 직접 呼出: '+禁止呼出し一覧)
    # 사용자가 읽는 Java 예제는 予約済み語一覧/리터럴을 제외한 식별자도 全体構築 한국어다.
    予約済み語一覧 = set('abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null'.split())
    for 経路 in sorted((計画根.parents[1]/'example/java').glob('*.java')):
        ソース = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', 経路.read_text())
        for 名前 in re.findall(r'\b[^\W\d]\w*\b', ソース, re.UNICODE):
            if 名前 not in 予約済み語一覧 and all(ord(文字値)<128 for 文字値 in 名前):
                失敗一覧.append('{}: 예제의 영어 識別子値 {}'.format(経路.name, 名前))
    for 名前 in ('窓', 'ボタン', 'ラベル', '本文フィールド', '画面要素', 'イベント待ち行列', '作業担当', '実行可能処理作業', '動作受信先', '動作通知', '作業'):
        ソース = (計画根/'日本語Java/日本語/内蔵'/(名前+'.java')).read_text()
        ソース = re.sub(r'//[^\n]*|/\*[\s\S]*?\*/', '', ソース)
        if re.search(r'\b(?:Runnable|Thread|JButton|SwingUtilities|ActionListener|ActionEvent)\b|javax\.swing|java\.awt', ソース):
            失敗一覧.append(名前+': 日本語 직접 구현에 표준 オブジェクト値 래퍼가 남았습니다.')
    C例 = (計画根.parents[1]/'example/c/通信例.c').read_text()
    for 名前 in ('AF_INET', 'SOCK_DGRAM', 'IPPROTO_UDP', 'pk_sockaddr', 'sin_family', 'sin_port', 'sin_addr', 's_addr'):
        if 名前 in C例: 失敗一覧.append('C 通信 예제에 남은 표준 名前: '+名前)
    Python例 = (計画根.parents[1]/'example/python/通信例.py').read_text()
    if 'OSError' in Python例 or '.args' in Python例: 失敗一覧.append('Python 通信 예제에 남은 표준 例外 직접 使用値')
    先頭部値 = (計画根.parents[1]/'posix-kor/arm64-native/ヘッダー/通信網ABI.h').read_text()
    for 名前 in ('インターネット体系', 'データグラムソケット', 'データグラム通信規約', 'ソケット番地', 'インターネットソケット番地', '通信端点作成', 'データグラムデータ送信'):
        if re.search(r'^#define\s+'+名前+r'\b', 先頭部値, re.M): 失敗一覧.append('C 직접 実装 대신 マクロ値 使用値: '+名前)
    Javaファイル個数 = 0
    for 根値 in ('ソース', '利用者/Java', '日本語Java'):
        for 経路 in (計画根/根値).rglob('*.java'):
            Javaファイル個数 += 1
            ソース = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', 経路.read_text())
            for 判定照合済み in re.finditer(r'\b(?:int|long|boolean|byte|char|short|String)(?:\s*\[\s*\])*\s+([A-Za-z_$][A-Za-z_$0-9]*)\b', ソース):
                失敗一覧.append('{}: 한국어화되지 않은 宣言 {}'.format(経路.relative_to(計画根), 判定照合済み[1]))
            if 根値 == '日本語Java' and re.search(r'\bthrows\s+[A-Za-z]', ソース):
                失敗一覧.append('{}: 공개 例外 宣言'.format(経路.relative_to(計画根)))
    x86Javaファイル数 = 0
    標準Java名前一覧 = {'String', 'length', 'charAt'}
    for 経路 in sorted((保管庫根/'os/ソース').glob('*.java')):
        x86Javaファイル数 += 1
        ソース = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', 経路.read_text())
        for 名前 in re.findall(r'\b[^\W\d]\w*\b', ソース, re.UNICODE):
            if 名前 not in 予約済み語一覧 | 標準Java名前一覧 and all(ord(文字値)<128 for 文字値 in 名前):
                失敗一覧.append('{}: 内蔵 영어 識別子値 {}'.format(経路.relative_to(保管庫根), 名前))
    履歴記録記録 = {'passed': False, 'python_files': ファイル個数, 'java_files': Javaファイル個数,
          'x86_java_files': x86Javaファイル数, 'host_compiler_python_files': len(共有コンパイラ群), 'c_semantic_checked': False,
          'java_examples_korean_identifiers': True, 'direct_korean_gui_thread_without_standard_wrappers': True}
    if 引数.C言語:
        subprocess.check_call(['python3', str(計画根/'道具/C名前一覧分析.py')])
        値分析 = json.loads((計画根/'build/한국어화/시언어분석.json').read_text())
        失敗一覧.extend(str(エラー) for エラー in 値分析['エラー'])
        公開ABI = set(json.loads((計画根/'命名/標準名前一覧.json').read_text()))
        for 入口値 in 値分析['宣言'].values():
            名前 = 入口値['名前']; 経路 = Path(入口値['ファイル'])
            ソース = 経路.read_bytes()
            # 日本語 소스가 공개 ABI 매크로를 거쳐 영어 심볼이 된 경우는 허용한다.
            if ソース[入口値['変位量値']:入口値['変位量値']+len(名前)] == 名前.encode() and 名前 not in 公開ABI:
                失敗一覧.append('{}:{}: {}'.format(経路.relative_to(計画根), 入口値['行'], 名前))
        履歴記録記録['c_semantic_checked'] = True
        履歴記録記録['c_source_sha256'] = {str(Path(ファイル).relative_to(計画根)):ハッシュファイル for ファイル,ハッシュファイル in 値分析['원문해시'].items()}
    履歴記録記録['passed'] = not 失敗一覧; 履歴記録記録['failures'] = 失敗一覧
    宛先値 = 計画根/'build/verification/naming'; 宛先値.mkdir(parents=True, exist_ok=True)
    (宛先値/'report.json').write_text(json.dumps(履歴記録記録, ensure_ascii=False, indent=2)+'\n')
    if 失敗一覧: raise SystemExit('\n'.join(失敗一覧))
    print('PASS: 日本語 宣言·ファイル 経路·호환 入口点·通信 用例')

if __name__ == '__main__': 起動処理()

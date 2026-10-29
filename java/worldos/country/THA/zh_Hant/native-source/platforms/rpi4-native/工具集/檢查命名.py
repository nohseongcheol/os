#!/usr/bin/env python3
"""命名 裁剪·異常·경로를 검사한다. --시언어는 libclang 聲明 분석도 수행한다."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess

項目根 = Path(__file__).resolve().parents[1]
代碼庫根 = 項目根.parents[1]

def 運行():
    解析器 = argparse.ArgumentParser(description=__doc__)
    解析器.add_argument('--C語言', action='store_true')
    實參 = 解析器.parse_args()
    失敗列 = []
    契約值 = {'_', '__init__', '__enter__', '__exit__', 'setUp', 'handle'}
    檔案個數 = 0
    形式參數表 = {}
    可變參數函數 = set()
    AST節點列 = {}
    共享編譯器集 = [代碼庫根/'compiler/編譯器.py', 代碼庫根/'compiler/提前所屬時間編譯器.py']
    for 路徑 in list((項目根/'工具集').glob('*.py')) + list((項目根/'範例').rglob('*.py')) + 共享編譯器集:
        if 路徑.name.endswith(('이름반영.py', '이름분석.py')): continue
        檔案個數 += 1
        AST節點 = ast.parse(路徑.read_text()); AST節點列[路徑] = AST節點
        for 條目值 in ast.walk(AST節點):
            if isinstance(條目值, ast.FunctionDef):
                形式參數表.setdefault(條目值.name, set()).update(形式參數實際參數.arg for 形式參數實際參數 in 條目值.args.args + 條目值.args.kwonlyargs)
                if 條目值.args.kwarg: 可變參數函數.add(條目值.name)
            if isinstance(條目值, ast.ClassDef):
                for 函數 in 條目值.body:
                    if isinstance(函數, ast.FunctionDef) and 函數.name == '__init__':
                        形式參數表.setdefault(條目值.name, set()).update(形式參數實際參數.arg for 形式參數實際參數 in 函數.args.args + 函數.args.kwonlyargs)
            名稱 = ''
            if isinstance(條目值, (ast.FunctionDef, ast.ClassDef)): 名稱 = 條目值.name
            elif isinstance(條目值, ast.Name) and isinstance(條目值.ctx, ast.Store): 名稱 = 條目值.id
            elif isinstance(條目值, ast.arg): 名稱 = 條目值.arg
            if 名稱 and 名稱 not in 契約值 and all(ord(字元值)<128 for 字元值 in 名稱):
                失敗列.append('{}:{}: {}'.format(路徑.relative_to(代碼庫根), 條目值.lineno, 名稱))
    for 路徑, AST節點 in AST節點列.items():
        for 調用 in ast.walk(AST節點):
            if not isinstance(調用, ast.Call): continue
            名稱 = 調用.func.id if isinstance(調用.func, ast.Name) else 調用.func.attr if isinstance(調用.func, ast.Attribute) else ''
            if 名稱 not in 形式參數表 or 名稱 in 可變參數函數 or not any(ord(字元值)>127 for 字元值 in 名稱): continue
            for 形式參數實際參數 in 調用.keywords:
                if 形式參數實際參數.arg and 形式參數實際參數.arg not in 形式參數表[名稱]:
                    失敗列.append('{}:{}: {}의 매개변수 {}'.format(路徑.relative_to(代碼庫根), 調用.lineno, 名稱, 形式參數實際參數.arg))
    for 行 in (項目根/'命名/檔案名稱映射.tsv').read_text().splitlines()[1:]:
        上一個項目, 當前項目, 程序值條目 = 行.split('\t')
        if not (項目根/當前項目).is_file(): 失敗列.append('移動值 檔案 缺失方法: '+當前項目)
        if 程序值條目 == '호환진입점유지' and not (項目根/上一個項目).is_file(): 失敗列.append('호환 條目分 缺失方法: '+上一個項目)
    範例 = (項目根.parents[1]/'example/java/網路例.java').read_text()
    for 禁止調用列 in ('java.net.', '.getOutputStream(', '.getInputStream(', '.write(', '.read(', '.close('):
        if 禁止調用列 in 範例: 失敗列.append('네트워크 예제에 남은 표준 직접 調用: '+禁止調用列)
    # 사용자가 읽는 Java 예제는 已保留位單詞列/리터럴을 제외한 식별자도 構建全部 한국어다.
    已保留位單詞列 = set('abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null'.split())
    for 路徑 in sorted((項目根.parents[1]/'example/java').glob('*.java')):
        原始碼 = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', 路徑.read_text())
        for 名稱 in re.findall(r'\b[^\W\d]\w*\b', 原始碼, re.UNICODE):
            if 名稱 not in 已保留位單詞列 and all(ord(字元值)<128 for 字元值 in 名稱):
                失敗列.append('{}: 예제의 영어 標識符值 {}'.format(路徑.name, 名稱))
    for 名稱 in ('窗口', '按鈕', '標籤', '文本字段', '屏幕元素', '事件排隊', '後臺任務', '可運行任務任務', '動作接收者', '動作通知', '任務'):
        原始碼 = (項目根/'中文Java/中文/內建'/(名稱+'.java')).read_text()
        原始碼 = re.sub(r'//[^\n]*|/\*[\s\S]*?\*/', '', 原始碼)
        if re.search(r'\b(?:Runnable|Thread|JButton|SwingUtilities|ActionListener|ActionEvent)\b|javax\.swing|java\.awt', 原始碼):
            失敗列.append(名稱+': 中文 직접 구현에 표준 物件值 래퍼가 남았습니다.')
    C範例 = (項目根.parents[1]/'example/c/網路例.c').read_text()
    for 名稱 in ('AF_INET', 'SOCK_DGRAM', 'IPPROTO_UDP', 'pk_sockaddr', 'sin_family', 'sin_port', 'sin_addr', 's_addr'):
        if 名稱 in C範例: 失敗列.append('C 通信 예제에 남은 표준 名稱: '+名稱)
    Python範例 = (項目根.parents[1]/'example/python/網路例.py').read_text()
    if 'OSError' in Python範例 or '.args' in Python範例: 失敗列.append('Python 通信 예제에 남은 표준 異常 직접 使用值')
    頭值 = (項目根.parents[1]/'posix-kor/arm64-native/頭文件/網路ABI.h').read_text()
    for 名稱 in ('互聯網族', '數據報通訊端', '數據報通訊協定', '通訊端地址', '互聯網通訊端地址', '創建端點', '發送數據報資料'):
        if re.search(r'^#define\s+'+名稱+r'\b', 頭值, re.M): 失敗列.append('C 직접 實現 대신 宏值 使用值: '+名稱)
    Java檔案個數 = 0
    for 根值 in ('原始碼', '使用者/Java', '中文Java'):
        for 路徑 in (項目根/根值).rglob('*.java'):
            Java檔案個數 += 1
            原始碼 = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', 路徑.read_text())
            for 是否已匹配 in re.finditer(r'\b(?:int|long|boolean|byte|char|short|String)(?:\s*\[\s*\])*\s+([A-Za-z_$][A-Za-z_$0-9]*)\b', 原始碼):
                失敗列.append('{}: 한국어화되지 않은 聲明 {}'.format(路徑.relative_to(項目根), 是否已匹配[1]))
            if 根值 == '中文Java' and re.search(r'\bthrows\s+[A-Za-z]', 原始碼):
                失敗列.append('{}: 공개 異常 聲明'.format(路徑.relative_to(項目根)))
    x86Java檔案數 = 0
    標準Java名稱列 = {'String', 'length', 'charAt'}
    for 路徑 in sorted((代碼庫根/'os/原始碼').glob('*.java')):
        x86Java檔案數 += 1
        原始碼 = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', 路徑.read_text())
        for 名稱 in re.findall(r'\b[^\W\d]\w*\b', 原始碼, re.UNICODE):
            if 名稱 not in 已保留位單詞列 | 標準Java名稱列 and all(ord(字元值)<128 for 字元值 in 名稱):
                失敗列.append('{}: 內建 영어 標識符值 {}'.format(路徑.relative_to(代碼庫根), 名稱))
    日誌記錄 = {'passed': False, 'python_files': 檔案個數, 'java_files': Java檔案個數,
          'x86_java_files': x86Java檔案數, 'host_compiler_python_files': len(共享編譯器集), 'c_semantic_checked': False,
          'java_examples_korean_identifiers': True, 'direct_korean_gui_thread_without_standard_wrappers': True}
    if 實參.C語言:
        subprocess.check_call(['python3', str(項目根/'工具集/分析C名稱列.py')])
        分析值 = json.loads((項目根/'build/한국어화/시언어분석.json').read_text())
        失敗列.extend(str(錯誤) for 錯誤 in 分析值['錯誤'])
        導出ABI = set(json.loads((項目根/'命名/標準名稱列.json').read_text()))
        for 條目值 in 分析值['聲明'].values():
            名稱 = 條目值['名稱']; 路徑 = Path(條目值['檔案'])
            原始碼 = 路徑.read_bytes()
            # 中文 소스가 공개 ABI 매크로를 거쳐 영어 심볼이 된 경우는 허용한다.
            if 原始碼[條目值['偏移值']:條目值['偏移值']+len(名稱)] == 名稱.encode() and 名稱 not in 導出ABI:
                失敗列.append('{}:{}: {}'.format(路徑.relative_to(項目根), 條目值['行'], 名稱))
        日誌記錄['c_semantic_checked'] = True
        日誌記錄['c_source_sha256'] = {str(Path(檔案).relative_to(項目根)):哈希檔案 for 檔案,哈希檔案 in 分析值['원문해시'].items()}
    日誌記錄['passed'] = not 失敗列; 日誌記錄['failures'] = 失敗列
    目的地址值 = 項目根/'build/verification/naming'; 目的地址值.mkdir(parents=True, exist_ok=True)
    (目的地址值/'report.json').write_text(json.dumps(日誌記錄, ensure_ascii=False, indent=2)+'\n')
    if 失敗列: raise SystemExit('\n'.join(失敗列))
    print('PASS: 中文 聲明·檔案 路徑·호환 條目分·通信 範例')

if __name__ == '__main__': 運行()

#!/usr/bin/env python3
"""システム構築 변환이 日本語 文字列, 주석, 헤더 경로를 바꾸지 않는지 검사한다."""
from 識別子変換結果 import 値変換

ソース = '''#include <ファイルABI.h>
#include "通信網ABI.h"
// ファイル開放 라는 주석
/* 자료이름 */
const char *ファイル入口名前 = "한글 \\" 文字列";
char 文字値 = '先頭位置被演算子';
int 파일열기_횟수 = 1;
'''
出力 = 値変換(ソース)
assert '#include <ファイルABI.h>' in 出力
assert '#include "通信網ABI.h"' in 出力
assert '// ファイル開放 라는 주석' in 出力
assert '/* 자료이름 */' in 出力
assert '"한글 \\" 文字列"' in 出力
assert "'先頭位置被演算子'" in 出力
assert '\\ud30c\\uc77c\\uc774\\ub984' in 出力
assert '파일열기_횟수' not in 出力
assert 値変換(出力) == 出力
print('PASS: 日本語 識別子値 値変換/文字列·주석·経路 보존')

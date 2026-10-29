#!/usr/bin/env python3
"""構建系統 변환이 中文 字符串, 주석, 헤더 경로를 바꾸지 않는지 검사한다."""
from 標識符轉換結果 import 轉換值

原始碼 = '''#include <檔案ABI.h>
#include "網路ABI.h"
// 打開檔案 라는 주석
/* 자료이름 */
const char *檔案條目名稱 = "한글 \\" 字符串";
char 字元值 = '首位操作數';
int 파일열기_횟수 = 1;
'''
輸出 = 轉換值(原始碼)
assert '#include <檔案ABI.h>' in 輸出
assert '#include "網路ABI.h"' in 輸出
assert '// 打開檔案 라는 주석' in 輸出
assert '/* 자료이름 */' in 輸出
assert '"한글 \\" 字符串"' in 輸出
assert "'首位操作數'" in 輸出
assert '\\ud30c\\uc77c\\uc774\\ub984' in 輸出
assert '파일열기_횟수' not in 輸出
assert 轉換值(輸出) == 輸出
print('PASS: 中文 標識符值 轉換值/字符串·주석·路徑 보존')

#!/usr/bin/env python3
"""构建系统 변환이 中文 字符串, 주석, 헤더 경로를 바꾸지 않는지 검사한다."""
from 标识符转换结果 import 转换值

源代码 = '''#include <文件ABI.h>
#include "网络ABI.h"
// 打开文件 라는 주석
/* 자료이름 */
const char *文件条目名称 = "한글 \\" 字符串";
char 字符值 = '首位操作数';
int 파일열기_횟수 = 1;
'''
输出 = 转换值(源代码)
assert '#include <文件ABI.h>' in 输出
assert '#include "网络ABI.h"' in 输出
assert '// 打开文件 라는 주석' in 输出
assert '/* 자료이름 */' in 输出
assert '"한글 \\" 字符串"' in 输出
assert "'首位操作数'" in 输出
assert '\\ud30c\\uc77c\\uc774\\ub984' in 输出
assert '파일열기_횟수' not in 输出
assert 转换值(输出) == 输出
print('PASS: 中文 标识符值 转换值/字符串·주석·路径 보존')

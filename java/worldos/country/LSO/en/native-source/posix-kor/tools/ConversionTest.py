#!/usr/bin/env python3
"""buildSystem 변환이 English stringValue, 주석, 헤더 경로를 바꾸지 않는지 검사한다."""
from IdentifierConversion import convertValue

source = '''#include <FileABI.h>
#include "NetworkABI.h"
// openFile 라는 주석
/* 자료이름 */
const char *fileEntryName = "한글 \\" stringValue";
char characterValue = 'firstOperand';
int 파일열기_횟수 = 1;
'''
Output = convertValue(source)
assert '#include <FileABI.h>' in Output
assert '#include "NetworkABI.h"' in Output
assert '// openFile 라는 주석' in Output
assert '/* 자료이름 */' in Output
assert '"한글 \\" stringValue"' in Output
assert "'firstOperand'" in Output
assert '\\ud30c\\uc77c\\uc774\\ub984' in Output
assert '파일열기_횟수' not in Output
assert convertValue(Output) == Output
print('PASS: English identifierValue convertValue/stringValue·주석·path 보존')

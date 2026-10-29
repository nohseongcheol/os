#!/usr/bin/env python3
"""bangun 변환이 Indonesia string_VALUE, 주석, 헤더 경로를 바꾸지 않는지 검사한다."""
from pengidentifikasi_konversi import CONVERT_VALUE

kodeSumber = '''#include <파일규약.h>
#include "통신규약.h"
// buat_file 라는 주석
/* 자료이름 */
const char *file_entri_nama = "한글 \\" string_VALUE";
char karakter_VALUE = '가';
int 파일열기_횟수 = 1;
'''
keluaranTeks = CONVERT_VALUE(kodeSumber)
assert '#include <파일규약.h>' in keluaranTeks
assert '#include "통신규약.h"' in keluaranTeks
assert '// buat_file 라는 주석' in keluaranTeks
assert '/* 자료이름 */' in keluaranTeks
assert '"한글 \\" string_VALUE"' in keluaranTeks
assert "'가'" in keluaranTeks
assert '\\ud30c\\uc77c\\uc774\\ub984' in keluaranTeks
assert '파일열기_횟수' not in keluaranTeks
assert CONVERT_VALUE(keluaranTeks) == keluaranTeks
print('PASS: Indonesia pengidentifikasi_VALUE CONVERT_VALUE/string_VALUE·주석·jalur 보존')

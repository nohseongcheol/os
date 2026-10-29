#!/usr/bin/env python3
"""ສ້າງ_ລະບົບ 변환이 한국어 ສະຕຣິງ_ຄ່າ, 주석, 헤더 경로를 바꾸지 않는지 검사한다."""
from 식별자변환 import 변환

ແຫຼ່ງທີ່ມາ = '''#include <파일규약.h>
#include "통신규약.h"
// ສ້າງ_ຟາຍ 라는 주석
/* 자료이름 */
const char *ຟາຍ_ເຂົ້າໃນ_ຊື່ = "한글 \\" ສະຕຣິງ_ຄ່າ";
char ຕົວອັກສອນ_ຄ່າ = '가';
int 파일열기_횟수 = 1;
'''
출력 = 변환(ແຫຼ່ງທີ່ມາ)
assert '#include <파일규약.h>' in 출력
assert '#include "통신규약.h"' in 출력
assert '// ສ້າງ_ຟາຍ 라는 주석' in 출력
assert '/* 자료이름 */' in 출력
assert '"한글 \\" ສະຕຣິງ_ຄ່າ"' in 출력
assert "'가'" in 출력
assert '\\ud30c\\uc77c\\uc774\\ub984' in 출력
assert '파일열기_횟수' not in 출력
assert 변환(출력) == 출력
print('PASS: 한국어 ຕົວ_ກໍາ_ນົດ_ຄ່າ 변환/ສະຕຣິງ_ຄ່າ·주석·ທາງໂຄຈອນ 보존')

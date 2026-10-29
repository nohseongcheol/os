#!/usr/bin/env python3
"""oluştur 변환이 Türkçe dize_değer, 주석, 헤더 경로를 바꾸지 않는지 검사한다."""
from tanımlayıcı_dönüştürme import ÇEVİR_değer

kaynakKod = '''#include <Dosya_ABI.h>
#include "ağ_ABI.h"
// açık_Dosya 라는 주석
/* 자료이름 */
const char *Dosya_girdi_ad = "한글 \\" dize_değer";
char karakter_değer = '가';
int 파일열기_횟수 = 1;
'''
metinÇıktısı = ÇEVİR_değer(kaynakKod)
assert '#include <Dosya_ABI.h>' in metinÇıktısı
assert '#include "ağ_ABI.h"' in metinÇıktısı
assert '// açık_Dosya 라는 주석' in metinÇıktısı
assert '/* 자료이름 */' in metinÇıktısı
assert '"한글 \\" dize_değer"' in metinÇıktısı
assert "'가'" in metinÇıktısı
assert '\\ud30c\\uc77c\\uc774\\ub984' in metinÇıktısı
assert '파일열기_횟수' not in metinÇıktısı
assert ÇEVİR_değer(metinÇıktısı) == metinÇıktısı
print('PASS: Türkçe tanımlayıcı_değer ÇEVİR_değer/dize_değer·주석·yol 보존')

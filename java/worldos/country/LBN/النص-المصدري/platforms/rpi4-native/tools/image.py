#!/usr/bin/env python3
"""기존 مسار 호환 نقطة_الإدخال. الفعلي_بيانات 구현: ../أدوات/فتح_صورة.py"""
import importlib as 가져오기
import sys as نظام_تشغيل_قيمة
from pathlib import Path as مسار
نظام_تشغيل_قيمة.path.insert(0, str(مسار(__file__).resolve().parents[1] / 'أدوات'))
if __name__ == '__main__':
    import runpy as تطبيق_مشغّل
    تطبيق_مشغّل.run_module('فتح_صورة', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('فتح_صورة')
    대응 = {'total': 'إجمالي_قدرة', 'start': 'تشغيل', 'firmware': 'برنامج_ثابت_قيمة', 'files': 'ملف_قائمة', 'archive_base': 'أرشيف_أساس', 'partition': 'قسم_ملف', 'archive': 'أرشيف', 'main': 'تشغيل', 'block': 'بيانات_حظر', 'ROOT': 'يعرض_جذر', 'boot': '부팅경로', 'stage': 'لوحة_قيمة', 'out': 'مقياس_بيانات', 'expected': '예상결과', 'f': 'ملف_إدخال_3d0c1245', 'src': '원본주소', 'path': 'مسار', 'p': 'بيانات_منصب', 'extracted': '추출자료', 'member': 'عضو', 'mbr': 'سجل_الإقلاع_الرئيسي', 'image': 'صورة', 'sector_count': '섹터개수', 'dist': 'توزيع_مسار', 'sha': '해시계산', 'license_': 'ترخيص', 'source': '원본자료', 'name': 'اسم', 'value': 'قيمة', 'manifest': 'يُجمع_بيان', 'dest': 'وجهة_قيمة_منصب', 'work': '작업경로'}
    for 이전, حديث_عنصر in 대응.items():
        if hasattr(구현, حديث_عنصر): globals()[이전] = getattr(구현, حديث_عنصر)

#!/usr/bin/env python3
from pathlib import Path
import subprocess
import tempfile

موضع = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='jkoros-packet-test-') as 임시:
    دليل_قيمة = Path(임시)
    경계 = دليل_قيمة / '시험장치.java'
    경계.write_text('''
class جهاز_قيمة { static int طابع_زمني_قيمة; static int 밀리초() { return طابع_زمني_قيمة++; } static void 잠시양보() {} }
class نص_الوحدة_الطرفية { static void كتابة(String قيمة) {} static void كتابة_رقم(int قيمة) {} }
class شبكة_برنامج_تشغيل_الجهاز {
    static int 입출력기준주소 = 1, 송신수, 수신수;
    static int[] جهاز_عنوان = {0x52,0x54,0,0x12,0x34,0x56}, أصدقائي_قيمة;
    static int يستلم(int[] بيانات) { return 0; }
    static int يرسل(int[] بيانات, int 길이) { أصدقائي_قيمة = بيانات.clone(); return 길이; }
}''', encoding='utf-8')
    subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(دليل_قيمة), str(경계),
                    str(موضع / 'مصدر/شبكة_رمز.java'), str(موضع / 'اختبارات/حزمة_يختبر.java')], check=True)
    subprocess.run(['java', '-cp', str(دليل_قيمة), 'حزمة_يختبر'], check=True, timeout=10)

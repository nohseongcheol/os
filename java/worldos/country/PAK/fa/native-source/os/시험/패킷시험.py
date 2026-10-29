#!/usr/bin/env python3
from pathlib import Path
import subprocess
import tempfile

مرتب_کردن = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='jkoros-packet-test-') as 임시:
    فهرست_مقدار_e5561a2b = Path(임시)
    경계 = فهرست_مقدار_e5561a2b / '시험장치.java'
    경계.write_text('''
class دستگاه_مقدار { static int 시각; static int 밀리초() { return 시각++; } static void 잠시양보() {} }
class متن_پایانه { static void نوشتن(String مقدار) {} static void 수쓰기(int مقدار) {} }
class شبکه_درایور {
    static int 입출력기준주소 = 1, 송신수, 수신수;
    static int[] دستگاه_آدرس_856320c2 = {0x52,0x54,0,0x12,0x34,0x56}, اخیر_مقدار;
    static int 받기(int[] داده_ها) { return 0; }
    static int ارسال(int[] داده_ها, int طول_مقدار) { اخیر_مقدار = داده_ها.clone(); return طول_مقدار; }
}''', encoding='utf-8')
    subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(فهرست_مقدار_e5561a2b), str(경계),
                    str(مرتب_کردن / 'مبداء/شبکه_پشته.java'), str(مرتب_کردن / '시험/패킷시험.java')], check=True)
    subprocess.run(['java', '-cp', str(فهرست_مقدار_e5561a2b), '패킷시험'], check=True, timeout=10)

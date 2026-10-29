#!/usr/bin/env python3
from pathlib import Path
import subprocess
import tempfile

מיקום = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='jkoros-packet-test-') as 임시:
    מדריך_ערך = Path(임시)
    경계 = מדריך_ערך / '시험장치.java'
    경계.write_text('''
class התקן_ערך_e13f0cd9 { static int חותמת_זמן_ערך; static int 밀리초() { return חותמת_זמן_ערך++; } static void 잠시양보() {} }
class טקסט_מסוף { static void כתוב(String ערך) {} static void 수쓰기(int ערך) {} }
class רשת_מתאם {
    static int 입출력기준주소 = 1, 송신수, 수신수;
    static int[] התקן_למען = {0x52,0x54,0,0x12,0x34,0x56}, לאחרונה_ערך;
    static int לקבל(int[] נתונים) { return 0; }
    static int שלח(int[] נתונים, int 길이) { לאחרונה_ערך = נתונים.clone(); return 길이; }
}''', encoding='utf-8')
    subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(מדריך_ערך), str(경계),
                    str(מיקום / 'קודמקור/רשת_רמז.java'), str(מיקום / '시험/מנה_נסה.java')], check=True)
    subprocess.run(['java', '-cp', str(מדריך_ערך), 'מנה_נסה'], check=True, timeout=10)

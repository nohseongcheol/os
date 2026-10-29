#!/usr/bin/env python3
from pathlib import Path
import subprocess
import tempfile

위치 = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='jkoros-packet-test-') as 임시:
    ڈائریکٹری_قدر = Path(임시)
    경계 = ڈائریکٹری_قدر / '시험장치.java'
    경계.write_text('''
class آلہ_قدر { static int 시각; static int 밀리초() { return 시각++; } static void 잠시양보() {} }
class 문자단말 { static void لکھو(String قدر) {} static void 수쓰기(int قدر) {} }
class نیٹ_ورک_ڈرائیور {
    static int 입출력기준주소 = 1, 송신수, 수신수;
    static int[] آلہ_پتا = {0x52,0x54,0,0x12,0x34,0x56}, حالیہ_قدر;
    static int 받기(int[] کوائف) { return 0; }
    static int بھیجو(int[] کوائف, int لمبائی_قدر) { حالیہ_قدر = کوائف.clone(); return لمبائی_قدر; }
}''', encoding='utf-8')
    subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(ڈائریکٹری_قدر), str(경계),
                    str(위치 / 'ماخذ/نیٹ_ورک_گٹھا.java'), str(위치 / '시험/패킷시험.java')], check=True)
    subprocess.run(['java', '-cp', str(ڈائریکٹری_قدر), '패킷시험'], check=True, timeout=10)

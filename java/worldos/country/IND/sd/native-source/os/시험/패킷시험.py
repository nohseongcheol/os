#!/usr/bin/env python3
from pathlib import Path
import subprocess
import tempfile

위치 = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='jkoros-packet-test-') as 임시:
    ڊائريڪٽري_قدر = Path(임시)
    경계 = ڊائريڪٽري_قدر / '시험장치.java'
    경계.write_text('''
class آلو_قدر { static int 시각; static int 밀리초() { return 시각++; } static void 잠시양보() {} }
class 문자단말 { static void لکو(String قدر) {} static void 수쓰기(int قدر) {} }
class نيٽ_ورڪ_ڊرائيور {
    static int 입출력기준주소 = 1, 송신수, 수신수;
    static int[] آلو_پتو = {0x52,0x54,0,0x12,0x34,0x56}, حالیہ_قدر;
    static int 받기(int[] ڪوائف) { return 0; }
    static int اي_ميل(int[] ڪوائف, int لمبائي_قدر) { حالیہ_قدر = ڪوائف.clone(); return لمبائي_قدر; }
}''', encoding='utf-8')
    subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(ڊائريڪٽري_قدر), str(경계),
                    str(위치 / 'ماخذ/نيٽ_ورڪ_اڀرڻ.java'), str(위치 / '시험/패킷시험.java')], check=True)
    subprocess.run(['java', '-cp', str(ڊائريڪٽري_قدر), '패킷시험'], check=True, timeout=10)

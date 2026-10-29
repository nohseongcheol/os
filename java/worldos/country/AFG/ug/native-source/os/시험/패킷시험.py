#!/usr/bin/env python3
from pathlib import Path
import subprocess
import tempfile

ئورۇن = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='jkoros-packet-test-') as 임시:
    مۇندەرىجە_قىممىتى = Path(임시)
    경계 = مۇندەرىجە_قىممىتى / '시험장치.java'
    경계.write_text('''
class كۆچمە_قىممىتى { static int 시각; static int 밀리초() { return 시각++; } static void 잠시양보() {} }
class تېكست_تېرمىنال { static void ياز(String قىممىتى) {} static void 수쓰기(int قىممىتى) {} }
class تور_قوزغىتىش_پىروگراممىسى {
    static int 입출력기준주소 = 1, 송신수, 수신수;
    static int[] كۆچمە_ئادرېس = {0x52,0x54,0,0x12,0x34,0x56}, يېقىنقى_قىممىتى;
    static int 받기(int[] مەلۇمات) { return 0; }
    static int ئەۋەتمەك(int[] مەلۇمات, int ئۇزۇنلۇق_قىممىتى) { يېقىنقى_قىممىتى = مەلۇمات.clone(); return ئۇزۇنلۇق_قىممىتى; }
}''', encoding='utf-8')
    subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(مۇندەرىجە_قىممىتى), str(경계),
                    str(ئورۇن / 'مەنبە/تور_دۆۋە.java'), str(ئورۇن / '시험/패킷시험.java')], check=True)
    subprocess.run(['java', '-cp', str(مۇندەرىجە_قىممىتى), '패킷시험'], check=True, timeout=10)

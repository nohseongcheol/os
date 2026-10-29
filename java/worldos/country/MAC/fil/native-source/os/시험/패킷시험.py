#!/usr/bin/env python3
from pathlib import Path
import subprocess
import tempfile

posisyon = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='jkoros-packet-test-') as 임시:
    Directory_VALUE = Path(임시)
    경계 = Directory_VALUE / '시험장치.java'
    경계.write_text('''
class device_VALUE { static int 시각; static int 밀리초() { return 시각++; } static void 잠시양보() {} }
class SMS_Terminal { static void sumulat(String VALUE) {} static void 수쓰기(int VALUE) {} }
class Network_driver {
    static int 입출력기준주소 = 1, 송신수, 수신수;
    static int[] device_email = {0x52,0x54,0,0x12,0x34,0x56}, kamakailan_VALUE;
    static int 받기(int[] data) { return 0; }
    static int i_email(int[] data, int haba_VALUE) { kamakailan_VALUE = data.clone(); return haba_VALUE; }
}''', encoding='utf-8')
    subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(Directory_VALUE), str(경계),
                    str(posisyon / 'pinagmulan/Network_Stack.java'), str(posisyon / '시험/패킷시험.java')], check=True)
    subprocess.run(['java', '-cp', str(Directory_VALUE), '패킷시험'], check=True, timeout=10)

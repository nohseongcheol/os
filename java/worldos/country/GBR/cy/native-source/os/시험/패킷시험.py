#!/usr/bin/env python3
from pathlib import Path
import subprocess
import tempfile

safle = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='jkoros-packet-test-') as 임시:
    cyfeiriadur_VALUE = Path(임시)
    경계 = cyfeiriadur_VALUE / '시험장치.java'
    경계.write_text('''
class dyfais_VALUE { static int 시각; static int 밀리초() { return 시각++; } static void 잠시양보() {} }
class SMS_Terfynell { static void Ysgrifennu(String VALUE) {} static void 수쓰기(int VALUE) {} }
class Rhwydwaith_gyrrwr {
    static int 입출력기준주소 = 1, 송신수, 수신수;
    static int[] dyfais_ADDRESS = {0x52,0x54,0,0x12,0x34,0x56}, yn_ddiweddar_VALUE;
    static int 받기(int[] data) { return 0; }
    static int anfon(int[] data, int hyd_VALUE) { yn_ddiweddar_VALUE = data.clone(); return hyd_VALUE; }
}''', encoding='utf-8')
    subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(cyfeiriadur_VALUE), str(경계),
                    str(safle / 'FFYNHONNELL/Rhwydwaith_pentwr.java'), str(safle / '시험/패킷시험.java')], check=True)
    subprocess.run(['java', '-cp', str(cyfeiriadur_VALUE), '패킷시험'], check=True, timeout=10)

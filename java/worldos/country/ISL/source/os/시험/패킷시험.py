#!/usr/bin/env python3
from pathlib import Path
import subprocess
import tempfile

Staðsetning = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='jkoros-packet-test-') as 임시:
    skráasafn_VALUE = Path(임시)
    경계 = skráasafn_VALUE / '시험장치.java'
    경계.write_text('''
class tæki_VALUE { static int 시각; static int 밀리초() { return 시각++; } static void 잠시양보() {} }
class SMS_Endastöð { static void Skrift(String VALUE) {} static void skrifa_númer(int VALUE) {} }
class Net_rekill {
    static int 입출력기준주소 = 1, 송신수, 수신수;
    static int[] tæki_slóð = {0x52,0x54,0,0x12,0x34,0x56}, nýlegt_VALUE;
    static int 받기(int[] gögn) { return 0; }
    static int senda(int[] gögn, int lengd_VALUE) { nýlegt_VALUE = gögn.clone(); return lengd_VALUE; }
}''', encoding='utf-8')
    subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(skráasafn_VALUE), str(경계),
                    str(Staðsetning / 'Uppruni/Net_bunki.java'), str(Staðsetning / '시험/패킷시험.java')], check=True)
    subprocess.run(['java', '-cp', str(skráasafn_VALUE), '패킷시험'], check=True, timeout=10)

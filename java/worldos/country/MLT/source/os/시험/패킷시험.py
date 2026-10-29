#!/usr/bin/env python3
from pathlib import Path
import subprocess
import tempfile

pożizzjoni = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='jkoros-packet-test-') as 임시:
    direttorju_VALUE = Path(임시)
    경계 = direttorju_VALUE / '시험장치.java'
    경계.write_text('''
class mowbajl_VALUE { static int 시각; static int 밀리초() { return 시각++; } static void 잠시양보() {} }
class SMS_Terminal { static void kiteb(String VALUE) {} static void 수쓰기(int VALUE) {} }
class netwerk_drajver {
    static int 입출력기준주소 = 1, 송신수, 수신수;
    static int[] mowbajl_ADDRESS = {0x52,0x54,0,0x12,0x34,0x56}, reċenti_VALUE;
    static int 받기(int[] data) { return 0; }
    static int bagħat(int[] data, int tul_VALUE) { reċenti_VALUE = data.clone(); return tul_VALUE; }
}''', encoding='utf-8')
    subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(direttorju_VALUE), str(경계),
                    str(pożizzjoni / 'sors/netwerk_Munzell.java'), str(pożizzjoni / '시험/패킷시험.java')], check=True)
    subprocess.run(['java', '-cp', str(direttorju_VALUE), '패킷시험'], check=True, timeout=10)

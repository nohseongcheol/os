#!/usr/bin/env python3
from pathlib import Path
import subprocess
import tempfile

suidhich = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='jkoros-packet-test-') as 임시:
    eòlaire_VALUE = Path(임시)
    경계 = eòlaire_VALUE / '시험장치.java'
    경계.write_text('''
class uidheam_VALUE { static int 시각; static int 밀리초() { return 시각++; } static void 잠시양보() {} }
class SMS_tèirmineal { static void sgrìobh(String VALUE) {} static void 수쓰기(int VALUE) {} }
class lìonra_dràibhear {
    static int 입출력기준주소 = 1, 송신수, 수신수;
    static int[] uidheam_ADDRESS = {0x52,0x54,0,0x12,0x34,0x56}, o_chionn_ghoirid_VALUE;
    static int 받기(int[] dàta) { return 0; }
    static int cuir(int[] dàta, int faid_VALUE) { o_chionn_ghoirid_VALUE = dàta.clone(); return faid_VALUE; }
}''', encoding='utf-8')
    subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(eòlaire_VALUE), str(경계),
                    str(suidhich / 'tùs/lìonra_stac.java'), str(suidhich / '시험/패킷시험.java')], check=True)
    subprocess.run(['java', '-cp', str(eòlaire_VALUE), '패킷시험'], check=True, timeout=10)

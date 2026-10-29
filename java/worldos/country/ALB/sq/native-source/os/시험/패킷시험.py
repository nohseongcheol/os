#!/usr/bin/env python3
from pathlib import Path
import subprocess
import tempfile

Pozicioni = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='jkoros-packet-test-') as 임시:
    direktori_VALUE = Path(임시)
    경계 = direktori_VALUE / '시험장치.java'
    경계.write_text('''
class pajisje_VALUE { static int 시각; static int 밀리초() { return 시각++; } static void 잠시양보() {} }
class SMS_Terminali { static void Shkrimi(String VALUE) {} static void 수쓰기(int VALUE) {} }
class rrjet_drejtues {
    static int 입출력기준주소 = 1, 송신수, 수신수;
    static int[] pajisje_email = {0x52,0x54,0,0x12,0x34,0x56}, së_fundi_VALUE;
    static int 받기(int[] të_dhëna) { return 0; }
    static int dërgoj(int[] të_dhëna, int gjatësi_VALUE) { së_fundi_VALUE = të_dhëna.clone(); return gjatësi_VALUE; }
}''', encoding='utf-8')
    subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(direktori_VALUE), str(경계),
                    str(Pozicioni / 'BURIMI/rrjet_Stivë.java'), str(Pozicioni / '시험/패킷시험.java')], check=True)
    subprocess.run(['java', '-cp', str(direktori_VALUE), '패킷시험'], check=True, timeout=10)

#!/usr/bin/env python3
from pathlib import Path
import subprocess
import tempfile

suíomh = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='jkoros-packet-test-') as 임시:
    eolaire_VALUE = Path(임시)
    경계 = eolaire_VALUE / '시험장치.java'
    경계.write_text('''
class gléas_VALUE { static int 시각; static int 밀리초() { return 시각++; } static void 잠시양보() {} }
class SMS_Teirminéal { static void Scríobh(String VALUE) {} static void 수쓰기(int VALUE) {} }
class Líonra_tiománaí {
    static int 입출력기준주소 = 1, 송신수, 수신수;
    static int[] gléas_ADDRESS = {0x52,0x54,0,0x12,0x34,0x56}, le_déanaí_VALUE;
    static int 받기(int[] sonraí) { return 0; }
    static int seol(int[] sonraí, int fad_VALUE) { le_déanaí_VALUE = sonraí.clone(); return fad_VALUE; }
}''', encoding='utf-8')
    subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(eolaire_VALUE), str(경계),
                    str(suíomh / 'FOINSE/Líonra_Cruach.java'), str(suíomh / '시험/패킷시험.java')], check=True)
    subprocess.run(['java', '-cp', str(eolaire_VALUE), '패킷시험'], check=True, timeout=10)

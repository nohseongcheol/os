#!/usr/bin/env python3
from pathlib import Path
import subprocess
import tempfile

위치 = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='jkoros-packet-test-') as 임시:
    dàmb_xëyma = Path(임시)
    경계 = dàmb_xëyma / '시험장치.java'
    경계.write_text('''
class toftal_xëyma { static int 시각; static int 밀리초() { return 시각++; } static void 잠시양보() {} }
class 문자단말 { static void biir(String xëyma) {} static void 수쓰기(int xëyma) {} }
class mbaal_daraayba {
    static int 입출력기준주소 = 1, 송신수, 수신수;
    static int[] toftal_dëkkuwaay = {0x52,0x54,0,0x12,0x34,0x56}, bees_xëyma;
    static int 받기(int[] mbir) { return 0; }
    static int Yónnee(int[] mbir, int diir_xëyma) { bees_xëyma = mbir.clone(); return diir_xëyma; }
}''', encoding='utf-8')
    subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(dàmb_xëyma), str(경계),
                    str(위치 / 'Cosaan/mbaal_Tegalo.java'), str(위치 / '시험/패킷시험.java')], check=True)
    subprocess.run(['java', '-cp', str(dàmb_xëyma), '패킷시험'], check=True, timeout=10)

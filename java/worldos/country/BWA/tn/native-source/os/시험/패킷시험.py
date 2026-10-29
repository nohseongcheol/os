#!/usr/bin/env python3
from pathlib import Path
import subprocess
import tempfile

위치 = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='jkoros-packet-test-') as 임시:
    Lenaneofaele_Boleng = Path(임시)
    경계 = Lenaneofaele_Boleng / '시험장치.java'
    경계.write_text('''
class mobaele_Boleng { static int 시각; static int 밀리초() { return 시각++; } static void 잠시양보() {} }
class 문자단말 { static void kwala(String Boleng) {} static void 수쓰기(int Boleng) {} }
class Neteweke_selaodi {
    static int 입출력기준주소 = 1, 송신수, 수신수;
    static int[] mobaele_aterese = {0x52,0x54,0,0x12,0x34,0x56}, bošhweng_Boleng;
    static int 받기(int[] tshedimosetso) { return 0; }
    static int romela(int[] tshedimosetso, int boleele_Boleng) { bošhweng_Boleng = tshedimosetso.clone(); return boleele_Boleng; }
}''', encoding='utf-8')
    subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(Lenaneofaele_Boleng), str(경계),
                    str(위치 / 'Motswedi/Neteweke_kokoanyodinepe.java'), str(위치 / '시험/패킷시험.java')], check=True)
    subprocess.run(['java', '-cp', str(Lenaneofaele_Boleng), '패킷시험'], check=True, timeout=10)

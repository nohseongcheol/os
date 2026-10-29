#!/usr/bin/env python3
from pathlib import Path
import subprocess
import tempfile

위치 = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='jkoros-packet-test-') as 임시:
    tukimuagutiit_atuutilik = Path(임시)
    경계 = tukimuagutiit_atuutilik / '시험장치.java'
    경계.write_text('''
class sunakkutaaq_atuutilik { static int 시각; static int 밀리초() { return 시각++; } static void 잠시양보() {} }
class 문자단말 { static void titiraq(String atuutilik) {} static void 수쓰기(int atuutilik) {} }
class Kasuqatigiitsimajut_qarasaujalirijjut {
    static int 입출력기준주소 = 1, 송신수, 수신수;
    static int[] sunakkutaaq_turaarut = {0x52,0x54,0,0x12,0x34,0x56}, pirataarniku_atuutilik;
    static int 받기(int[] titiqqat) { return 0; }
    static int nassiutili(int[] titiqqat, int takininga_atuutilik) { pirataarniku_atuutilik = titiqqat.clone(); return takininga_atuutilik; }
}''', encoding='utf-8')
    subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(tukimuagutiit_atuutilik), str(경계),
                    str(위치 / 'pivviujuq/통신망.java'), str(위치 / '시험/패킷시험.java')], check=True)
    subprocess.run(['java', '-cp', str(tukimuagutiit_atuutilik), '패킷시험'], check=True, timeout=10)

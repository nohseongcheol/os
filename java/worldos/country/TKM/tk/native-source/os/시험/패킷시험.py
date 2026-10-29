#!/usr/bin/env python3
from pathlib import Path
import subprocess
import tempfile

위치 = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='jkoros-packet-test-') as 임시:
    katalog_baha = Path(임시)
    경계 = katalog_baha / '시험장치.java'
    경계.write_text('''
class enjam_baha { static int 시각; static int 밀리초() { return 시각++; } static void 잠시양보() {} }
class 문자단말 { static void Ýaz(String baha) {} static void 수쓰기(int baha) {} }
class Tor_draýwer {
    static int 입출력기준주소 = 1, 송신수, 수신수;
    static int[] enjam_salgy = {0x52,0x54,0,0x12,0x34,0x56}, Ýakynda_baha;
    static int 받기(int[] maglumat) { return 0; }
    static int iber(int[] maglumat, int dowamlylyk_baha) { Ýakynda_baha = maglumat.clone(); return dowamlylyk_baha; }
}''', encoding='utf-8')
    subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(katalog_baha), str(경계),
                    str(위치 / 'Çeşme/Tor_Desse.java'), str(위치 / '시험/패킷시험.java')], check=True)
    subprocess.run(['java', '-cp', str(katalog_baha), '패킷시험'], check=True, timeout=10)

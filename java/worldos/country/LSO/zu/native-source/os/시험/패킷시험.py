#!/usr/bin/env python3
from pathlib import Path
import subprocess
import tempfile

위치 = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='jkoros-packet-test-') as 임시:
    umkhombandlela_inani = Path(임시)
    경계 = umkhombandlela_inani / '시험장치.java'
    경계.write_text('''
class idivayisi_inani { static int 시각; static int 밀리초() { return 시각++; } static void 잠시양보() {} }
class 문자단말 { static void Bhala(String inani) {} static void 수쓰기(int inani) {} }
class iNethiwekhi_idrayiva {
    static int 입출력기준주소 = 1, 송신수, 수신수;
    static int[] idivayisi_ikheli = {0x52,0x54,0,0x12,0x34,0x56}, okwamuva_nje_inani;
    static int 받기(int[] imininingwane) { return 0; }
    static int Thumela(int[] imininingwane, int ubude_inani) { okwamuva_nje_inani = imininingwane.clone(); return ubude_inani; }
}''', encoding='utf-8')
    subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(umkhombandlela_inani), str(경계),
                    str(위치 / 'umthombo/iNethiwekhi_Isitaki.java'), str(위치 / '시험/패킷시험.java')], check=True)
    subprocess.run(['java', '-cp', str(umkhombandlela_inani), '패킷시험'], check=True, timeout=10)

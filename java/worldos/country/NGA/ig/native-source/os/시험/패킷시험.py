#!/usr/bin/env python3
from pathlib import Path
import subprocess
import tempfile

위치 = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='jkoros-packet-test-') as 임시:
    dàịrektrị_valuu = Path(임시)
    경계 = dàịrektrị_valuu / '시험장치.java'
    경계.write_text('''
class njìarụ_valuu { static int 시각; static int 밀리초() { return 시각++; } static void 잠시양보() {} }
class 문자단말 { static void Chekwaa_ozi(String valuu) {} static void 수쓰기(int valuu) {} }
class Netwọọkụ_ǹnyà {
    static int 입출력기준주소 = 1, 송신수, 수신수;
    static int[] njìarụ_àdreèsì = {0x52,0x54,0,0x12,0x34,0x56}, dị_nsonso_valuu;
    static int 받기(int[] datà) { return 0; }
    static int zìga(int[] datà, int ogologo_valuu) { dị_nsonso_valuu = datà.clone(); return ogologo_valuu; }
}''', encoding='utf-8')
    subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(dàịrektrị_valuu), str(경계),
                    str(위치 / 'ebensìbịa/Netwọọkụ_ikpo.java'), str(위치 / '시험/패킷시험.java')], check=True)
    subprocess.run(['java', '-cp', str(dàịrektrị_valuu), '패킷시험'], check=True, timeout=10)

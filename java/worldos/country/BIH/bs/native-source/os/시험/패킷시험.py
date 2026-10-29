#!/usr/bin/env python3
from pathlib import Path
import subprocess
import tempfile

Pozicija = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='jkoros-packet-test-') as 임시:
    Direktorij_VALUE = Path(임시)
    경계 = Direktorij_VALUE / '시험장치.java'
    경계.write_text('''
class uređaj_VALUE { static int 시각; static int 밀리초() { return 시각++; } static void 잠시양보() {} }
class SMS_Terminal { static void Piši(String VALUE) {} static void 수쓰기(int VALUE) {} }
class Mreža_drajver_uređaja {
    static int 입출력기준주소 = 1, prenositi_COUNT, 수신수;
    static int[] uređaj_adresa = {0x52,0x54,0,0x12,0x34,0x56}, nedavno_VALUE;
    static int 받기(int[] podaci) { return 0; }
    static int poslati(int[] podaci, int dužina_VALUE) { nedavno_VALUE = podaci.clone(); return dužina_VALUE; }
}''', encoding='utf-8')
    subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(Direktorij_VALUE), str(경계),
                    str(Pozicija / 'IZVOR/Mreža_snop.java'), str(Pozicija / '시험/패킷시험.java')], check=True)
    subprocess.run(['java', '-cp', str(Direktorij_VALUE), '패킷시험'], check=True, timeout=10)

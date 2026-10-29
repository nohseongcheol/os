#!/usr/bin/env python3
from pathlib import Path
import subprocess
import tempfile

Položaj = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='jkoros-packet-test-') as 임시:
    imenik_VALUE = Path(임시)
    경계 = imenik_VALUE / '시험장치.java'
    경계.write_text('''
class uređaj_VALUE { static int podaci_vremenske_oznake_VALUE; static int 밀리초() { return podaci_vremenske_oznake_VALUE++; } static void 잠시양보() {} }
class SMS_Terminal { static void Zapisuj(String VALUE) {} static void 수쓰기(int VALUE) {} }
class mreža_upravljački_program {
    static int 입출력기준주소 = 1, 송신수, primiti_COUNT;
    static int[] uređaj_adresa = {0x52,0x54,0,0x12,0x34,0x56}, nedavno_VALUE;
    static int primiti(int[] podaci) { return 0; }
    static int slati(int[] podaci, int 길이) { nedavno_VALUE = podaci.clone(); return 길이; }
}''', encoding='utf-8')
    subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(imenik_VALUE), str(경계),
                    str(Položaj / 'IZVOR/mreža_hrpa.java'), str(Položaj / '시험/패킷시험.java')], check=True)
    subprocess.run(['java', '-cp', str(imenik_VALUE), '패킷시험'], check=True, timeout=10)

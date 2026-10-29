#!/usr/bin/env python3
from pathlib import Path
import subprocess
import tempfile

Pozicija = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='jkoros-packet-test-') as 임시:
    Katalogas_VALUE = Path(임시)
    경계 = Katalogas_VALUE / '시험장치.java'
    경계.write_text('''
class įrenginys_VALUE { static int laiko_žyma_VALUE; static int 밀리초() { return laiko_žyma_VALUE++; } static void 잠시양보() {} }
class SMS_Terminalas { static void Rašymas(String VALUE) {} static void rašymas_numeris(int VALUE) {} }
class tinklas_tvarkyklė {
    static int 입출력기준주소 = 1, 송신수, gauti_COUNT;
    static int[] įrenginys_ADDRESS = {0x52,0x54,0,0x12,0x34,0x56}, naujausia_VALUE;
    static int gauti(int[] duomenys) { return 0; }
    static int siųsti(int[] duomenys, int 길이) { naujausia_VALUE = duomenys.clone(); return 길이; }
}''', encoding='utf-8')
    subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(Katalogas_VALUE), str(경계),
                    str(Pozicija / 'ŠALTINIS/tinklas_eilė.java'), str(Pozicija / '시험/패킷시험.java')], check=True)
    subprocess.run(['java', '-cp', str(Katalogas_VALUE), '패킷시험'], check=True, timeout=10)

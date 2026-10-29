#!/usr/bin/env python3
from pathlib import Path
import subprocess
import tempfile

Pozícia = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='jkoros-packet-test-') as 임시:
    Adresár_VALUE = Path(임시)
    경계 = Adresár_VALUE / '시험장치.java'
    경계.write_text('''
class telefón_VALUE { static int časová_pečiatka_VALUE; static int 밀리초() { return časová_pečiatka_VALUE++; } static void 잠시양보() {} }
class SMS_Terminál { static void Zápis(String VALUE) {} static void 수쓰기(int VALUE) {} }
class sieť_ovládač {
    static int 입출력기준주소 = 1, 송신수, dostať_COUNT;
    static int[] telefón_adresa = {0x52,0x54,0,0x12,0x34,0x56}, Nedávne_VALUE;
    static int dostať(int[] údaje) { return 0; }
    static int odoslať(int[] údaje, int dĺžka_VALUE) { Nedávne_VALUE = údaje.clone(); return dĺžka_VALUE; }
}''', encoding='utf-8')
    subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(Adresár_VALUE), str(경계),
                    str(Pozícia / 'ZDROJ/sieť_Vrstvy.java'), str(Pozícia / '시험/paket_test.java')], check=True)
    subprocess.run(['java', '-cp', str(Adresár_VALUE), 'paket_test'], check=True, timeout=10)

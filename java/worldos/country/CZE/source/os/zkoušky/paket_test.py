#!/usr/bin/env python3
from pathlib import Path
import subprocess
import tempfile

pozice = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='jkoros-packet-test-') as 임시:
    Adresář_HODNOTA = Path(임시)
    mez_HODNOTA = Adresář_HODNOTA / '시험장치.java'
    mez_HODNOTA.write_text('''
class mobilní_HODNOTA { static int timestamp_HODNOTA; static int 밀리초() { return timestamp_HODNOTA++; } static void 잠시양보() {} }
class SMS_Terminál { static void Zápis(String HODNOTA) {} static void zápis_číslo(int HODNOTA) {} }
class síť_ovladač {
    static int 입출력기준주소 = 1, 송신수, dostat_POČET;
    static int[] mobilní_ODKAZ = {0x52,0x54,0,0x12,0x34,0x56}, nedávné_HODNOTA;
    static int dostat(int[] data) { return 0; }
    static int poslat(int[] data, int délka_HODNOTA) { nedávné_HODNOTA = data.clone(); return délka_HODNOTA; }
}''', encoding='utf-8')
    subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(Adresář_HODNOTA), str(mez_HODNOTA),
                    str(pozice / 'zdrojový_soubor/síť_Štos.java'), str(pozice / 'zkoušky/paket_test.java')], check=True)
    subprocess.run(['java', '-cp', str(Adresář_HODNOTA), 'paket_test'], check=True, timeout=10)

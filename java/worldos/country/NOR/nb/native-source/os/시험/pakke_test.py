#!/usr/bin/env python3
from pathlib import Path
import subprocess
import tempfile

Posisjon = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='jkoros-packet-test-') as 임시:
    katalog_VERDI = Path(임시)
    grense_VERDI = katalog_VERDI / '시험장치.java'
    grense_VERDI.write_text('''
class enhet_VERDI { static int timestamp_VERDI; static int 밀리초() { return timestamp_VERDI++; } static void 잠시양보() {} }
class SMS_Terminal { static void Skriv(String VERDI) {} static void skrive_nummer(int VERDI) {} }
class nettverk_driver {
    static int 입출력기준주소 = 1, 송신수, motta_ANTALL;
    static int[] enhet_e_post = {0x52,0x54,0,0x12,0x34,0x56}, nyeste_VERDI;
    static int motta(int[] data) { return 0; }
    static int sende(int[] data, int lengde_VERDI) { nyeste_VERDI = data.clone(); return lengde_VERDI; }
}''', encoding='utf-8')
    subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(katalog_VERDI), str(grense_VERDI),
                    str(Posisjon / 'KILDE/nettverk_stakk.java'), str(Posisjon / '시험/pakke_test.java')], check=True)
    subprocess.run(['java', '-cp', str(katalog_VERDI), 'pakke_test'], check=True, timeout=10)

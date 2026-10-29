#!/usr/bin/env python3
from pathlib import Path
import subprocess
import tempfile

position = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='jkoros-packet-test-') as 임시:
    Katalog_värde = Path(임시)
    gräns_värde = Katalog_värde / '시험장치.java'
    gräns_värde.write_text('''
class enhet_värde { static int tidsstämpel_värde; static int 밀리초() { return tidsstämpel_värde++; } static void 잠시양보() {} }
class SMS_Terminal { static void Skriv(String värde) {} static void skriva_nummer(int värde) {} }
class nätverk_drivrutin {
    static int 입출력기준주소 = 1, 송신수, få_ANTAL;
    static int[] enhet_ADRESS = {0x52,0x54,0,0x12,0x34,0x56}, senaste_värde;
    static int få(int[] data) { return 0; }
    static int skicka(int[] data, int längd_värde) { senaste_värde = data.clone(); return längd_värde; }
}''', encoding='utf-8')
    subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(Katalog_värde), str(gräns_värde),
                    str(position / 'källfil/nätverk_Stack.java'), str(position / 'tester/paket_test.java')], check=True)
    subprocess.run(['java', '-cp', str(Katalog_värde), 'paket_test'], check=True, timeout=10)

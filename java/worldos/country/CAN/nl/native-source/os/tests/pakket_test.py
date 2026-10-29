#!/usr/bin/env python3
from pathlib import Path
import subprocess
import tempfile

positie = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='jkoros-packet-test-') as 임시:
    map_WAARDE = Path(임시)
    grens_WAARDE = map_WAARDE / '시험장치.java'
    grens_WAARDE.write_text('''
class mobiel_WAARDE { static int timestamp_WAARDE; static int 밀리초() { return timestamp_WAARDE++; } static void 잠시양보() {} }
class sms_Terminal { static void Schrijven(String WAARDE) {} static void schrijven_nummer(int WAARDE) {} }
class net_stuurprogramma {
    static int 입출력기준주소 = 1, 송신수, ontvangen_AANTAL;
    static int[] mobiel_ADRES = {0x52,0x54,0,0x12,0x34,0x56}, recent_WAARDE;
    static int ontvangen(int[] gegevens) { return 0; }
    static int e_mailen(int[] gegevens, int tijdsduur_WAARDE) { recent_WAARDE = gegevens.clone(); return tijdsduur_WAARDE; }
}''', encoding='utf-8')
    subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(map_WAARDE), str(grens_WAARDE),
                    str(positie / 'broncode/net_stack.java'), str(positie / 'tests/pakket_test.java')], check=True)
    subprocess.run(['java', '-cp', str(map_WAARDE), 'pakket_test'], check=True, timeout=10)

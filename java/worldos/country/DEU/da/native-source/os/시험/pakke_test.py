#!/usr/bin/env python3
from pathlib import Path
import subprocess
import tempfile

Placering = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='jkoros-packet-test-') as 임시:
    mappe_VÆRDI = Path(임시)
    grænse_VÆRDI = mappe_VÆRDI / '시험장치.java'
    grænse_VÆRDI.write_text('''
class enhed_VÆRDI { static int timestamp_VÆRDI; static int 밀리초() { return timestamp_VÆRDI++; } static void 잠시양보() {} }
class sms_Terminal { static void Skrive(String VÆRDI) {} static void skrive_tal(int VÆRDI) {} }
class netværk_driver {
    static int 입출력기준주소 = 1, 송신수, modtage_TÆL;
    static int[] enhed_mail = {0x52,0x54,0,0x12,0x34,0x56}, seneste_VÆRDI;
    static int modtage(int[] data) { return 0; }
    static int maile(int[] data, int varighed_VÆRDI) { seneste_VÆRDI = data.clone(); return varighed_VÆRDI; }
}''', encoding='utf-8')
    subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(mappe_VÆRDI), str(grænse_VÆRDI),
                    str(Placering / 'KILDE/netværk_Stak.java'), str(Placering / '시험/pakke_test.java')], check=True)
    subprocess.run(['java', '-cp', str(mappe_VÆRDI), 'pakke_test'], check=True, timeout=10)

#!/usr/bin/env python3
from pathlib import Path
import subprocess
import tempfile

Novietojums = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='jkoros-packet-test-') as 임시:
    Direktorijs_VALUE = Path(임시)
    경계 = Direktorijs_VALUE / '시험장치.java'
    경계.write_text('''
class ierīce_VALUE { static int timestamp_VALUE; static int 밀리초() { return timestamp_VALUE++; } static void 잠시양보() {} }
class SMS_Terminālis { static void Rakstīt(String VALUE) {} static void rakstīšana_numurs(int VALUE) {} }
class tīkls_draiveris {
    static int 입출력기준주소 = 1, 송신수, saņemt_COUNT;
    static int[] ierīce_adrese = {0x52,0x54,0,0x12,0x34,0x56}, pēdējās_VALUE;
    static int saņemt(int[] dati) { return 0; }
    static int sūtīt(int[] dati, int 길이) { pēdējās_VALUE = dati.clone(); return 길이; }
}''', encoding='utf-8')
    subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(Direktorijs_VALUE), str(경계),
                    str(Novietojums / 'AVOTS/tīkls_kopa.java'), str(Novietojums / '시험/패킷시험.java')], check=True)
    subprocess.run(['java', '-cp', str(Direktorijs_VALUE), '패킷시험'], check=True, timeout=10)

#!/usr/bin/env python3
from pathlib import Path
import subprocess
import tempfile

Poziție = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='jkoros-packet-test-') as 임시:
    Director_VALUE = Path(임시)
    경계 = Director_VALUE / '시험장치.java'
    경계.write_text('''
class mobil_VALUE { static int marcă_de_timp_VALUE; static int 밀리초() { return marcă_de_timp_VALUE++; } static void 잠시양보() {} }
class SMS_Terminal { static void Scriere(String VALUE) {} static void 수쓰기(int VALUE) {} }
class rețea_driver {
    static int 입출력기준주소 = 1, 송신수, primi_COUNT;
    static int[] mobil_adresa = {0x52,0x54,0,0x12,0x34,0x56}, recent_VALUE;
    static int primi(int[] date) { return 0; }
    static int trimite(int[] date, int lungime_VALUE) { recent_VALUE = date.clone(); return lungime_VALUE; }
}''', encoding='utf-8')
    subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(Director_VALUE), str(경계),
                    str(Poziție / 'SURSĂ/rețea_Teanc.java'), str(Poziție / '시험/패킷시험.java')], check=True)
    subprocess.run(['java', '-cp', str(Director_VALUE), '패킷시험'], check=True, timeout=10)

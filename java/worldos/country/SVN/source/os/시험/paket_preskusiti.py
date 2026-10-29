#!/usr/bin/env python3
from pathlib import Path
import subprocess
import tempfile

Položaj = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='jkoros-packet-test-') as 임시:
    Imenik_VALUE = Path(임시)
    경계 = Imenik_VALUE / '시험장치.java'
    경계.write_text('''
class naprava_VALUE { static int timestamp_VALUE; static int 밀리초() { return timestamp_VALUE++; } static void 잠시양보() {} }
class SMS_Terminal { static void Pisanje(String VALUE) {} static void 수쓰기(int VALUE) {} }
class mreža_gonilnik {
    static int 입출력기준주소 = 1, 송신수, sprejeti_sprejemati_prejeti_prejemati_COUNT;
    static int[] naprava_naslov = {0x52,0x54,0,0x12,0x34,0x56}, Nedavno_VALUE;
    static int sprejeti_sprejemati_prejeti_prejemati(int[] podatki) { return 0; }
    static int poslati(int[] podatki, int 길이) { Nedavno_VALUE = podatki.clone(); return 길이; }
}''', encoding='utf-8')
    subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(Imenik_VALUE), str(경계),
                    str(Položaj / 'VIR/mreža_Sklad.java'), str(Položaj / '시험/paket_preskusiti.java')], check=True)
    subprocess.run(['java', '-cp', str(Imenik_VALUE), 'paket_preskusiti'], check=True, timeout=10)

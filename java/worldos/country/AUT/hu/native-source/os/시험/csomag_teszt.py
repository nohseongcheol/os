#!/usr/bin/env python3
from pathlib import Path
import subprocess
import tempfile

Pozíció = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='jkoros-packet-test-') as 임시:
    címtár_ÉRTÉK = Path(임시)
    határ_ÉRTÉK = címtár_ÉRTÉK / '시험장치.java'
    határ_ÉRTÉK.write_text('''
class mobil_ÉRTÉK { static int timestamp_ÉRTÉK; static int 밀리초() { return timestamp_ÉRTÉK++; } static void 잠시양보() {} }
class SMS_Terminál { static void Írás(String ÉRTÉK) {} static void ír_szám(int ÉRTÉK) {} }
class hálózat_eszközillesztő {
    static int 입출력기준주소 = 1, 송신수, fogad_DARAB;
    static int[] mobil_CÍM = {0x52,0x54,0,0x12,0x34,0x56}, aktuális_ÉRTÉK;
    static int fogad(int[] adat) { return 0; }
    static int küld(int[] adat, int hossz_ÉRTÉK) { aktuális_ÉRTÉK = adat.clone(); return hossz_ÉRTÉK; }
}''', encoding='utf-8')
    subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(címtár_ÉRTÉK), str(határ_ÉRTÉK),
                    str(Pozíció / 'FORRÁS/hálózat_Sor.java'), str(Pozíció / '시험/csomag_teszt.java')], check=True)
    subprocess.run(['java', '-cp', str(címtár_ÉRTÉK), 'csomag_teszt'], check=True, timeout=10)

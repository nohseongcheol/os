#!/usr/bin/env python3
from pathlib import Path
import subprocess
import tempfile

paikka = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='jkoros-packet-test-') as 임시:
    Directory_ARVO = Path(임시)
    rajattu_alue_ARVO = Directory_ARVO / '시험장치.java'
    rajattu_alue_ARVO.write_text('''
class laite_ARVO { static int aikaleima_ARVO; static int 밀리초() { return aikaleima_ARVO++; } static void 잠시양보() {} }
class SMS_Pääte { static void Kirjoitus(String ARVO) {} static void kirjoitus_numero(int ARVO) {} }
class verkko_ohjain {
    static int 입출력기준주소 = 1, lähettää_LASKE, saada_LASKE;
    static int[] laite_OSOITE = {0x52,0x54,0,0x12,0x34,0x56}, viimeisimmät_ARVO;
    static int saada(int[] data) { return 0; }
    static int lähettää(int[] data, int kesto_ARVO) { viimeisimmät_ARVO = data.clone(); return kesto_ARVO; }
}''', encoding='utf-8')
    subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(Directory_ARVO), str(rajattu_alue_ARVO),
                    str(paikka / 'lähdetiedosto/verkko_Pino.java'), str(paikka / 'testit/paketti_testi.java')], check=True)
    subprocess.run(['java', '-cp', str(Directory_ARVO), 'paketti_testi'], check=True, timeout=10)

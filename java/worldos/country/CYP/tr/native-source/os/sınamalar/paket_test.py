#!/usr/bin/env python3
from pathlib import Path
import subprocess
import tempfile

konum = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='jkoros-packet-test-') as 임시:
    dizin_değer = Path(임시)
    sınır_değer = dizin_değer / '시험장치.java'
    sınır_değer.write_text('''
class cihaz_değer { static int zaman_damgası_değer; static int 밀리초() { return zaman_damgası_değer++; } static void 잠시양보() {} }
class SMS_Terminal { static void Yazma(String değer) {} static void 수쓰기(int değer) {} }
class ağ_sürücü {
    static int 입출력기준주소 = 1, 송신수, almak_BAĞ_DEĞ_SAY;
    static int[] cihaz_ADRES = {0x52,0x54,0,0x12,0x34,0x56}, en_son_değer;
    static int almak(int[] veri) { return 0; }
    static int göndermek(int[] veri, int süre_değer) { en_son_değer = veri.clone(); return süre_değer; }
}''', encoding='utf-8')
    subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(dizin_değer), str(sınır_değer),
                    str(konum / 'kaynakKod/ağ_Yığın.java'), str(konum / 'sınamalar/paket_test.java')], check=True)
    subprocess.run(['java', '-cp', str(dizin_değer), 'paket_test'], check=True, timeout=10)

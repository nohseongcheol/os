#!/usr/bin/env python3
from pathlib import Path
import subprocess
import tempfile

pozycja = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='jkoros-packet-test-') as 임시:
    Katalog_WARTOŚĆ = Path(임시)
    granica_WARTOŚĆ = Katalog_WARTOŚĆ / '시험장치.java'
    granica_WARTOŚĆ.write_text('''
class urządzenie_WARTOŚĆ { static int znacznik_czasu_WARTOŚĆ; static int 밀리초() { return znacznik_czasu_WARTOŚĆ++; } static void 잠시양보() {} }
class SMS_Terminal { static void Zapis(String WARTOŚĆ) {} static void zapis_identyfikator(int WARTOŚĆ) {} }
class sieć_sterownik {
    static int 입출력기준주소 = 1, 송신수, odbierać_ILE_LICZB;
    static int[] urządzenie_ADRES = {0x52,0x54,0,0x12,0x34,0x56}, ostatnio_WARTOŚĆ;
    static int odbierać(int[] dane) { return 0; }
    static int wysłać(int[] dane, int długość_WARTOŚĆ) { ostatnio_WARTOŚĆ = dane.clone(); return długość_WARTOŚĆ; }
}''', encoding='utf-8')
    subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(Katalog_WARTOŚĆ), str(granica_WARTOŚĆ),
                    str(pozycja / 'plik_źródłowy/sieć_Stos.java'), str(pozycja / 'testy/pakiet_test.java')], check=True)
    subprocess.run(['java', '-cp', str(Katalog_WARTOŚĆ), 'pakiet_test'], check=True, timeout=10)

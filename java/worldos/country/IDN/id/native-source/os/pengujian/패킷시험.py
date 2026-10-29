#!/usr/bin/env python3
from pathlib import Path
import subprocess
import tempfile

posisi = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='jkoros-packet-test-') as 임시:
    Direktori_VALUE = Path(임시)
    경계 = Direktori_VALUE / '시험장치.java'
    경계.write_text('''
class Ponsel_VALUE { static int stempel_waktu_VALUE; static int 밀리초() { return stempel_waktu_VALUE++; } static void 잠시양보() {} }
class SMS_Terminal { static void Tulis(String VALUE) {} static void 수쓰기(int VALUE) {} }
class jaringan_driver {
    static int 입출력기준주소 = 1, 송신수, terima_COUNT;
    static int[] Ponsel_surel = {0x52,0x54,0,0x12,0x34,0x56}, terakhir_VALUE;
    static int terima(int[] data) { return 0; }
    static int kirim(int[] data, int panjang_VALUE) { terakhir_VALUE = data.clone(); return panjang_VALUE; }
}''', encoding='utf-8')
    subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(Direktori_VALUE), str(경계),
                    str(posisi / 'kodeSumber/jaringan_tumpuk.java'), str(posisi / 'pengujian/패킷시험.java')], check=True)
    subprocess.run(['java', '-cp', str(Direktori_VALUE), '패킷시험'], check=True, timeout=10)

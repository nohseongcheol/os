#!/usr/bin/env python3
from pathlib import Path
import subprocess
import tempfile

Holati = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='jkoros-packet-test-') as 임시:
    katalog_VALUE = Path(임시)
    경계 = katalog_VALUE / '시험장치.java'
    경계.write_text('''
class qurilma_VALUE { static int 시각; static int 밀리초() { return 시각++; } static void 잠시양보() {} }
class SMS_Terminal { static void Yozish(String VALUE) {} static void 수쓰기(int VALUE) {} }
class Tarmoq_drayver {
    static int 입출력기준주소 = 1, 송신수, 수신수;
    static int[] qurilma_manzil = {0x52,0x54,0,0x12,0x34,0x56}, so_nggi_VALUE;
    static int 받기(int[] ma_lumotlar) { return 0; }
    static int yuborish(int[] ma_lumotlar, int uzunlik_VALUE) { so_nggi_VALUE = ma_lumotlar.clone(); return uzunlik_VALUE; }
}''', encoding='utf-8')
    subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(katalog_VALUE), str(경계),
                    str(Holati / 'manba/Tarmoq_Stack.java'), str(Holati / '시험/패킷시험.java')], check=True)
    subprocess.run(['java', '-cp', str(katalog_VALUE), '패킷시험'], check=True, timeout=10)

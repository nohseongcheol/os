#!/usr/bin/env python3
from pathlib import Path
import subprocess
import tempfile

yerinə_qoymaq = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='jkoros-packet-test-') as 임시:
    kataloq_VALUE = Path(임시)
    경계 = kataloq_VALUE / '시험장치.java'
    경계.write_text('''
class cihaz_VALUE { static int 시각; static int 밀리초() { return 시각++; } static void 잠시양보() {} }
class SMS_Terminal { static void Yazma(String VALUE) {} static void 수쓰기(int VALUE) {} }
class Şəbəkə_drayver {
    static int 입출력기준주소 = 1, 송신수, 수신수;
    static int[] cihaz_ünvan = {0x52,0x54,0,0x12,0x34,0x56}, son_VALUE;
    static int 받기(int[] verilənlər) { return 0; }
    static int göndərmək(int[] verilənlər, int uzunluq_VALUE) { son_VALUE = verilənlər.clone(); return uzunluq_VALUE; }
}''', encoding='utf-8')
    subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(kataloq_VALUE), str(경계),
                    str(yerinə_qoymaq / 'QAYNAQ/Şəbəkə_Yığın.java'), str(yerinə_qoymaq / '시험/패킷시험.java')], check=True)
    subprocess.run(['java', '-cp', str(kataloq_VALUE), '패킷시험'], check=True, timeout=10)

#!/usr/bin/env python3
from pathlib import Path
import subprocess
import tempfile

Kedudukan = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='jkoros-packet-test-') as 임시:
    direktori_VALUE = Path(임시)
    경계 = direktori_VALUE / '시험장치.java'
    경계.write_text('''
class peranti_VALUE { static int cap_masa_VALUE; static int 밀리초() { return cap_masa_VALUE++; } static void 잠시양보() {} }
class SMS_Terminal { static void Tulis(String VALUE) {} static void 수쓰기(int VALUE) {} }
class rangkaian_pemacu {
    static int 입출력기준주소 = 1, 송신수, 수신수;
    static int[] peranti_e_mel = {0x52,0x54,0,0x12,0x34,0x56}, terbaru_VALUE;
    static int 받기(int[] data) { return 0; }
    static int e_mel_9aee63bd(int[] data, int kepanjangan_VALUE) { terbaru_VALUE = data.clone(); return kepanjangan_VALUE; }
}''', encoding='utf-8')
    subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(direktori_VALUE), str(경계),
                    str(Kedudukan / 'SUMBER/rangkaian_tindan.java'), str(Kedudukan / 'ujian/paket_ujian.java')], check=True)
    subprocess.run(['java', '-cp', str(direktori_VALUE), 'paket_ujian'], check=True, timeout=10)

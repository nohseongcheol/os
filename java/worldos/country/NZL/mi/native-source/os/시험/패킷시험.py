#!/usr/bin/env python3
from pathlib import Path
import subprocess
import tempfile

tūranga = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='jkoros-packet-test-') as 임시:
    whaiaronga_uara = Path(임시)
    경계 = whaiaronga_uara / '시험장치.java'
    경계.write_text('''
class pūkoro_uara { static int 시각; static int 밀리초() { return 시각++; } static void 잠시양보() {} }
class TEXT_Tauranga { static void Tuhia(String uara) {} static void 수쓰기(int uara) {} }
class whatunga_atekōkiri {
    static int 입출력기준주소 = 1, 송신수, 수신수;
    static int[] pūkoro_ADDRESS = {0x52,0x54,0,0x12,0x34,0x56}, nōnākuanei_uara;
    static int 받기(int[] raraunga) { return 0; }
    static int tuku(int[] raraunga, int roa_uara) { nōnākuanei_uara = raraunga.clone(); return roa_uara; }
}''', encoding='utf-8')
    subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(whaiaronga_uara), str(경계),
                    str(tūranga / 'pūtake/whatunga_Huinga.java'), str(tūranga / '시험/패킷시험.java')], check=True)
    subprocess.run(['java', '-cp', str(whaiaronga_uara), '패킷시험'], check=True, timeout=10)

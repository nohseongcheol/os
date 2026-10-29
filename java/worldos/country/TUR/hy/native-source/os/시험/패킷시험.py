#!/usr/bin/env python3
from pathlib import Path
import subprocess
import tempfile

Դիրք = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='jkoros-packet-test-') as 임시:
    գրացուցակ_արժեք = Path(임시)
    경계 = գրացուցակ_արժեք / '시험장치.java'
    경계.write_text('''
class սարք_արժեք { static int 시각; static int 밀리초() { return 시각++; } static void 잠시양보() {} }
class Գրվածք_Տերմինալ { static void Գրել(String արժեք) {} static void 수쓰기(int արժեք) {} }
class Ցանց_սարքավար {
    static int 입출력기준주소 = 1, 송신수, 수신수;
    static int[] սարք_հասցե = {0x52,0x54,0,0x12,0x34,0x56}, վերջերս_արժեք;
    static int 받기(int[] տվյալ) { return 0; }
    static int ուղարկել(int[] տվյալ, int տեւողություն_արժեք) { վերջերս_արժեք = տվյալ.clone(); return տեւողություն_արժեք; }
}''', encoding='utf-8')
    subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(գրացուցակ_արժեք), str(경계),
                    str(Դիրք / 'ԱՂԲՅՈՒՐ/Ցանց_Շեղջ.java'), str(Դիրք / '시험/패킷시험.java')], check=True)
    subprocess.run(['java', '-cp', str(գրացուցակ_արժեք), '패킷시험'], check=True, timeout=10)

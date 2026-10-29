#!/usr/bin/env python3
from pathlib import Path
import subprocess
import tempfile

Орны = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='jkoros-packet-test-') as 임시:
    каталог_мән = Path(임시)
    경계 = каталог_мән / '시험장치.java'
    경계.write_text('''
class құрылғы_мән { static int 시각; static int 밀리초() { return 시각++; } static void 잠시양보() {} }
class Мәтін_Терминал { static void Жазу(String мән) {} static void 수쓰기(int мән) {} }
class желі_драйвер {
    static int 입출력기준주소 = 1, 송신수, 수신수;
    static int[] құрылғы_мекенжай = {0x52,0x54,0,0x12,0x34,0x56}, соңғы_мән;
    static int 받기(int[] деректер) { return 0; }
    static int жіберу(int[] деректер, int ұзындық_мән) { соңғы_мән = деректер.clone(); return ұзындық_мән; }
}''', encoding='utf-8')
    subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(каталог_мән), str(경계),
                    str(Орны / 'Неден/желі_Бума.java'), str(Орны / '시험/패킷시험.java')], check=True)
    subprocess.run(['java', '-cp', str(каталог_мән), '패킷시험'], check=True, timeout=10)

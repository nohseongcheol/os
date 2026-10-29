#!/usr/bin/env python3
from pathlib import Path
import subprocess
import tempfile

Турган_жери = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='jkoros-packet-test-') as 임시:
    каталог_маани = Path(임시)
    경계 = каталог_маани / '시험장치.java'
    경계.write_text('''
class түзмөк_маани { static int 시각; static int 밀리초() { return 시각++; } static void 잠시양보() {} }
class 문자단말 { static void Жазуу(String маани) {} static void 수쓰기(int маани) {} }
class Желе_драйвер {
    static int 입출력기준주소 = 1, 송신수, 수신수;
    static int[] түзмөк_дарек = {0x52,0x54,0,0x12,0x34,0x56}, жакынкы_маани;
    static int 받기(int[] берилмелер) { return 0; }
    static int жөнөтүү(int[] берилмелер, int узундук_маани) { жакынкы_маани = берилмелер.clone(); return узундук_маани; }
}''', encoding='utf-8')
    subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(каталог_маани), str(경계),
                    str(Турган_жери / 'Булак/Желе_стек.java'), str(Турган_жери / '시험/패킷시험.java')], check=True)
    subprocess.run(['java', '-cp', str(каталог_маани), '패킷시험'], check=True, timeout=10)

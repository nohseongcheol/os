#!/usr/bin/env python3
from pathlib import Path
import subprocess
import tempfile

Пазіцыя = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='jkoros-packet-test-') as 임시:
    каталог_значэнне = Path(임시)
    경계 = каталог_значэнне / '시험장치.java'
    경계.write_text('''
class прылада_значэнне { static int 시각; static int 밀리초() { return 시각++; } static void 잠시양보() {} }
class 문자단말 { static void Запіс(String значэнне) {} static void 수쓰기(int значэнне) {} }
class Сетка_драйвер {
    static int 입출력기준주소 = 1, 송신수, 수신수;
    static int[] прылада_адрас = {0x52,0x54,0,0x12,0x34,0x56}, апошнія_значэнне;
    static int 받기(int[] дадзеныя) { return 0; }
    static int адправіць(int[] дадзеныя, int даўжыня_значэнне) { апошнія_значэнне = дадзеныя.clone(); return даўжыня_значэнне; }
}''', encoding='utf-8')
    subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(каталог_значэнне), str(경계),
                    str(Пазіцыя / 'КРЫНІЦА/Сетка_Стэк.java'), str(Пазіцыя / '시험/패킷시험.java')], check=True)
    subprocess.run(['java', '-cp', str(каталог_значэнне), '패킷시험'], check=True, timeout=10)

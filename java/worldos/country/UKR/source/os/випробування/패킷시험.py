#!/usr/bin/env python3
from pathlib import Path
import subprocess
import tempfile

позиція = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='jkoros-packet-test-') as 임시:
    Каталог_значення = Path(임시)
    경계 = Каталог_значення / '시험장치.java'
    경계.write_text('''
class пристрій_значення { static int позначка_часу_значення; static int 밀리초() { return позначка_часу_значення++; } static void 잠시양보() {} }
class Текст_Термінал { static void Запис(String значення) {} static void 수쓰기(int значення) {} }
class мережа_драйвер {
    static int 입출력기준주소 = 1, 송신수, 수신수;
    static int[] пристрій_адреса = {0x52,0x54,0,0x12,0x34,0x56}, останні_значення;
    static int отримувати(int[] дані) { return 0; }
    static int надсилати(int[] дані, int 길이) { останні_значення = дані.clone(); return 길이; }
}''', encoding='utf-8')
    subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(Каталог_значення), str(경계),
                    str(позиція / 'вихіднийКод/мережа_Стіс.java'), str(позиція / 'випробування/패킷시험.java')], check=True)
    subprocess.run(['java', '-cp', str(Каталог_значення), '패킷시험'], check=True, timeout=10)

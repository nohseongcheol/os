#!/usr/bin/env python3
from pathlib import Path
import subprocess
import tempfile

позиция = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='jkoros-packet-test-') as 임시:
    Каталог_ЗНАЧЕН = Path(임시)
    граница_ЗНАЧЕН = Каталог_ЗНАЧЕН / '시험장치.java'
    граница_ЗНАЧЕН.write_text('''
class устройство_ЗНАЧЕН { static int метка_времени_ЗНАЧЕН; static int 밀리초() { return метка_времени_ЗНАЧЕН++; } static void 잠시양보() {} }
class SMS_Терминал { static void Запись(String ЗНАЧЕН) {} static void 수쓰기(int ЗНАЧЕН) {} }
class драйвер_сетевого_устройства {
    static int 입출력기준주소 = 1, 송신수, получить_СЧЁТ;
    static int[] устройство_АДРЕС = {0x52,0x54,0,0x12,0x34,0x56}, Что_нового_ЗНАЧЕН;
    static int получить(int[] данные) { return 0; }
    static int написать(int[] данные, int длина_ЗНАЧЕН) { Что_нового_ЗНАЧЕН = данные.clone(); return длина_ЗНАЧЕН; }
}''', encoding='utf-8')
    subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(Каталог_ЗНАЧЕН), str(граница_ЗНАЧЕН),
                    str(позиция / 'исходныйКод/сеть_стек.java'), str(позиция / 'испытания/пакет_тест.java')], check=True)
    subprocess.run(['java', '-cp', str(Каталог_ЗНАЧЕН), 'пакет_тест'], check=True, timeout=10)

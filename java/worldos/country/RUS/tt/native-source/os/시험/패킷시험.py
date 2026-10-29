#!/usr/bin/env python3
from pathlib import Path
import subprocess
import tempfile

урнаштыру = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='jkoros-packet-test-') as 임시:
    каталог_VALUE = Path(임시)
    경계 = каталог_VALUE / '시험장치.java'
    경계.write_text('''
class мобиль_VALUE { static int 시각; static int 밀리초() { return 시각++; } static void 잠시양보() {} }
class СМС_Терминал { static void язу(String VALUE) {} static void 수쓰기(int VALUE) {} }
class Челтәр_драйвер {
    static int 입출력기준주소 = 1, 송신수, 수신수;
    static int[] мобиль_адрес = {0x52,0x54,0,0x12,0x34,0x56}, соңгы_VALUE;
    static int 받기(int[] мәгълүмат) { return 0; }
    static int җибәрү(int[] мәгълүмат, int озынлык_VALUE) { соңгы_VALUE = мәгълүмат.clone(); return озынлык_VALUE; }
}''', encoding='utf-8')
    subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(каталог_VALUE), str(경계),
                    str(урнаштыру / 'чыганак/Челтәр_Стәк.java'), str(урнаштыру / '시험/패킷시험.java')], check=True)
    subprocess.run(['java', '-cp', str(каталог_VALUE), '패킷시험'], check=True, timeout=10)

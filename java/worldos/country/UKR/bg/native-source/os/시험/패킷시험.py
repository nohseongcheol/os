#!/usr/bin/env python3
from pathlib import Path
import subprocess
import tempfile

Позиция = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='jkoros-packet-test-') as 임시:
    указател_стойност = Path(임시)
    경계 = указател_стойност / '시험장치.java'
    경계.write_text('''
class устройство_стойност { static int времево_клеймо_стойност; static int 밀리초() { return времево_клеймо_стойност++; } static void 잠시양보() {} }
class Текст_Терминал { static void Писане(String стойност) {} static void 수쓰기(int стойност) {} }
class мрежа_драйвер {
    static int 입출력기준주소 = 1, 송신수, 수신수;
    static int[] устройство_адрес = {0x52,0x54,0,0x12,0x34,0x56}, скорошни_стойност;
    static int получавам(int[] данни) { return 0; }
    static int изпращам(int[] данни, int 길이) { скорошни_стойност = данни.clone(); return 길이; }
}''', encoding='utf-8')
    subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(указател_стойност), str(경계),
                    str(Позиция / 'ИЗТОЧНИК/мрежа_стек.java'), str(Позиция / '시험/패킷시험.java')], check=True)
    subprocess.run(['java', '-cp', str(указател_стойност), '패킷시험'], check=True, timeout=10)

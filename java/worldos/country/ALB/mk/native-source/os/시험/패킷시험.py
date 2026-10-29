#!/usr/bin/env python3
from pathlib import Path
import subprocess
import tempfile

Позиција = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='jkoros-packet-test-') as 임시:
    Именик_VALUE = Path(임시)
    경계 = Именик_VALUE / '시험장치.java'
    경계.write_text('''
class уред_VALUE { static int 시각; static int 밀리초() { return 시각++; } static void 잠시양보() {} }
class СМС_Терминал { static void Запиши(String VALUE) {} static void 수쓰기(int VALUE) {} }
class Мрежа_двигател {
    static int 입출력기준주소 = 1, пренесува_COUNT, 수신수;
    static int[] уред_адреса = {0x52,0x54,0,0x12,0x34,0x56}, неодамна_VALUE;
    static int 받기(int[] податоци) { return 0; }
    static int испрати(int[] податоци, int должина_VALUE) { неодамна_VALUE = податоци.clone(); return должина_VALUE; }
}''', encoding='utf-8')
    subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(Именик_VALUE), str(경계),
                    str(Позиција / 'ИЗВОР/Мрежа_Купче.java'), str(Позиција / '시험/패킷시험.java')], check=True)
    subprocess.run(['java', '-cp', str(Именик_VALUE), '패킷시험'], check=True, timeout=10)

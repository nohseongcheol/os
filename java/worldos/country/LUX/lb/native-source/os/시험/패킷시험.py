#!/usr/bin/env python3
from pathlib import Path
import subprocess
import tempfile

positionéieren = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='jkoros-packet-test-') as 임시:
    Verzeechnes_VALUE = Path(임시)
    경계 = Verzeechnes_VALUE / '시험장치.java'
    경계.write_text('''
class Mobil_VALUE { static int 시각; static int 밀리초() { return 시각++; } static void 잠시양보() {} }
class SMS_Terminal { static void schreiwen(String VALUE) {} static void 수쓰기(int VALUE) {} }
class Reseau_Driver {
    static int 입출력기준주소 = 1, 송신수, 수신수;
    static int[] Mobil_Adress = {0x52,0x54,0,0x12,0x34,0x56}, rezent_VALUE;
    static int 받기(int[] Daten) { return 0; }
    static int mailen(int[] Daten, int Längt_VALUE) { rezent_VALUE = Daten.clone(); return Längt_VALUE; }
}''', encoding='utf-8')
    subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(Verzeechnes_VALUE), str(경계),
                    str(positionéieren / 'Quell/Reseau_Stapel.java'), str(positionéieren / '시험/패킷시험.java')], check=True)
    subprocess.run(['java', '-cp', str(Verzeechnes_VALUE), '패킷시험'], check=True, timeout=10)

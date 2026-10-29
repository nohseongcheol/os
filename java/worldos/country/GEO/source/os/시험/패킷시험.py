#!/usr/bin/env python3
from pathlib import Path
import subprocess
import tempfile

პოზიცია = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='jkoros-packet-test-') as 임시:
    საქაღალდე_მნიშვნელობა = Path(임시)
    경계 = საქაღალდე_მნიშვნელობა / '시험장치.java'
    경계.write_text('''
class მობილური_მნიშვნელობა { static int 시각; static int 밀리초() { return 시각++; } static void 잠시양보() {} }
class ტექსტი_ტერმინალი { static void ჩაწერა(String მნიშვნელობა) {} static void 수쓰기(int მნიშვნელობა) {} }
class ქსელი_დრაივერი {
    static int 입출력기준주소 = 1, 송신수, 수신수;
    static int[] მობილური_მისამართი = {0x52,0x54,0,0x12,0x34,0x56}, ბოლოდროინდელი_მნიშვნელობა;
    static int 받기(int[] მონაცემები) { return 0; }
    static int გაგზავნა(int[] მონაცემები, int სიგრძე_მნიშვნელობა) { ბოლოდროინდელი_მნიშვნელობა = მონაცემები.clone(); return სიგრძე_მნიშვნელობა; }
}''', encoding='utf-8')
    subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(საქაღალდე_მნიშვნელობა), str(경계),
                    str(პოზიცია / 'წყარო/ქსელი_დასტა.java'), str(პოზიცია / '시험/패킷시험.java')], check=True)
    subprocess.run(['java', '-cp', str(საქაღალდე_მნიშვნელობა), '패킷시험'], check=True, timeout=10)

#!/usr/bin/env python3
from pathlib import Path
import subprocess
import tempfile

위치 = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='jkoros-packet-test-') as 임시:
    mooftordu_njaru = Path(임시)
    경계 = mooftordu_njaru / '시험장치.java'
    경계.write_text('''
class kaɓirgal_njaru { static int 시각; static int 밀리초() { return 시각++; } static void 잠시양보() {} }
class 문자단말 { static void winndude(String njaru) {} static void 수쓰기(int njaru) {} }
class laylaytol_pilot {
    static int 입출력기준주소 = 1, 송신수, 수신수;
    static int[] kaɓirgal_ñiiɓirde = {0x52,0x54,0,0x12,0x34,0x56}, 최근;
    static int 받기(int[] keɓe) { return 0; }
    static int neldude(int[] keɓe, int njuuteendi_njaru) { 최근 = keɓe.clone(); return njuuteendi_njaru; }
}''', encoding='utf-8')
    subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(mooftordu_njaru), str(경계),
                    str(위치 / 'sewnde/통신망.java'), str(위치 / '시험/패킷시험.java')], check=True)
    subprocess.run(['java', '-cp', str(mooftordu_njaru), '패킷시험'], check=True, timeout=10)

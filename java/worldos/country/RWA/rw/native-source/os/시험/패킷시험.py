#!/usr/bin/env python3
from pathlib import Path
import subprocess
import tempfile

위치 = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='jkoros-packet-test-') as 임시:
    ububiko_agaciro_e5561a2b = Path(임시)
    경계 = ububiko_agaciro_e5561a2b / '시험장치.java'
    경계.write_text('''
class igendanwa_agaciro { static int 시각; static int 밀리초() { return 시각++; } static void 잠시양보() {} }
class 문자단말 { static void kwandika(String agaciro) {} static void 수쓰기(int agaciro) {} }
class Urusobemiyoboro_mukoresha {
    static int 입출력기준주소 = 1, 송신수, 수신수;
    static int[] igendanwa_aderesi = {0x52,0x54,0,0x12,0x34,0x56}, biheruka_agaciro;
    static int 받기(int[] amakurushingiro) { return 0; }
    static int kohereza(int[] amakurushingiro, int uburebure_agaciro) { biheruka_agaciro = amakurushingiro.clone(); return uburebure_agaciro; }
}''', encoding='utf-8')
    subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(ububiko_agaciro_e5561a2b), str(경계),
                    str(위치 / 'Inkomoko/Urusobemiyoboro_Ikirundo.java'), str(위치 / '시험/패킷시험.java')], check=True)
    subprocess.run(['java', '-cp', str(ububiko_agaciro_e5561a2b), '패킷시험'], check=True, timeout=10)

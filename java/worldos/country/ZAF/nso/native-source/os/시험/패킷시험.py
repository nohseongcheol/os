#!/usr/bin/env python3
from pathlib import Path
import subprocess
import tempfile

위치 = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='jkoros-packet-test-') as 임시:
    lelokelelo_boleng = Path(임시)
    경계 = lelokelelo_boleng / '시험장치.java'
    경계.write_text('''
class sedirišwa_boleng { static int 시각; static int 밀리초() { return 시각++; } static void 잠시양보() {} }
class 문자단말 { static void Ngwala(String boleng) {} static void 수쓰기(int boleng) {} }
class Netweke_teraeba {
    static int 입출력기준주소 = 1, 송신수, 수신수;
    static int[] sedirišwa_atrese = {0x52,0x54,0,0x12,0x34,0x56}, ya_bjale_boleng;
    static int 받기(int[] data) { return 0; }
    static int Romela(int[] data, int botelele_boleng) { ya_bjale_boleng = data.clone(); return botelele_boleng; }
}''', encoding='utf-8')
    subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(lelokelelo_boleng), str(경계),
                    str(위치 / 'mohlodi/Netweke_kgoboko.java'), str(위치 / '시험/패킷시험.java')], check=True)
    subprocess.run(['java', '-cp', str(lelokelelo_boleng), '패킷시험'], check=True, timeout=10)

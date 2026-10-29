#!/usr/bin/env python3
from pathlib import Path
import subprocess
import tempfile

위치 = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='jkoros-packet-test-') as 임시:
    àkójọpọ̀_fáìlì_iye = Path(임시)
    경계 = àkójọpọ̀_fáìlì_iye / '시험장치.java'
    경계.write_text('''
class ohun_èlò_iye { static int 시각; static int 밀리초() { return 시각++; } static void 잠시양보() {} }
class 문자단말 { static void Kọ(String iye) {} static void 수쓰기(int iye) {} }
class Alásopọ̀_adarí_aláìrídìmú {
    static int 입출력기준주소 = 1, 송신수, 수신수;
    static int[] ohun_èlò_àdírẹ́ẹ̀sì = {0x52,0x54,0,0x12,0x34,0x56}, Àìpẹ́_iye;
    static int 받기(int[] détà) { return 0; }
    static int í_meèlì(int[] détà, int gígùn_iye) { Àìpẹ́_iye = détà.clone(); return gígùn_iye; }
}''', encoding='utf-8')
    subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(àkójọpọ̀_fáìlì_iye), str(경계),
                    str(위치 / 'orísun/Alásopọ̀_kójọ.java'), str(위치 / '시험/패킷시험.java')], check=True)
    subprocess.run(['java', '-cp', str(àkójọpọ̀_fáìlì_iye), '패킷시험'], check=True, timeout=10)

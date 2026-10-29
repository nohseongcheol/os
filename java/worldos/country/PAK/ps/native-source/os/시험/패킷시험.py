#!/usr/bin/env python3
from pathlib import Path
import subprocess
import tempfile

ځای = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='jkoros-packet-test-') as 임시:
    نوملړ_ارزښت = Path(임시)
    경계 = نوملړ_ارزښت / '시험장치.java'
    경계.write_text('''
class وزله_ارزښت { static int 시각; static int 밀리초() { return 시각++; } static void 잠시양보() {} }
class 문자단말 { static void لوستل_2(String ارزښت) {} static void 수쓰기(int ارزښت) {} }
class جال_چلاند {
    static int 입출력기준주소 = 1, 송신수, 수신수;
    static int[] وزله_پته = {0x52,0x54,0,0x12,0x34,0x56}, 최근;
    static int 받기(int[] اومتوک) { return 0; }
    static int استول(int[] اومتوک, int اوږدوالى_ارزښت) { 최근 = اومتوک.clone(); return اوږدوالى_ارزښت; }
}''', encoding='utf-8')
    subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(نوملړ_ارزښت), str(경계),
                    str(ځای / 'سرچينه/통신망.java'), str(ځای / '시험/패킷시험.java')], check=True)
    subprocess.run(['java', '-cp', str(نوملړ_ارزښت), '패킷시험'], check=True, timeout=10)

#!/usr/bin/env python3
from pathlib import Path
import subprocess
import tempfile

위치 = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='jkoros-packet-test-') as 임시:
    Saraka_thamani = Path(임시)
    경계 = Saraka_thamani / '시험장치.java'
    경계.write_text('''
class kifaa_thamani { static int 시각; static int 밀리초() { return 시각++; } static void 잠시양보() {} }
class 문자단말 { static void andika(String thamani) {} static void 수쓰기(int thamani) {} }
class Mtandao_kiendeshaji {
    static int 입출력기준주소 = 1, 송신수, 수신수;
    static int[] kifaa_anwani = {0x52,0x54,0,0x12,0x34,0x56}, hivi_karibuni_thamani;
    static int 받기(int[] data) { return 0; }
    static int tuma(int[] data, int urefu_thamani) { hivi_karibuni_thamani = data.clone(); return urefu_thamani; }
}''', encoding='utf-8')
    subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(Saraka_thamani), str(경계),
                    str(위치 / 'chanzo/Mtandao_Mpororo.java'), str(위치 / '시험/패킷시험.java')], check=True)
    subprocess.run(['java', '-cp', str(Saraka_thamani), '패킷시험'], check=True, timeout=10)

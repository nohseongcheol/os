#!/usr/bin/env python3
from pathlib import Path
import subprocess
import tempfile

위치 = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='jkoros-packet-test-') as 임시:
    폴더 = Path(임시)
    경계 = 폴더 / '시험장치.java'
    경계.write_text('''
class 장치 { static int 시각; static int 밀리초() { return 시각++; } static void 잠시양보() {} }
class 문자단말 { static void Scribe(String 값) {} static void 수쓰기(int 값) {} }
class 망장치구동기 {
    static int 입출력기준주소 = 1, 송신수, 수신수;
    static int[] 장치주소 = {0x52,0x54,0,0x12,0x34,0x56}, 최근;
    static int 받기(int[] 자료) { return 0; }
    static int 보내기(int[] 자료, int 길이) { 최근 = 자료.clone(); return 길이; }
}''', encoding='utf-8')
    subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(폴더), str(경계),
                    str(위치 / 'Fonte/통신망.java'), str(위치 / '시험/패킷시험.java')], check=True)
    subprocess.run(['java', '-cp', str(폴더), '패킷시험'], check=True, timeout=10)

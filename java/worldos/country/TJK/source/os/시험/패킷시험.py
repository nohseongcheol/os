#!/usr/bin/env python3
from pathlib import Path
import subprocess
import tempfile

위치 = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='jkoros-packet-test-') as 임시:
    директория_қимат = Path(임시)
    경계 = директория_қимат / '시험장치.java'
    경계.write_text('''
class мобилӣ_қимат { static int 시각; static int 밀리초() { return 시각++; } static void 잠시양보() {} }
class 문자단말 { static void Навиштан(String қимат) {} static void 수쓰기(int қимат) {} }
class Шабака_драйвер {
    static int 입출력기준주소 = 1, 송신수, 수신수;
    static int[] мобилӣ_суроға = {0x52,0x54,0,0x12,0x34,0x56}, охирин_қимат;
    static int 받기(int[] иттилоот) { return 0; }
    static int фиристодан(int[] иттилоот, int дарозӣ_қимат) { охирин_қимат = иттилоот.clone(); return дарозӣ_қимат; }
}''', encoding='utf-8')
    subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(директория_қимат), str(경계),
                    str(위치 / 'манбаъ/Шабака_ҷамъ.java'), str(위치 / '시험/패킷시험.java')], check=True)
    subprocess.run(['java', '-cp', str(директория_қимат), '패킷시험'], check=True, timeout=10)

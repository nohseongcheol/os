#!/usr/bin/env python3
from pathlib import Path
import subprocess
import tempfile

កំណត់ទីតាំង = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='jkoros-packet-test-') as 임시:
    បញ្ជី_តំលៃ = Path(임시)
    경계 = បញ្ជី_តំលៃ / '시험장치.java'
    경계.write_text('''
class ឧបករណ៍_តំលៃ { static int 시각; static int 밀리초() { return 시각++; } static void 잠시양보() {} }
class អត្ថបទ_ធើមីណល { static void សរសេរ(String តំលៃ) {} static void 수쓰기(int តំលៃ) {} }
class ណិតវឺក_ដ្រាយវឺ {
    static int 입출력기준주소 = 1, 송신수, 수신수;
    static int[] ឧបករណ៍_អ៊ីម៉ែល = {0x52,0x54,0,0x12,0x34,0x56}, រីសិន_តំលៃ;
    static int 받기(int[] ទិន្នន័យ) { return 0; }
    static int ផ្ញើ(int[] ទិន្នន័យ, int ប្រវែង_តំលៃ) { រីសិន_តំលៃ = ទិន្នន័យ.clone(); return ប្រវែង_តំលៃ; }
}''', encoding='utf-8')
    subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(បញ្ជី_តំលៃ), str(경계),
                    str(កំណត់ទីតាំង / 'ប្រភព/ណិតវឺក_គរ.java'), str(កំណត់ទីតាំង / '시험/패킷시험.java')], check=True)
    subprocess.run(['java', '-cp', str(បញ្ជី_តំលៃ), '패킷시험'], check=True, timeout=10)

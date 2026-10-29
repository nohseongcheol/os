#!/usr/bin/env python3
from pathlib import Path
import subprocess
import tempfile

സ്ഥാനം = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='jkoros-packet-test-') as 임시:
    ഡയറക്ടറി_മൂല്യം = Path(임시)
    경계 = ഡയറക്ടറി_മൂല്യം / '시험장치.java'
    경계.write_text('''
class മൊബൈൽ_മൂല്യം { static int 시각; static int 밀리초() { return 시각++; } static void 잠시양보() {} }
class ലിഖിതം_ടെർമിനൽ { static void എഴുത്തു്(String മൂല്യം) {} static void 수쓰기(int മൂല്യം) {} }
class നെറ്റ്_വർക്ക്_ഡ്രൈവര് {
    static int 입출력기준주소 = 1, 송신수, 수신수;
    static int[] മൊബൈൽ_ഇമെയിൽ = {0x52,0x54,0,0x12,0x34,0x56}, സമീപകാലം_മൂല്യം;
    static int 받기(int[] ഡാറ്റാ) { return 0; }
    static int അയയ്ക്കുക(int[] ഡാറ്റാ, int ദൈര്_ഘ്യം_മൂല്യം) { സമീപകാലം_മൂല്യം = ഡാറ്റാ.clone(); return ദൈര്_ഘ്യം_മൂല്യം; }
}''', encoding='utf-8')
    subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(ഡയറക്ടറി_മൂല്യം), str(경계),
                    str(സ്ഥാനം / 'ഉറവിടം/നെറ്റ്_വർക്ക്_സ്റ്റാക്ക്_ചെയ്യുക.java'), str(സ്ഥാനം / '시험/패킷시험.java')], check=True)
    subprocess.run(['java', '-cp', str(ഡയറക്ടറി_മൂല്യം), '패킷시험'], check=True, timeout=10)

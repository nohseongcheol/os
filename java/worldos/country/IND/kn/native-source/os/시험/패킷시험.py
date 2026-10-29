#!/usr/bin/env python3
from pathlib import Path
import subprocess
import tempfile

ಸ್ಥಾನ = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='jkoros-packet-test-') as 임시:
    ಡೈರೆಕ್ಟರಿ_ಮೌಲ್ಯ = Path(임시)
    경계 = ಡೈರೆಕ್ಟರಿ_ಮೌಲ್ಯ / '시험장치.java'
    경계.write_text('''
class ಸಾಧನ_ಮೌಲ್ಯ { static int 시각; static int 밀리초() { return 시각++; } static void 잠시양보() {} }
class ಪಠ್ಯ_ಟರ್ಮಿನಲ್ { static void ಬರೆ(String ಮೌಲ್ಯ) {} static void 수쓰기(int ಮೌಲ್ಯ) {} }
class ನೆಟ್_ವರ್ಕ್_ಡ್ರೈವರ್ {
    static int 입출력기준주소 = 1, 송신수, 수신수;
    static int[] ಸಾಧನ_ಇಮೇಲ್ = {0x52,0x54,0,0x12,0x34,0x56}, ಇತ್ತೀಚಿನ_ಮೌಲ್ಯ;
    static int 받기(int[] ಡೇಟಾ) { return 0; }
    static int ಕಳುಹಿಸಿ(int[] ಡೇಟಾ, int ಉದ್ದ_ಮೌಲ್ಯ) { ಇತ್ತೀಚಿನ_ಮೌಲ್ಯ = ಡೇಟಾ.clone(); return ಉದ್ದ_ಮೌಲ್ಯ; }
}''', encoding='utf-8')
    subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(ಡೈರೆಕ್ಟರಿ_ಮೌಲ್ಯ), str(경계),
                    str(ಸ್ಥಾನ / 'ಮೂಲ/ನೆಟ್_ವರ್ಕ್_ಸ್ಟ್ಯಾಕ್.java'), str(ಸ್ಥಾನ / '시험/패킷시험.java')], check=True)
    subprocess.run(['java', '-cp', str(ಡೈರೆಕ್ಟರಿ_ಮೌಲ್ಯ), '패킷시험'], check=True, timeout=10)

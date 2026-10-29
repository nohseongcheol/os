#!/usr/bin/env python3
from pathlib import Path
import subprocess
import tempfile

स्थिती = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='jkoros-packet-test-') as 임시:
    नामावळ_मोल = Path(임시)
    경계 = नामावळ_मोल / '시험장치.java'
    경계.write_text('''
class मोबायल_मोल { static int 시각; static int 밀리초() { return 시각++; } static void 잠시양보() {} }
class SMS_टर्मिनल { static void बरोवचें(String मोल) {} static void 수쓰기(int मोल) {} }
class नॅटवर्क_ड्रायव्हर {
    static int 입출력기준주소 = 1, 송신수, 수신수;
    static int[] मोबायल_नामो = {0x52,0x54,0,0x12,0x34,0x56}, हालीं_मोल;
    static int 받기(int[] डेटा) { return 0; }
    static int धाडचें(int[] डेटा, int लांबाय_मोल) { हालीं_मोल = डेटा.clone(); return लांबाय_मोल; }
}''', encoding='utf-8')
    subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(नामावळ_मोल), str(경계),
                    str(स्थिती / 'स्त्रोत/नॅटवर्क_स्टॅक.java'), str(स्थिती / '시험/패킷시험.java')], check=True)
    subprocess.run(['java', '-cp', str(नामावळ_मोल), '패킷시험'], check=True, timeout=10)

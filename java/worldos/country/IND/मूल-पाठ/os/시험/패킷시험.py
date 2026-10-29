#!/usr/bin/env python3
from pathlib import Path
import subprocess
import tempfile

स्थान = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='jkoros-packet-test-') as 임시:
    डायरेक्टरी_मान = Path(임시)
    경계 = डायरेक्टरी_मान / '시험장치.java'
    경계.write_text('''
class उपकरण_मान { static int 시각; static int 밀리초() { return 시각++; } static void 잠시양보() {} }
class पाठ_टर्मिनल { static void लिखें(String मान) {} static void 수쓰기(int मान) {} }
class नेटवर्क_डिवाइस_ड्राइवर {
    static int 입출력기준주소 = 1, 송신수, 수신수;
    static int[] उपकरण_पता = {0x52,0x54,0,0x12,0x34,0x56}, हाल_ही_का_मान;
    static int 받기(int[] आँकड़े) { return 0; }
    static int भेजें(int[] आँकड़े, int 길이) { हाल_ही_का_मान = आँकड़े.clone(); return 길이; }
}''', encoding='utf-8')
    subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(डायरेक्टरी_मान), str(경계),
                    str(स्थान / 'स्रोत/नेटवर्क_स्टैक.java'), str(स्थान / '시험/패킷시험.java')], check=True)
    subprocess.run(['java', '-cp', str(डायरेक्टरी_मान), '패킷시험'], check=True, timeout=10)

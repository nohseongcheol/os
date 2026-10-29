#!/usr/bin/env python3
from pathlib import Path
import subprocess
import tempfile

स्थिति = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='jkoros-packet-test-') as 임시:
    डाइरेक्टरी_मान = Path(임시)
    경계 = डाइरेक्टरी_मान / '시험장치.java'
    경계.write_text('''
class मोबाइल_मान { static int 시각; static int 밀리초() { return 시각++; } static void 잠시양보() {} }
class पाठ_टर्मिनल { static void लेख्नुहोस्(String मान) {} static void 수쓰기(int मान) {} }
class सञ्जाल_चालक {
    static int 입출력기준주소 = 1, 송신수, 수신수;
    static int[] मोबाइल_ठेगाना = {0x52,0x54,0,0x12,0x34,0x56}, हालको_मान;
    static int 받기(int[] लगत) { return 0; }
    static int पठाउनुहोस्(int[] लगत, int लम्बाइ_मान) { हालको_मान = लगत.clone(); return लम्बाइ_मान; }
}''', encoding='utf-8')
    subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(डाइरेक्टरी_मान), str(경계),
                    str(स्थिति / 'स्रोत/सञ्जाल_चाङ.java'), str(स्थिति / '시험/패킷시험.java')], check=True)
    subprocess.run(['java', '-cp', str(डाइरेक्टरी_मान), '패킷시험'], check=True, timeout=10)

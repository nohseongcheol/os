#!/usr/bin/env python3
from pathlib import Path
import subprocess
import tempfile

অৱস্থান = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='jkoros-packet-test-') as 임시:
    ডাইৰেক্টৰী_মান = Path(임시)
    경계 = ডাইৰেক্টৰী_মান / '시험장치.java'
    경계.write_text('''
class চেলফোন_মান { static int 시각; static int 밀리초() { return 시각++; } static void 잠시양보() {} }
class পাঠ_টাৰ্মিনেল { static void লিখা(String মান) {} static void 수쓰기(int মান) {} }
class নেটৱৰ্ক_ড্ৰাইভাৰ {
    static int 입출력기준주소 = 1, 송신수, 수신수;
    static int[] চেলফোন_ঠিকনা = {0x52,0x54,0,0x12,0x34,0x56}, শেহতীয়া_মান;
    static int 받기(int[] ডাটা) { return 0; }
    static int ই_মেইল_কৰক(int[] ডাটা, int দৈর্ঘ্য_মান) { শেহতীয়া_মান = ডাটা.clone(); return দৈর্ঘ্য_মান; }
}''', encoding='utf-8')
    subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(ডাইৰেক্টৰী_মান), str(경계),
                    str(অৱস্থান / 'উৎস/নেটৱৰ্ক_ষ্টেক.java'), str(অৱস্থান / '시험/패킷시험.java')], check=True)
    subprocess.run(['java', '-cp', str(ডাইৰেক্টৰী_মান), '패킷시험'], check=True, timeout=10)

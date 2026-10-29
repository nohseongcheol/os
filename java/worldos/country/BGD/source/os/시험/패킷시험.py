#!/usr/bin/env python3
from pathlib import Path
import subprocess
import tempfile

অবস্থান = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='jkoros-packet-test-') as 임시:
    ডিরেক্টরি_মান = Path(임시)
    경계 = ডিরেক্টরি_মান / '시험장치.java'
    경계.write_text('''
class ডিভাইস_মান { static int 시각; static int 밀리초() { return 시각++; } static void 잠시양보() {} }
class পাঠ_টার্মিনাল { static void লেখা(String মান) {} static void 수쓰기(int মান) {} }
class নেটওয়ার্ক_ড্রাইভার {
    static int 입출력기준주소 = 1, 송신수, 수신수;
    static int[] ডিভাইস_ইমেইল = {0x52,0x54,0,0x12,0x34,0x56}, সাম্প্রতিক_মান;
    static int 받기(int[] ডাটা) { return 0; }
    static int পাঠান(int[] ডাটা, int দৈর্ঘ্য_মান) { সাম্প্রতিক_মান = ডাটা.clone(); return দৈর্ঘ্য_মান; }
}''', encoding='utf-8')
    subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(ডিরেক্টরি_মান), str(경계),
                    str(অবস্থান / 'উৎস_নথি/নেটওয়ার্ক_গাদা.java'), str(অবস্থান / '시험/패킷시험.java')], check=True)
    subprocess.run(['java', '-cp', str(ডিরেক্টরি_মান), '패킷시험'], check=True, timeout=10)

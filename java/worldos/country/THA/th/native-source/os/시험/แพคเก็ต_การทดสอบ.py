#!/usr/bin/env python3
from pathlib import Path
import subprocess
import tempfile

ตําแหน่ง = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='jkoros-packet-test-') as 임시:
    ไดเรกทอรี_ค่า = Path(임시)
    경계 = ไดเรกทอรี_ค่า / '시험장치.java'
    경계.write_text('''
class อุปกรณ์_ค่า { static int ประทับเวลา_ค่า; static int 밀리초() { return ประทับเวลา_ค่า++; } static void 잠시양보() {} }
class ข้อความ_เทอร์มินัล { static void เขียน(String ค่า) {} static void 수쓰기(int ค่า) {} }
class เครือข่าย_โปรแกรมควบคุม {
    static int 입출력기준주소 = 1, 송신수, 수신수;
    static int[] อุปกรณ์_อีเมล = {0x52,0x54,0,0x12,0x34,0x56}, ล่าสุด_ค่า;
    static int รับ(int[] ข้อมูล) { return 0; }
    static int ส่ง(int[] ข้อมูล, int 길이) { ล่าสุด_ค่า = ข้อมูล.clone(); return 길이; }
}''', encoding='utf-8')
    subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(ไดเรกทอรี_ค่า), str(경계),
                    str(ตําแหน่ง / 'รหัสต้นฉบับ/เครือข่าย_สแตก.java'), str(ตําแหน่ง / '시험/แพคเก็ต_การทดสอบ.java')], check=True)
    subprocess.run(['java', '-cp', str(ไดเรกทอรี_ค่า), 'แพคเก็ต_การทดสอบ'], check=True, timeout=10)

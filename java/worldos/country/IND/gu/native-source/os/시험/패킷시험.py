#!/usr/bin/env python3
from pathlib import Path
import subprocess
import tempfile

સ્થાન = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='jkoros-packet-test-') as 임시:
    નિર્દેશિકા_મૂલ્ય = Path(임시)
    경계 = નિર્દેશિકા_મૂલ્ય / '시험장치.java'
    경계.write_text('''
class ડિવાઇસ_મૂલ્ય { static int 시각; static int 밀리초() { return 시각++; } static void 잠시양보() {} }
class પાઠ_ટર્મિનલ { static void લખો(String મૂલ્ય) {} static void 수쓰기(int મૂલ્ય) {} }
class નેટવર્ક_ડ્રાઇવર {
    static int 입출력기준주소 = 1, 송신수, 수신수;
    static int[] ડિવાઇસ_સરનામું = {0x52,0x54,0,0x12,0x34,0x56}, તાજેતરનું_મૂલ્ય;
    static int 받기(int[] ડેટા) { return 0; }
    static int મોકલો(int[] ડેટા, int લંબાઈ_મૂલ્ય) { તાજેતરનું_મૂલ્ય = ડેટા.clone(); return લંબાઈ_મૂલ્ય; }
}''', encoding='utf-8')
    subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(નિર્દેશિકા_મૂલ્ય), str(경계),
                    str(સ્થાન / 'સ્રોત/નેટવર્ક_સ્ટેક.java'), str(સ્થાન / '시험/패킷시험.java')], check=True)
    subprocess.run(['java', '-cp', str(નિર્દેશિકા_મૂલ્ય), '패킷시험'], check=True, timeout=10)

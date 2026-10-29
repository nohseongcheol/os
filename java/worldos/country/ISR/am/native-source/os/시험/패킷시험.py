#!/usr/bin/env python3
from pathlib import Path
import subprocess
import tempfile

አካባቢ = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='jkoros-packet-test-') as 임시:
    ማውጫ_እሴት = Path(임시)
    경계 = ማውጫ_እሴት / '시험장치.java'
    경계.write_text('''
class መሳሪያ_እሴት { static int 시각; static int 밀리초() { return 시각++; } static void 잠시양보() {} }
class ጽሁፍ_ተርሚናል { static void መጻፊያ(String እሴት) {} static void 수쓰기(int እሴት) {} }
class መረብ_ነጂ {
    static int 입출력기준주소 = 1, 송신수, 수신수;
    static int[] መሳሪያ_አድራሻ = {0x52,0x54,0,0x12,0x34,0x56}, የቅርብ_ጊዜ_እሴት;
    static int 받기(int[] ውሂብ) { return 0; }
    static int ላክ(int[] ውሂብ, int ርዝመት_እሴት) { የቅርብ_ጊዜ_እሴት = ውሂብ.clone(); return ርዝመት_እሴት; }
}''', encoding='utf-8')
    subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(ማውጫ_እሴት), str(경계),
                    str(አካባቢ / 'ምንጭ/መረብ_ክምር.java'), str(አካባቢ / '시험/패킷시험.java')], check=True)
    subprocess.run(['java', '-cp', str(ማውጫ_እሴት), '패킷시험'], check=True, timeout=10)

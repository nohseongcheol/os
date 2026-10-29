#!/usr/bin/env python3
from pathlib import Path
import subprocess
import tempfile

위치 = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='jkoros-packet-test-') as 임시:
    ڕێبەرنامە_نرخ = Path(임시)
    경계 = ڕێبەرنامە_نرخ / '시험장치.java'
    경계.write_text('''
class ئامێر_نرخ { static int 시각; static int 밀리초() { return 시각++; } static void 잠시양보() {} }
class 문자단말 { static void ڕایت_کردن(String نرخ) {} static void 수쓰기(int نرخ) {} }
class تۆڕ_درایڤێر {
    static int 입출력기준주소 = 1, 송신수, 수신수;
    static int[] ئامێر_ناونیشان = {0x52,0x54,0,0x12,0x34,0x56}, ئەم_دواییانە_نرخ;
    static int 받기(int[] دەیتا) { return 0; }
    static int ناردن(int[] دەیتا, int درێژی_نرخ) { ئەم_دواییانە_نرخ = دەیتا.clone(); return درێژی_نرخ; }
}''', encoding='utf-8')
    subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(ڕێبەرنامە_نرخ), str(경계),
                    str(위치 / 'ژێدەر/تۆڕ_ستاك.java'), str(위치 / '시험/패킷시험.java')], check=True)
    subprocess.run(['java', '-cp', str(ڕێبەرنامە_نرخ), '패킷시험'], check=True, timeout=10)

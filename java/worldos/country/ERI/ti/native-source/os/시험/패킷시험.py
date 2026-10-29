#!/usr/bin/env python3
from pathlib import Path
import subprocess
import tempfile

위치 = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='jkoros-packet-test-') as 임시:
    ሓባሪ_ማህደር_ዋጋ = Path(임시)
    경계 = ሓባሪ_ማህደር_ዋጋ / '시험장치.java'
    경계.write_text('''
class መሳርሒ_ዋጋ { static int 시각; static int 밀리초() { return 시각++; } static void 잠시양보() {} }
class 문자단말 { static void ጸሓፍ(String ዋጋ) {} static void 수쓰기(int ዋጋ) {} }
class ማሕበራዊ_ኔትወርክ_መወሃዲ {
    static int 입출력기준주소 = 1, 송신수, 수신수;
    static int[] መሳርሒ_ኣድራሻ = {0x52,0x54,0,0x12,0x34,0x56}, ናይ_ቀረባ_ግዜ_ዋጋ;
    static int 받기(int[] ሓበሬታ) { return 0; }
    static int ለኣኽ(int[] ሓበሬታ, int ንውሓት_ዋጋ) { ናይ_ቀረባ_ግዜ_ዋጋ = ሓበሬታ.clone(); return ንውሓት_ዋጋ; }
}''', encoding='utf-8')
    subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(ሓባሪ_ማህደር_ዋጋ), str(경계),
                    str(위치 / 'ምንጪ/ማሕበራዊ_ኔትወርክ_ድርደራ.java'), str(위치 / '시험/패킷시험.java')], check=True)
    subprocess.run(['java', '-cp', str(ሓባሪ_ማህደር_ዋጋ), '패킷시험'], check=True, timeout=10)

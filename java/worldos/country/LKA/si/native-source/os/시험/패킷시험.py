#!/usr/bin/env python3
from pathlib import Path
import subprocess
import tempfile

පිහිටීම = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='jkoros-packet-test-') as 임시:
    නාමාවලිය_අගය = Path(임시)
    경계 = නාමාවලිය_අගය / '시험장치.java'
    경계.write_text('''
class ජංගම_අගය { static int 시각; static int 밀리초() { return 시각++; } static void 잠시양보() {} }
class 문자단말 { static void ලිවීම(String අගය) {} static void 수쓰기(int අගය) {} }
class ජාලය_ධාවකය {
    static int 입출력기준주소 = 1, 송신수, 수신수;
    static int[] ජංගම_යොමුව = {0x52,0x54,0,0x12,0x34,0x56}, මෑතකාලීන_අගය;
    static int 받기(int[] දත්ත) { return 0; }
    static int ඊමේල්(int[] දත්ත, int දිග_අගය) { මෑතකාලීන_අගය = දත්ත.clone(); return දිග_අගය; }
}''', encoding='utf-8')
    subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(නාමාවලිය_අගය), str(경계),
                    str(පිහිටීම / 'මූලය/ජාලය_කැටිය.java'), str(පිහිටීම / '시험/패킷시험.java')], check=True)
    subprocess.run(['java', '-cp', str(නාමාවලිය_අගය), '패킷시험'], check=True, timeout=10)

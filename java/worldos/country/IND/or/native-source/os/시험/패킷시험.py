#!/usr/bin/env python3
from pathlib import Path
import subprocess
import tempfile

ଅବସ୍ଥାନ = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='jkoros-packet-test-') as 임시:
    ଡିରେକ୍ଟୋରୀ_ମୂଲ୍ୟ = Path(임시)
    경계 = ଡିରେକ୍ଟୋରୀ_ମୂଲ୍ୟ / '시험장치.java'
    경계.write_text('''
class ଡିଭାଇସ_ମୂଲ୍ୟ { static int 시각; static int 밀리초() { return 시각++; } static void 잠시양보() {} }
class ପାଠ_ଟର୍ମିନାଲ୍ { static void ଲେଖନ୍ତୁ(String ମୂଲ୍ୟ) {} static void 수쓰기(int ମୂଲ୍ୟ) {} }
class ନେଟ୍_ୱାର୍କ୍_ଡ୍ରାଇଭର୍ {
    static int 입출력기준주소 = 1, 송신수, 수신수;
    static int[] ଡିଭାଇସ_ଠିକଣା = {0x52,0x54,0,0x12,0x34,0x56}, ବର୍ତ୍ତମାନ_ମୂଲ୍ୟ;
    static int 받기(int[] ଡାଟା) { return 0; }
    static int ପଠାନ୍ତୁ(int[] ଡାଟା, int ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ) { ବର୍ତ୍ତମାନ_ମୂଲ୍ୟ = ଡାଟା.clone(); return ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ; }
}''', encoding='utf-8')
    subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(ଡିରେକ୍ଟୋରୀ_ମୂଲ୍ୟ), str(경계),
                    str(ଅବସ୍ଥାନ / 'ଉତ୍ସ/ନେଟ୍_ୱାର୍କ୍_ଗଦା.java'), str(ଅବସ୍ଥାନ / '시험/패킷시험.java')], check=True)
    subprocess.run(['java', '-cp', str(ଡିରେକ୍ଟୋରୀ_ମୂଲ୍ୟ), '패킷시험'], check=True, timeout=10)

#!/usr/bin/env python3
from pathlib import Path
import subprocess
import tempfile

இடம் = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='jkoros-packet-test-') as 임시:
    கோப்பகம்_மதிப்பு = Path(임시)
    경계 = கோப்பகம்_மதிப்பு / '시험장치.java'
    경계.write_text('''
class சாதனம்_மதிப்பு { static int 시각; static int 밀리초() { return 시각++; } static void 잠시양보() {} }
class உரை_முனையம் { static void எழுது(String மதிப்பு) {} static void 수쓰기(int மதிப்பு) {} }
class பிணையம்_இயக்குநிரல் {
    static int 입출력기준주소 = 1, 송신수, 수신수;
    static int[] சாதனம்_முகவரி = {0x52,0x54,0,0x12,0x34,0x56}, சமீபத்தியவை_மதிப்பு;
    static int 받기(int[] தரவு) { return 0; }
    static int அனுப்பு(int[] தரவு, int நீளம்_மதிப்பு) { சமீபத்தியவை_மதிப்பு = தரவு.clone(); return நீளம்_மதிப்பு; }
}''', encoding='utf-8')
    subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(கோப்பகம்_மதிப்பு), str(경계),
                    str(இடம் / 'மூலக்_கோப்பு/பிணையம்_அடுக்கு_49fba3da.java'), str(இடம் / '시험/패킷시험.java')], check=True)
    subprocess.run(['java', '-cp', str(கோப்பகம்_மதிப்பு), '패킷시험'], check=True, timeout=10)

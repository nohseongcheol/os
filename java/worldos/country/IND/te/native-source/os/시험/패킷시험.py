#!/usr/bin/env python3
from pathlib import Path
import subprocess
import tempfile

స్థానము = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='jkoros-packet-test-') as 임시:
    సంచయని_మూల్యం = Path(임시)
    경계 = సంచయని_మూల్యం / '시험장치.java'
    경계.write_text('''
class పరికరం_మూల్యం { static int 시각; static int 밀리초() { return 시각++; } static void 잠시양보() {} }
class పాఠం_టెర్మినల్ { static void వ్రాయుము(String మూల్యం) {} static void 수쓰기(int మూల్యం) {} }
class నెట్_వర్క్_డ్రైవర్ {
    static int 입출력기준주소 = 1, 송신수, 수신수;
    static int[] పరికరం_ఇమెయిల్ = {0x52,0x54,0,0x12,0x34,0x56}, ఇటీవల_మూల్యం;
    static int 받기(int[] డేటా) { return 0; }
    static int పంపు(int[] డేటా, int పొడవు_మూల్యం) { ఇటీవల_మూల్యం = డేటా.clone(); return పొడవు_మూల్యం; }
}''', encoding='utf-8')
    subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(సంచయని_మూల్యం), str(경계),
                    str(స్థానము / 'వనరు/నెట్_వర్క్_దొంతర.java'), str(స్థానము / '시험/패킷시험.java')], check=True)
    subprocess.run(['java', '-cp', str(సంచయని_మూల్యం), '패킷시험'], check=True, timeout=10)

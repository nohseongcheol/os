#!/usr/bin/env python3
from pathlib import Path
import subprocess
import tempfile

위치 = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='jkoros-packet-test-') as 임시:
    ᎠᏓᏎᎮᎯ_ᏫᎦᎷᎯᏍᏗ_ᏧᎬᏩᎶᏗᏯ = Path(임시)
    경계 = ᎠᏓᏎᎮᎯ_ᏫᎦᎷᎯᏍᏗ_ᏧᎬᏩᎶᏗᏯ / '시험장치.java'
    경계.write_text('''
class ᎠᏂᎩᏍᎩ_ᏧᎬᏩᎶᏗᏯ { static int 시각; static int 밀리초() { return 시각++; } static void 잠시양보() {} }
class 문자단말 { static void ᎪᏪᎶᏗ(String ᏧᎬᏩᎶᏗᏯ) {} static void 수쓰기(int ᏧᎬᏩᎶᏗᏯ) {} }
class ᏧᎾᏚᏓᎵ_ᎠᏠᏓᎪᎵᏰᏙᏗ {
    static int 입출력기준주소 = 1, 송신수, 수신수;
    static int[] ᎠᏂᎩᏍᎩ_ᎪᏪᎵ_ᏫᏗᎦᏅᏗ = {0x52,0x54,0,0x12,0x34,0x56}, 최근;
    static int 받기(int[] ᎦᏟᏌᏅᎯ) { return 0; }
    static int ᏫᎦᏅᏗ(int[] ᎦᏟᏌᏅᎯ, int ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ) { 최근 = ᎦᏟᏌᏅᎯ.clone(); return ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ; }
}''', encoding='utf-8')
    subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(ᎠᏓᏎᎮᎯ_ᏫᎦᎷᎯᏍᏗ_ᏧᎬᏩᎶᏗᏯ), str(경계),
                    str(위치 / 'ᎦᏟᏌᏅᎯ_0201f362/통신망.java'), str(위치 / '시험/패킷시험.java')], check=True)
    subprocess.run(['java', '-cp', str(ᎠᏓᏎᎮᎯ_ᏫᎦᎷᎯᏍᏗ_ᏧᎬᏩᎶᏗᏯ), '패킷시험'], check=True, timeout=10)

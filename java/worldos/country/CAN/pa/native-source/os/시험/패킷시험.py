#!/usr/bin/env python3
from pathlib import Path
import subprocess
import tempfile

ਸਥਿਤੀ = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='jkoros-packet-test-') as 임시:
    ਨਿਰਦੇਸ਼ਕ_ਕੀਮਤ = Path(임시)
    경계 = ਨਿਰਦੇਸ਼ਕ_ਕੀਮਤ / '시험장치.java'
    경계.write_text('''
class ਤਜਵੀਜ_ਕੀਮਤ { static int 시각; static int 밀리초() { return 시각++; } static void 잠시양보() {} }
class ਪਾਠ_ਟਰਮੀਨਲ { static void ਲਿਖਣ(String ਕੀਮਤ) {} static void 수쓰기(int ਕੀਮਤ) {} }
class ਨੈਟਵਰਕ_ਚਾਲਕ {
    static int 입출력기준주소 = 1, 송신수, 수신수;
    static int[] ਤਜਵੀਜ_ਪਤਾ = {0x52,0x54,0,0x12,0x34,0x56}, ਹਾਲ_ਹੀ_ਕੀਮਤ;
    static int 받기(int[] ਸਮੱਗਰੀ) { return 0; }
    static int ਈਮੇਲ(int[] ਸਮੱਗਰੀ, int ਲੰਬਾਈ_ਕੀਮਤ) { ਹਾਲ_ਹੀ_ਕੀਮਤ = ਸਮੱਗਰੀ.clone(); return ਲੰਬਾਈ_ਕੀਮਤ; }
}''', encoding='utf-8')
    subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(ਨਿਰਦੇਸ਼ਕ_ਕੀਮਤ), str(경계),
                    str(ਸਥਿਤੀ / 'ਸਰੋਤ/ਨੈਟਵਰਕ_ਸਟੈਕ.java'), str(ਸਥਿਤੀ / '시험/패킷시험.java')], check=True)
    subprocess.run(['java', '-cp', str(ਨਿਰਦੇਸ਼ਕ_ਕੀਮਤ), '패킷시험'], check=True, timeout=10)

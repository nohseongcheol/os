#!/usr/bin/env python3
from pathlib import Path
import subprocess
import tempfile

ຈັດຕໍາແຫນ່ງ = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='jkoros-packet-test-') as 임시:
    ກຸ່ມຂໍ້ມູນ_ຄ່າ = Path(임시)
    경계 = ກຸ່ມຂໍ້ມູນ_ຄ່າ / '시험장치.java'
    경계.write_text('''
class ມືຖື_ຄ່າ { static int 시각; static int 밀리초() { return 시각++; } static void 잠시양보() {} }
class ຂໍ້ຄວາມ_ເທີມີນໍ { static void ຂຽນ(String ຄ່າ) {} static void 수쓰기(int ຄ່າ) {} }
class ເຄືອຂ່າຍ_ດຣ້າຍເວີ {
    static int 입출력기준주소 = 1, 송신수, 수신수;
    static int[] ມືຖື_ອີເມວ = {0x52,0x54,0,0x12,0x34,0x56}, ບໍ່_ດົນ_ມາ_ນີ້_ຄ່າ;
    static int 받기(int[] ຂໍ້ມູນ) { return 0; }
    static int ສົ່ງ(int[] ຂໍ້ມູນ, int ຄວາມຍາວ_ຄ່າ) { ບໍ່_ດົນ_ມາ_ນີ້_ຄ່າ = ຂໍ້ມູນ.clone(); return ຄວາມຍາວ_ຄ່າ; }
}''', encoding='utf-8')
    subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(ກຸ່ມຂໍ້ມູນ_ຄ່າ), str(경계),
                    str(ຈັດຕໍາແຫນ່ງ / 'ແຫຼ່ງທີ່ມາ/ເຄືອຂ່າຍ_ກຸ່ມບັດ.java'), str(ຈັດຕໍາແຫນ່ງ / '시험/패킷시험.java')], check=True)
    subprocess.run(['java', '-cp', str(ກຸ່ມຂໍ້ມູນ_ຄ່າ), '패킷시험'], check=True, timeout=10)

#!/usr/bin/env python3
from pathlib import Path
import subprocess
import tempfile

vịTrí = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='jkoros-packet-test-') as giáTrịTạm:
    giáTrịThưMục = Path(giáTrịTạm)
    giáTrịRanhGiới = giáTrịThưMục / '시험장치.java'
    giáTrịRanhGiới.write_text('''
class ThiếtBị { static int giáTrịDấuThờiGian; static int miliGiây() { return giáTrịDấuThờiGian++; } static void nhườngNgắn() {} }
class ĐầuCuốiVănBản { static void ghi(String giáTrị) {} static void ghiSố(int giáTrị) {} }
class TrìnhĐiềuKhiểnMạng {
    static int địaChỉCơSởVàoRa = 1, sốLượngTruyền, nhậnSốLượng;
    static int[] địaChỉThiếtBị = {0x52,0x54,0,0x12,0x34,0x56}, giáTrịGầnĐây;
    static int nhận(int[] DữLiệu) { return 0; }
    static int gửi(int[] DữLiệu, int độDài) { giáTrịGầnĐây = DữLiệu.clone(); return độDài; }
}''', encoding='utf-8')
    subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(giáTrịThưMục), str(giáTrịRanhGiới),
                    str(vịTrí / 'mãNguồn/NgănXếpMạng.java'), str(vịTrí / 'KiểmThử/ThửGóiTin.java')], check=True)
    subprocess.run(['java', '-cp', str(giáTrịThưMục), 'ThửGóiTin'], check=True, timeout=10)

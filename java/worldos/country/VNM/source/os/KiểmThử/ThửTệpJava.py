#!/usr/bin/env python3
"""게스트 작성 표준 FileStream 바이트코드를 독립 OpenJDK 실행과 대조한다."""
import json
from pathlib import Path
import re
import subprocess
import tempfile
from thửMạngNgườiDùng import MáyẢo, vịTrí
from ThửJava import giáTrịSửa, tệpKhách

def thựcThiLệnh():
    kếtQuả = {}
    mãNguồn = (vịTrí.parent / 'posix-kor/VíDụJava/FileDemo.java').read_text()
    for giáTrịLoại in ('elf', 'iso'):
        máy = MáyẢo(vịTrí / ('build/kernel.' + giáTrịLoại), giáTrịLoại, giáTrịMạng=False)
        try:
            giáTrịSửa(máy, 'FileDemo.java', mãNguồn)
            máy.lệnh('javac FileDemo.java', ['Compiled: FileDemo.class', 'Exit: 0'])
            for giáTrịLầnLặp in range(2):
                ĐầuRa = máy.lệnh('java FileDemo', ['65\r\n255\r\n66\r\n-1\r\n', 'JAVA FILE IO PASS', 'Exit: 0'])
            danhSáchMục = máy.lệnh('ls', ['java.txt  3 bytes'])
            cỡ = int(re.search(r'FileDemo.class\s+(\d+) bytes', danhSáchMục)[1])
            with tempfile.TemporaryDirectory(prefix='jkoros-stream-class-') as giáTrịTạm:
                giáTrịThưMục = Path(giáTrịTạm)
                tệpKhách(máy, 2, cỡ, giáTrịThưMục / 'FileDemo.class')
                Chủ = subprocess.check_output(['java', '-Xverify:all', '-cp', str(giáTrịThưMục), 'FileDemo'], cwd=str(giáTrịThưMục), universal_newlines=True)
                assert Chủ == '65\n255\n66\n-1\nJAVA FILE IO PASS\n', Chủ
                assert (giáTrịThưMục / 'java.txt').read_bytes() == b'A\xffB'
            giáTrịSửa(máy, 'FileDemo.java', mãNguồn.replace('output.write(65);', 'output.close(); output.write(65);'))
            máy.lệnh('javac FileDemo.java', ['Exit: 0'])
            máy.lệnh('java FileDemo', ['IOException: stream closed', 'Exit: 1'])
            giáTrịSửa(máy, 'FileDemo.java', '''import java.io.FileInputStream;
public class FileDemo {
 public static void main(String[] args) throws Exception {
  FileInputStream input = new FileInputStream("missing.dat");
 }
}''')
            máy.lệnh('javac FileDemo.java', ['Exit: 0'])
            máy.lệnh('java FileDemo', ['FileNotFoundException', 'Exit: 1'])
            máy.lệnh('run hello recovered', ['Exit: 0'])
            kếtQuả[giáTrịLoại] = máy.bảnGhiNhậtKý.decode('utf-8', 'replace')
        finally:
            máy.đóng()
        print('PASS:', giáTrịLoại, '게스트 Java Tệp sinh/thêmCuốiSựTiếpDiễn/giáTrịByte/EOF/làĐãĐóng/giáTrịSựThấtBại/OpenJDK 교차 thựcThiLệnh', flush=True)
    (vịTrí / 'build/ThửTệpJava.json').write_text(json.dumps(kếtQuả, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    thựcThiLệnh()

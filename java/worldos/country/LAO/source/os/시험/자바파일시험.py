#!/usr/bin/env python3
"""게스트 작성 표준 FileStream 바이트코드를 독립 OpenJDK 실행과 대조한다."""
import json
from pathlib import Path
import re
import subprocess
import tempfile
from 사용자통신시험 import ຈໍາລອງ_ເຄື່ອງຈັກ, ຈັດຕໍາແຫນ່ງ
from 자바시험 import ແກ້ໄຂ_ຄ່າ, ແຂກ_ຟາຍ

def ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ():
    ມາດຕະການ = {}
    ແຫຼ່ງທີ່ມາ = (ຈັດຕໍາແຫນ່ງ.parent / 'posix-kor/자바예제/FileDemo.java').read_text()
    for 종류 in ('elf', 'iso'):
        ເຄື່ອງຈັກ = ຈໍາລອງ_ເຄື່ອງຈັກ(ຈັດຕໍາແຫນ່ງ / ('build/kernel.' + 종류), 종류, ເຄືອຂ່າຍ_ຄ່າ=False)
        try:
            ແກ້ໄຂ_ຄ່າ(ເຄື່ອງຈັກ, 'FileDemo.java', ແຫຼ່ງທີ່ມາ)
            ເຄື່ອງຈັກ.ຄໍາສັ່ງ_1f12b8e2('javac FileDemo.java', ['Compiled: FileDemo.class', 'Exit: 0'])
            for ສະປຣິນ_ຄ່າ in range(2):
                출력 = ເຄື່ອງຈັກ.ຄໍາສັ່ງ_1f12b8e2('java FileDemo', ['65\r\n255\r\n66\r\n-1\r\n', 'JAVA FILE IO PASS', 'Exit: 0'])
            ເຂົ້າໃນ_ລາຍຊື່ = ເຄື່ອງຈັກ.ຄໍາສັ່ງ_1f12b8e2('ls', ['java.txt  3 bytes'])
            ຂະ_ຫນາດ = int(re.search(r'FileDemo.class\s+(\d+) bytes', ເຂົ້າໃນ_ລາຍຊື່)[1])
            with tempfile.TemporaryDirectory(prefix='jkoros-stream-class-') as 임시:
                ກຸ່ມຂໍ້ມູນ_ຄ່າ = Path(임시)
                ແຂກ_ຟາຍ(ເຄື່ອງຈັກ, 2, ຂະ_ຫນາດ, ກຸ່ມຂໍ້ມູນ_ຄ່າ / 'FileDemo.class')
                ໂຮສ = subprocess.check_output(['java', '-Xverify:all', '-cp', str(ກຸ່ມຂໍ້ມູນ_ຄ່າ), 'FileDemo'], cwd=str(ກຸ່ມຂໍ້ມູນ_ຄ່າ), universal_newlines=True)
                assert ໂຮສ == '65\n255\n66\n-1\nJAVA FILE IO PASS\n', ໂຮສ
                assert (ກຸ່ມຂໍ້ມູນ_ຄ່າ / 'java.txt').read_bytes() == b'A\xffB'
            ແກ້ໄຂ_ຄ່າ(ເຄື່ອງຈັກ, 'FileDemo.java', ແຫຼ່ງທີ່ມາ.replace('output.write(65);', 'output.close(); output.write(65);'))
            ເຄື່ອງຈັກ.ຄໍາສັ່ງ_1f12b8e2('javac FileDemo.java', ['Exit: 0'])
            ເຄື່ອງຈັກ.ຄໍາສັ່ງ_1f12b8e2('java FileDemo', ['IOException: stream closed', 'Exit: 1'])
            ແກ້ໄຂ_ຄ່າ(ເຄື່ອງຈັກ, 'FileDemo.java', '''import java.io.FileInputStream;
public class FileDemo {
 public static void main(String[] args) throws Exception {
  FileInputStream input = new FileInputStream("missing.dat");
 }
}''')
            ເຄື່ອງຈັກ.ຄໍາສັ່ງ_1f12b8e2('javac FileDemo.java', ['Exit: 0'])
            ເຄື່ອງຈັກ.ຄໍາສັ່ງ_1f12b8e2('java FileDemo', ['FileNotFoundException', 'Exit: 1'])
            ເຄື່ອງຈັກ.ຄໍາສັ່ງ_1f12b8e2('run hello recovered', ['Exit: 0'])
            ມາດຕະການ[종류] = ເຄື່ອງຈັກ.ບັນທຶກ_ແຖວ.decode('utf-8', 'replace')
        finally:
            ເຄື່ອງຈັກ.ປິດ()
        print('PASS:', 종류, '게스트 Java ຟາຍ ສ້າງ_167eff27/이어쓰기/ໄບ_ຄ່າ/EOF/닫힘/ຫຼົ້ມເຫຼວ_ຄ່າ/OpenJDK 교차 ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ', flush=True)
    (ຈັດຕໍາແຫນ່ງ / 'build/자바파일시험.json').write_text(json.dumps(ມາດຕະການ, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ()

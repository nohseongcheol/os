#!/usr/bin/env python3
"""게스트 작성 표준 FileStream 바이트코드를 독립 OpenJDK 실행과 대조한다."""
import json
from pathlib import Path
import re
import subprocess
import tempfile
from 사용자통신시험 import àfojúunúṣe_maṣíìnì, 위치
from 자바시험 import ṣàtúnṣe_iye, àlejò_fáìlì

def ṣiṣẹ́_àṣẹ():
    결과 = {}
    orísun = (위치.parent / 'posix-kor/자바예제/FileDemo.java').read_text()
    for 종류 in ('elf', 'iso'):
        maṣíìnì = àfojúunúṣe_maṣíìnì(위치 / ('build/kernel.' + 종류), 종류, Alásopọ̀_iye=False)
        try:
            ṣàtúnṣe_iye(maṣíìnì, 'FileDemo.java', orísun)
            maṣíìnì.Àṣẹ('javac FileDemo.java', ['Compiled: FileDemo.class', 'Exit: 0'])
            for àṣetúnṣe_iye in range(2):
                출력 = maṣíìnì.Àṣẹ('java FileDemo', ['65\r\n255\r\n66\r\n-1\r\n', 'JAVA FILE IO PASS', 'Exit: 0'])
            ìgbéwọlé_Àtòkọ = maṣíìnì.Àṣẹ('ls', ['java.txt  3 bytes'])
            Ìwọ̀n = int(re.search(r'FileDemo.class\s+(\d+) bytes', ìgbéwọlé_Àtòkọ)[1])
            with tempfile.TemporaryDirectory(prefix='jkoros-stream-class-') as 임시:
                àkójọpọ̀_fáìlì_iye = Path(임시)
                àlejò_fáìlì(maṣíìnì, 2, Ìwọ̀n, àkójọpọ̀_fáìlì_iye / 'FileDemo.class')
                olùpèsè = subprocess.check_output(['java', '-Xverify:all', '-cp', str(àkójọpọ̀_fáìlì_iye), 'FileDemo'], cwd=str(àkójọpọ̀_fáìlì_iye), universal_newlines=True)
                assert olùpèsè == '65\n255\n66\n-1\nJAVA FILE IO PASS\n', olùpèsè
                assert (àkójọpọ̀_fáìlì_iye / 'java.txt').read_bytes() == b'A\xffB'
            ṣàtúnṣe_iye(maṣíìnì, 'FileDemo.java', orísun.replace('output.write(65);', 'output.close(); output.write(65);'))
            maṣíìnì.Àṣẹ('javac FileDemo.java', ['Exit: 0'])
            maṣíìnì.Àṣẹ('java FileDemo', ['IOException: stream closed', 'Exit: 1'])
            ṣàtúnṣe_iye(maṣíìnì, 'FileDemo.java', '''import java.io.FileInputStream;
public class FileDemo {
 public static void main(String[] args) throws Exception {
  FileInputStream input = new FileInputStream("missing.dat");
 }
}''')
            maṣíìnì.Àṣẹ('javac FileDemo.java', ['Exit: 0'])
            maṣíìnì.Àṣẹ('java FileDemo', ['FileNotFoundException', 'Exit: 1'])
            maṣíìnì.Àṣẹ('run hello recovered', ['Exit: 0'])
            결과[종류] = maṣíìnì.àkọsílẹ̀_ìṣe_ìlà_ìbú.decode('utf-8', 'replace')
        finally:
            maṣíìnì.Ti()
        print('PASS:', 종류, '게스트 Java Fáìlì 생성/이어쓰기/báìtì_iye/EOF/닫힘/ìkùnà_iye/OpenJDK 교차 ṣiṣẹ́_àṣẹ', flush=True)
    (위치 / 'build/자바파일시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    ṣiṣẹ́_àṣẹ()

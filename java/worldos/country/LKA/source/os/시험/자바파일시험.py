#!/usr/bin/env python3
"""게스트 작성 표준 FileStream 바이트코드를 독립 OpenJDK 실행과 대조한다."""
import json
from pathlib import Path
import re
import subprocess
import tempfile
from 사용자통신시험 import අතථ්_ය_යන්ත්_රය, පිහිටීම
from 자바시험 import සකසන්න_අගය, අමුත්තා_ගොනුව

def ක්_රියාත්මක_කරන්න_විධානය():
    결과 = {}
    මූලය = (පිහිටීම.parent / 'posix-kor/자바예제/FileDemo.java').read_text()
    for 종류 in ('elf', 'iso'):
        යන්ත්_රය = අතථ්_ය_යන්ත්_රය(පිහිටීම / ('build/kernel.' + 종류), 종류, ජාලය_අගය=False)
        try:
            සකසන්න_අගය(යන්ත්_රය, 'FileDemo.java', මූලය)
            යන්ත්_රය.විධානය('javac FileDemo.java', ['Compiled: FileDemo.class', 'Exit: 0'])
            for පුනර්කරණය_අගය in range(2):
                출력 = යන්ත්_රය.විධානය('java FileDemo', ['65\r\n255\r\n66\r\n-1\r\n', 'JAVA FILE IO PASS', 'Exit: 0'])
            පිවිසුම_ලැයිස්තුව = යන්ත්_රය.විධානය('ls', ['java.txt  3 bytes'])
            ප්_රමාණය = int(re.search(r'FileDemo.class\s+(\d+) bytes', පිවිසුම_ලැයිස්තුව)[1])
            with tempfile.TemporaryDirectory(prefix='jkoros-stream-class-') as 임시:
                නාමාවලිය_අගය = Path(임시)
                අමුත්තා_ගොනුව(යන්ත්_රය, 2, ප්_රමාණය, නාමාවලිය_අගය / 'FileDemo.class')
                ධාරකය = subprocess.check_output(['java', '-Xverify:all', '-cp', str(නාමාවලිය_අගය), 'FileDemo'], cwd=str(නාමාවලිය_අගය), universal_newlines=True)
                assert ධාරකය == '65\n255\n66\n-1\nJAVA FILE IO PASS\n', ධාරකය
                assert (නාමාවලිය_අගය / 'java.txt').read_bytes() == b'A\xffB'
            සකසන්න_අගය(යන්ත්_රය, 'FileDemo.java', මූලය.replace('output.write(65);', 'output.close(); output.write(65);'))
            යන්ත්_රය.විධානය('javac FileDemo.java', ['Exit: 0'])
            යන්ත්_රය.විධානය('java FileDemo', ['IOException: stream closed', 'Exit: 1'])
            සකසන්න_අගය(යන්ත්_රය, 'FileDemo.java', '''import java.io.FileInputStream;
public class FileDemo {
 public static void main(String[] args) throws Exception {
  FileInputStream input = new FileInputStream("missing.dat");
 }
}''')
            යන්ත්_රය.විධානය('javac FileDemo.java', ['Exit: 0'])
            යන්ත්_රය.විධානය('java FileDemo', ['FileNotFoundException', 'Exit: 1'])
            යන්ත්_රය.විධානය('run hello recovered', ['Exit: 0'])
            결과[종류] = යන්ත්_රය.ලොගය_පේළිය.decode('utf-8', 'replace')
        finally:
            යන්ත්_රය.වසන්න()
        print('PASS:', 종류, '게스트 Java ගොනු 생성/이어쓰기/බයිටය_අගය/EOF/닫힘/අසමත්වීම_අගය/OpenJDK 교차 ක්_රියාත්මක_කරන්න_විධානය', flush=True)
    (පිහිටීම / 'build/자바파일시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    ක්_රියාත්මක_කරන්න_විධානය()

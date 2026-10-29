#!/usr/bin/env python3
"""게스트 작성 표준 FileStream 바이트코드를 독립 OpenJDK 실행과 대조한다."""
import json
from pathlib import Path
import re
import subprocess
import tempfile
from 사용자통신시험 import និម្មិត_ម៉ាស៊ីន, កំណត់ទីតាំង
from 자바시험 import កែសម្រួល_តំលៃ, ភ្ញៀវ_ឯកសារ

def អនុវត្ត_ពាក្យបញ្ជា():
    ការវាស់វែង = {}
    ប្រភព = (កំណត់ទីតាំង.parent / 'posix-kor/자바예제/FileDemo.java').read_text()
    for 종류 in ('elf', 'iso'):
        ម៉ាស៊ីន = និម្មិត_ម៉ាស៊ីន(កំណត់ទីតាំង / ('build/kernel.' + 종류), 종류, ណិតវឺក_តំលៃ=False)
        try:
            កែសម្រួល_តំលៃ(ម៉ាស៊ីន, 'FileDemo.java', ប្រភព)
            ម៉ាស៊ីន.ពាក្យ_បញ្ជា('javac FileDemo.java', ['Compiled: FileDemo.class', 'Exit: 0'])
            for ការធ្វើឡើងវិញ_តំលៃ in range(2):
                លទ្ធផល = ម៉ាស៊ីន.ពាក្យ_បញ្ជា('java FileDemo', ['65\r\n255\r\n66\r\n-1\r\n', 'JAVA FILE IO PASS', 'Exit: 0'])
            ការបញ្ចូល_បញ្ជី = ម៉ាស៊ីន.ពាក្យ_បញ្ជា('ls', ['java.txt  3 bytes'])
            ដាក់ទំហំ = int(re.search(r'FileDemo.class\s+(\d+) bytes', ការបញ្ចូល_បញ្ជី)[1])
            with tempfile.TemporaryDirectory(prefix='jkoros-stream-class-') as 임시:
                បញ្ជី_តំលៃ = Path(임시)
                ភ្ញៀវ_ឯកសារ(ម៉ាស៊ីន, 2, ដាក់ទំហំ, បញ្ជី_តំលៃ / 'FileDemo.class')
                ហូស = subprocess.check_output(['java', '-Xverify:all', '-cp', str(បញ្ជី_តំលៃ), 'FileDemo'], cwd=str(បញ្ជី_តំលៃ), universal_newlines=True)
                assert ហូស == '65\n255\n66\n-1\nJAVA FILE IO PASS\n', ហូស
                assert (បញ្ជី_តំលៃ / 'java.txt').read_bytes() == b'A\xffB'
            កែសម្រួល_តំលៃ(ម៉ាស៊ីន, 'FileDemo.java', ប្រភព.replace('output.write(65);', 'output.close(); output.write(65);'))
            ម៉ាស៊ីន.ពាក្យ_បញ្ជា('javac FileDemo.java', ['Exit: 0'])
            ម៉ាស៊ីន.ពាក្យ_បញ្ជា('java FileDemo', ['IOException: stream closed', 'Exit: 1'])
            កែសម្រួល_តំលៃ(ម៉ាស៊ីន, 'FileDemo.java', '''import java.io.FileInputStream;
public class FileDemo {
 public static void main(String[] args) throws Exception {
  FileInputStream input = new FileInputStream("missing.dat");
 }
}''')
            ម៉ាស៊ីន.ពាក្យ_បញ្ជា('javac FileDemo.java', ['Exit: 0'])
            ម៉ាស៊ីន.ពាក្យ_បញ្ជា('java FileDemo', ['FileNotFoundException', 'Exit: 1'])
            ម៉ាស៊ីន.ពាក្យ_បញ្ជា('run hello recovered', ['Exit: 0'])
            ការវាស់វែង[종류] = ម៉ាស៊ីន.កំណត់_ហេតុ_ថត.decode('utf-8', 'replace')
        finally:
            ម៉ាស៊ីន.បិទ()
        print('PASS:', 종류, '게스트 Java ឯកសារ បង្កើត/이어쓰기/បៃ_តំលៃ/EOF/닫힘/បរាជ័យ_តំលៃ/OpenJDK 교차 អនុវត្ត_ពាក្យបញ្ជា', flush=True)
    (កំណត់ទីតាំង / 'build/자바파일시험.json').write_text(json.dumps(ការវាស់វែង, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    អនុវត្ត_ពាក្យបញ្ជា()

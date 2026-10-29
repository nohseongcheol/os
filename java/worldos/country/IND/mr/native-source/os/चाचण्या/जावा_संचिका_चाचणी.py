#!/usr/bin/env python3
"""게스트 작성 표준 FileStream 바이트코드를 독립 OpenJDK 실행과 대조한다."""
import json
from pathlib import Path
import re
import subprocess
import tempfile
from प्रयोक्ता_संचारजाळे_चाचणी import व्हर्च्युअल_मशीन, जागा
from जावा_चाचणी import संपादन_मूल्य, अतिथी_संचिका

def आज्ञा_कार्यवाही_करा():
    मोजमाप = {}
    स्रोत = (जागा.parent / 'posix-kor/जावा_उदाहरण/FileDemo.java').read_text()
    for प्रकार_मूल्य in ('elf', 'iso'):
        मशीन = व्हर्च्युअल_मशीन(जागा / ('build/kernel.' + प्रकार_मूल्य), प्रकार_मूल्य, संचारजाळे_मूल्य=False)
        try:
            संपादन_मूल्य(मशीन, 'FileDemo.java', स्रोत)
            मशीन.आदेश('javac FileDemo.java', ['Compiled: FileDemo.class', 'Exit: 0'])
            for पुनरावृत्ती_मूल्य in range(2):
                आउटपुट = मशीन.आदेश('java FileDemo', ['65\r\n255\r\n66\r\n-1\r\n', 'JAVA FILE IO PASS', 'Exit: 0'])
            प्रविष्टी_यादी = मशीन.आदेश('ls', ['java.txt  3 bytes'])
            आकार = int(re.search(r'FileDemo.class\s+(\d+) bytes', प्रविष्टी_यादी)[1])
            with tempfile.TemporaryDirectory(prefix='jkoros-stream-class-') as तात्पुरते_मूल्य:
                निर्देशिका_मूल्य = Path(तात्पुरते_मूल्य)
                अतिथी_संचिका(मशीन, 2, आकार, निर्देशिका_मूल्य / 'FileDemo.class')
                होस्ट = subprocess.check_output(['java', '-Xverify:all', '-cp', str(निर्देशिका_मूल्य), 'FileDemo'], cwd=str(निर्देशिका_मूल्य), universal_newlines=True)
                assert होस्ट == '65\n255\n66\n-1\nJAVA FILE IO PASS\n', होस्ट
                assert (निर्देशिका_मूल्य / 'java.txt').read_bytes() == b'A\xffB'
            संपादन_मूल्य(मशीन, 'FileDemo.java', स्रोत.replace('output.write(65);', 'output.close(); output.write(65);'))
            मशीन.आदेश('javac FileDemo.java', ['Exit: 0'])
            मशीन.आदेश('java FileDemo', ['IOException: stream closed', 'Exit: 1'])
            संपादन_मूल्य(मशीन, 'FileDemo.java', '''import java.io.FileInputStream;
public class FileDemo {
 public static void main(String[] args) throws Exception {
  FileInputStream input = new FileInputStream("missing.dat");
 }
}''')
            मशीन.आदेश('javac FileDemo.java', ['Exit: 0'])
            मशीन.आदेश('java FileDemo', ['FileNotFoundException', 'Exit: 1'])
            मशीन.आदेश('run hello recovered', ['Exit: 0'])
            मोजमाप[प्रकार_मूल्य] = मशीन.लॉग_नोंद.decode('utf-8', 'replace')
        finally:
            मशीन.बंद_करा()
        print('PASS:', प्रकार_मूल्य, '게스트 Java फाइल तयार_करा/शेवटीजोडा_पुढीलक्रम/बाइट_मूल्य/EOF/आहे_बंदकेलेले/बिघाड_मूल्य/OpenJDK 교차 आज्ञा_कार्यवाही_करा', flush=True)
    (जागा / 'build/जावा_संचिका_चाचणी.json').write_text(json.dumps(मोजमाप, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    आज्ञा_कार्यवाही_करा()

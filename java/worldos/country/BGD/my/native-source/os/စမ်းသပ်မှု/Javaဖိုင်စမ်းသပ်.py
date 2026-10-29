#!/usr/bin/env python3
"""게스트 작성 표준 FileStream 바이트코드를 독립 OpenJDK 실행과 대조한다."""
import json
from pathlib import Path
import re
import subprocess
import tempfile
from သုံးစွဲဆက်သွယ်စမ်းသပ် import စက်တု, နေရာ
from Javaစမ်းသပ် import တည်းဖြတ်တန်ဖိုး, ဧည့်သည်ဖိုင်

def စက်မောင်း():
    ရလဒ် = {}
    မူရင်းကုဒ် = (နေရာ.parent / 'posix-kor/Javaဥပမာ/FileDemo.java').read_text()
    for အမျိုးအစားတန်ဖိုး in ('elf', 'iso'):
        စက် = စက်တု(နေရာ / ('build/kernel.' + အမျိုးအစားတန်ဖိုး), အမျိုးအစားတန်ဖိုး, ကွန်ရက်တန်ဖိုး=False)
        try:
            တည်းဖြတ်တန်ဖိုး(စက်, 'FileDemo.java', မူရင်းကုဒ်)
            စက်.အမိန့်('javac FileDemo.java', ['Compiled: FileDemo.class', 'Exit: 0'])
            for 반복 in range(2):
                အထွက် = စက်.အမိန့်('java FileDemo', ['65\r\n255\r\n66\r\n-1\r\n', 'JAVA FILE IO PASS', 'Exit: 0'])
            အချက်စာရင်း = စက်.အမိန့်('ls', ['java.txt  3 bytes'])
            အရွယ် = int(re.search(r'FileDemo.class\s+(\d+) bytes', အချက်စာရင်း)[1])
            with tempfile.TemporaryDirectory(prefix='jkoros-stream-class-') as ယာယီတန်ဖိုး:
                ဖိုင်တွဲတန်ဖိုး = Path(ယာယီတန်ဖိုး)
                ဧည့်သည်ဖိုင်(စက်, 2, အရွယ်, ဖိုင်တွဲတန်ဖိုး / 'FileDemo.class')
                အိမ်ရှင် = subprocess.check_output(['java', '-Xverify:all', '-cp', str(ဖိုင်တွဲတန်ဖိုး), 'FileDemo'], cwd=str(ဖိုင်တွဲတန်ဖိုး), universal_newlines=True)
                assert အိမ်ရှင် == '65\n255\n66\n-1\nJAVA FILE IO PASS\n', အိမ်ရှင်
                assert (ဖိုင်တွဲတန်ဖိုး / 'java.txt').read_bytes() == b'A\xffB'
            တည်းဖြတ်တန်ဖိုး(စက်, 'FileDemo.java', မူရင်းကုဒ်.replace('output.write(65);', 'output.close(); output.write(65);'))
            စက်.အမိန့်('javac FileDemo.java', ['Exit: 0'])
            စက်.အမိန့်('java FileDemo', ['IOException: stream closed', 'Exit: 1'])
            တည်းဖြတ်တန်ဖိုး(စက်, 'FileDemo.java', '''import java.io.FileInputStream;
public class FileDemo {
 public static void main(String[] args) throws Exception {
  FileInputStream input = new FileInputStream("missing.dat");
 }
}''')
            စက်.အမိန့်('javac FileDemo.java', ['Exit: 0'])
            စက်.အမိန့်('java FileDemo', ['FileNotFoundException', 'Exit: 1'])
            စက်.အမိန့်('run hello recovered', ['Exit: 0'])
            ရလဒ်[အမျိုးအစားတန်ဖိုး] = စက်.မှတ်တမ်းမှတ်တမ်းတစ်ခု.decode('utf-8', 'replace')
        finally:
            စက်.ပိတ်()
        print('PASS:', အမျိုးအစားတန်ဖိုး, '게스트 Java ဖိုင် ထုတ်လုပ်/ဆက်လက်ဖြည့်ရေး/ဘိုက်တန်ဖိုး/EOF/ပိတ်ပြီးသလား/မအောင်မြင်မှု/OpenJDK 교차 စက်မောင်း', flush=True)
    (နေရာ / 'build/Javaဖိုင်စမ်းသပ်.json').write_text(json.dumps(ရလဒ်, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    စက်မောင်း()

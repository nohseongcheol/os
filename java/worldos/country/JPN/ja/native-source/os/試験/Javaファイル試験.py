#!/usr/bin/env python3
"""게스트 작성 표준 FileStream 바이트코드를 독립 OpenJDK 실행과 대조한다."""
import json
from pathlib import Path
import re
import subprocess
import tempfile
from 利用者通信網試験 import 仮想機械, 位置
from Java試験 import 編集値, ゲストファイル

def 命令実行():
    結果 = {}
    ソース = (位置.parent / 'posix-kor/Java例/FileDemo.java').read_text()
    for 種別値 in ('elf', 'iso'):
        機械 = 仮想機械(位置 / ('build/kernel.' + 種別値), 種別値, 通信網値=False)
        try:
            編集値(機械, 'FileDemo.java', ソース)
            機械.命令('javac FileDemo.java', ['Compiled: FileDemo.class', 'Exit: 0'])
            for 反復回値 in range(2):
                出力 = 機械.命令('java FileDemo', ['65\r\n255\r\n66\r\n-1\r\n', 'JAVA FILE IO PASS', 'Exit: 0'])
            入口一覧 = 機械.命令('ls', ['java.txt  3 bytes'])
            容量 = int(re.search(r'FileDemo.class\s+(\d+) bytes', 入口一覧)[1])
            with tempfile.TemporaryDirectory(prefix='jkoros-stream-class-') as 一時値:
                ディレクトリ値 = Path(一時値)
                ゲストファイル(機械, 2, 容量, ディレクトリ値 / 'FileDemo.class')
                ホスト = subprocess.check_output(['java', '-Xverify:all', '-cp', str(ディレクトリ値), 'FileDemo'], cwd=str(ディレクトリ値), universal_newlines=True)
                assert ホスト == '65\n255\n66\n-1\nJAVA FILE IO PASS\n', ホスト
                assert (ディレクトリ値 / 'java.txt').read_bytes() == b'A\xffB'
            編集値(機械, 'FileDemo.java', ソース.replace('output.write(65);', 'output.close(); output.write(65);'))
            機械.命令('javac FileDemo.java', ['Exit: 0'])
            機械.命令('java FileDemo', ['IOException: stream closed', 'Exit: 1'])
            編集値(機械, 'FileDemo.java', '''import java.io.FileInputStream;
public class FileDemo {
 public static void main(String[] args) throws Exception {
  FileInputStream input = new FileInputStream("missing.dat");
 }
}''')
            機械.命令('javac FileDemo.java', ['Exit: 0'])
            機械.命令('java FileDemo', ['FileNotFoundException', 'Exit: 1'])
            機械.命令('run hello recovered', ['Exit: 0'])
            結果[種別値] = 機械.履歴記録記録.decode('utf-8', 'replace')
        finally:
            機械.閉鎖()
        print('PASS:', 種別値, '게스트 Java ファイル 生成/継続状態追記/バイト値/EOF/判定閉鎖済み/失敗値/OpenJDK 교차 命令実行', flush=True)
    (位置 / 'build/Javaファイル試験.json').write_text(json.dumps(結果, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    命令実行()

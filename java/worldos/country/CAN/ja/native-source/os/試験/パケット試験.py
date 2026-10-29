#!/usr/bin/env python3
from pathlib import Path
import subprocess
import tempfile

位置 = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='jkoros-packet-test-') as 一時値:
    ディレクトリ値 = Path(一時値)
    境界位置値 = ディレクトリ値 / '시험장치.java'
    境界位置値.write_text('''
class 装置 { static int 時刻印値; static int ミリ秒() { return 時刻印値++; } static void 短時間だけ実行権譲渡() {} }
class 文字端末 { static void 書込(String 値) {} static void 番号書込(int 値) {} }
class 通信装置駆動器 {
    static int 入出力基底番地 = 1, 伝送個数, 個数受取;
    static int[] 装置番地 = {0x52,0x54,0,0x12,0x34,0x56}, 直近値;
    static int 受取(int[] データ) { return 0; }
    static int 送信(int[] データ, int 長さ) { 直近値 = データ.clone(); return 長さ; }
}''', encoding='utf-8')
    subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(ディレクトリ値), str(境界位置値),
                    str(位置 / 'ソース/通信網.java'), str(位置 / '試験/パケット試験.java')], check=True)
    subprocess.run(['java', '-cp', str(ディレクトリ値), 'パケット試験'], check=True, timeout=10)

#!/usr/bin/env python3
from pathlib import Path
import subprocess
import tempfile

位置 = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='jkoros-packet-test-') as 臨時值:
    目錄值 = Path(臨時值)
    邊界位置值 = 目錄值 / '시험장치.java'
    邊界位置值.write_text('''
class 設備 { static int 時間戳值; static int 毫秒() { return 時間戳值++; } static void 掛起短暫地() {} }
class 字元終端 { static void 寫入(String 值) {} static void 寫入編號(int 值) {} }
class 網絡設備驅動 {
    static int 輸入輸出基底地址 = 1, 傳輸個數, 接收個數;
    static int[] 設備地址 = {0x52,0x54,0,0x12,0x34,0x56}, 最近值;
    static int 接收(int[] 資料) { return 0; }
    static int 發送(int[] 資料, int 長度) { 最近值 = 資料.clone(); return 長度; }
}''', encoding='utf-8')
    subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(目錄值), str(邊界位置值),
                    str(位置 / '原始碼/通信網絡.java'), str(位置 / '測試/數據包測試.java')], check=True)
    subprocess.run(['java', '-cp', str(目錄值), '數據包測試'], check=True, timeout=10)

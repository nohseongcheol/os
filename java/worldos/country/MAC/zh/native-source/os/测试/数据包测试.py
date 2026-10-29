#!/usr/bin/env python3
from pathlib import Path
import subprocess
import tempfile

位置 = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='jkoros-packet-test-') as 临时值:
    目录值 = Path(临时值)
    边界位置值 = 目录值 / '시험장치.java'
    边界位置值.write_text('''
class 设备 { static int 时间戳值; static int 毫秒() { return 时间戳值++; } static void 挂起短暂地() {} }
class 字符终端 { static void 写入(String 值) {} static void 写入编号(int 值) {} }
class 网络设备驱动 {
    static int 输入输出基底地址 = 1, 传输个数, 接收个数;
    static int[] 设备地址 = {0x52,0x54,0,0x12,0x34,0x56}, 最近值;
    static int 接收(int[] 数据) { return 0; }
    static int 发送(int[] 数据, int 长度) { 最近值 = 数据.clone(); return 长度; }
}''', encoding='utf-8')
    subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(目录值), str(边界位置值),
                    str(位置 / '源代码/通信网络.java'), str(位置 / '测试/数据包测试.java')], check=True)
    subprocess.run(['java', '-cp', str(目录值), '数据包测试'], check=True, timeout=10)

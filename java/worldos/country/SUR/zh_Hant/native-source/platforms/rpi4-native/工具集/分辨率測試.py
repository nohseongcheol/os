#!/usr/bin/env python3
"""實際資料 QEMU/VNC에서 屏幕 大小·邊界位置值·窗口 移動值·Swing·언어별 그리기를 검사한다."""
import ftplib
import hashlib
import io
import json
import re
import selectors
import socket
import struct
import subprocess
import time
from PIL import Image
from 桌面視圖 import 精確值
from 執行命令 import 項目根


def 分辨率測試(寬度值, 高度值, 結果路徑):
    with socket.socket() as 臨時值:
        臨時值.bind(('127.0.0.1', 0)); 埠編號 = 臨時值.getsockname()[1]
    大小文本 = '{}x{}'.format(寬度值, 高度值)
    程序值 = subprocess.Popen(['python3', str(項目根/'工具集/執行命令.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(埠編號), '--resolution', 大小文本], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    選擇器 = selectors.DefaultSelector(); 選擇器.register(程序值.stdout, selectors.EVENT_READ)
    日誌記錄 = bytearray(); 遠程值 = None; 傳送值 = None

    def 等待(顯示值, 運行=0):
        截止時間值 = time.monotonic() + 60
        while 顯示值 not in 日誌記錄[運行:]:
            if time.monotonic() > 截止時間值 or 程序值.poll() is not None or b'HALTED' in 日誌記錄 or b'PANIC:' in 日誌記錄:
                raise AssertionError(日誌記錄[運行:].decode('utf-8', 'replace'))
            for 事件, _ in 選擇器.select(.1):
                資料 = 事件.fileobj.read(65536)
                if 資料: 日誌記錄.extend(資料)
        return 日誌記錄[運行:].decode('utf-8', 'replace')

    def 單擊按鈕(符號, 是否已按下=True): 遠程值.sendall(struct.pack('>BBHI', 4, int(是否已按下), 0, 符號))

    def 發送文本(文本):
        運行 = len(日誌記錄)
        for 字元值 in 文本:
            符號 = 0xff0d if 字元值 == '\n' else ord(字元值) if ord(字元值) < 256 else 0x1000000 | ord(字元值)
            單擊按鈕(符號); 單擊按鈕(符號, False)
        return 運行

    def 命令殼(文本): return 等待(b'\r\n__RESOLUTION_DONE__\r\n', 發送文本(文本+'; echo __RESOLUTION_DONE__\n'))

    def 分位置(水平位置, 垂直位置, 是否已按下): 遠程值.sendall(struct.pack('>BBHH', 5, 是否已按下, 水平位置, 垂直位置))

    def 單擊值(水平位置, 垂直位置): 分位置(水平位置, 垂直位置, 1); 分位置(水平位置, 垂直位置, 0)

    def 位圖映像():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 實際資料 너비를 쓴다.
        遠程值.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 寬度值, 高度值))
        繪圖 = Image.new('RGB', (寬度值, 高度值)); 區域面積值 = 0
        while True:
            種類值 = 精確值(遠程值, 1)[0]
            if 種類值 == 2: continue
            if 種類值 == 3:
                長度 = struct.unpack('>I', 精確值(遠程值, 7)[3:])[0]; 精確值(遠程值, 長度); continue
            assert 種類值 == 0, 種類值
            項目個數 = struct.unpack('>H', 精確值(遠程值, 3)[1:])[0]
            for _ in range(項目個數):
                水平位置, 垂直位置, 寬度跨度, 長度, 編碼狀態值 = struct.unpack('>HHHHi', 精確值(遠程值, 12))
                assert 編碼狀態值 == 0 and 水平位置+寬度跨度 <= 寬度值 and 垂直位置+長度 <= 高度值
                繪圖.paste(Image.frombytes('RGB', (寬度跨度, 長度), 精確值(遠程值, 寬度跨度*長度*4), 'raw', 'BGRX'), (水平位置, 垂直位置))
                區域面積值 += 寬度跨度*長度
            if 區域面積值:
                assert 區域面積值 == 寬度值*高度值, 區域面積值
                return 繪圖

    def 檢查像素(座標值, 顏色值):
        截止時間值 = time.monotonic()+10
        while True:
            繪圖 = 位圖映像()
            if 繪圖.getpixel(座標值) == 顏色值: return 繪圖
            if time.monotonic() > 截止時間值: raise AssertionError((座標值, 繪圖.getpixel(座標值), 顏色值))

    def 上傳檔案集(名稱, 資料): 傳送值.storbinary('STOR '+名稱, io.BytesIO(資料))

    try:
        等待(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+大小文本+' RGB32').encode() in 日誌記錄
        print('BOOT:', 大小文本, flush=True)
        遠程編號 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', 日誌記錄).group(1))
        遠程值 = socket.create_connection(('127.0.0.1', 遠程編號), timeout=20)
        assert 精確值(遠程值, 12) == b'RFB 003.008\n'; 遠程值.sendall(b'RFB 003.008\n')
        assert 1 in 精確值(遠程值, 精確值(遠程值, 1)[0]); 遠程值.sendall(b'\x01')
        assert 精確值(遠程值, 4) == b'\0'*4; 遠程值.sendall(b'\x01')
        初始狀態 = 精確值(遠程值, 24); assert struct.unpack('>HH', 初始狀態[:4]) == (寬度值, 高度值)
        精確值(遠程值, struct.unpack('>I', 初始狀態[20:])[0])
        遠程值.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        遠程值.sendall(struct.pack('>BBHi', 2, 0, 1, 0))
        檢查像素((寬度值-1, 高度值-1), (24, 32, 48))
        # 屏幕 右 아래까지 이동한다. 上一個項目 640×480 邊界位置值 밖에서 X를 누른다.
        分位置(40, 60, 1); 分位置(寬度值-568+28, 高度值-360+12, 1); 分位置(寬度值-568+28, 高度值-360+12, 0)
        檢查像素((寬度值-568, 高度值-360), (32, 80, 144))
        運行 = len(日誌記錄); 單擊值(寬度值-20, 高度值-345); 等待(b'TERMINAL FOCUS 1', 運行)
        檢查像素((寬度值-568, 高度值-360), (24, 32, 48))
        運行 = len(日誌記錄); 單擊值(80, 16); 等待(b'TERMINAL FOCUS 1', 運行)
        命令殼('ftpd start')
        傳送值 = ftplib.FTP(); 傳送值.encoding = 'utf-8'; 傳送值.connect('127.0.0.1', 埠編號, timeout=20); 傳送值.login()
        # C 邊界位置值 검사는 32비트 unsigned 負數值 轉換值·裁剪 밖·빈 사각형을 포함한다.
        原始碼 = '''#include <屏幕ABI.h>
#include <檔案ABI.h>
int main(void) {
    unsigned 寬度值=屏幕寬度(), 高度值=屏幕高度();
    if(寬度值!=WIDTH || 高度值!=HEIGHT) return 1;
    if(繪製矩形(寬度值,高度值,0,0,0)) return 2;
    if(繪製矩形(寬度值,高度值-1,1,1,0)!=-22) return 3;
    if(繪製矩形(寬度值-1,高度值,1,1,0)!=-22) return 4;
    if(繪製矩形(-1,0,1,1,0)!=-22) return 5;
    if(繪製矩形(0,0,-1,1,0)!=-22) return 6;
    if(繪製矩形(寬度值-1,高度值-1,1,1,0x332211)) return 7;
    寫入檔案資料(1,"C RESOLUTION PASS\\n",18);
    等待狀態用於繪圖(); return 0;
}
'''.replace('WIDTH', str(寬度值)).replace('HEIGHT', str(高度值))
        上傳檔案集('測試屏幕.c', 原始碼.encode())
        assert 'exit 0' in 命令殼('cc /測試屏幕.c -o /測試屏幕')
        等待(b'C RESOLUTION PASS', 發送文本('run /測試屏幕\n'))
        檢查像素((寬度值-1, 高度值-1), (17, 34, 51))
        等待(b'jkoros-native> ', 發送文本('q'))
        原始碼 = '''from 中文 import 屏幕大小, 繪製矩形, 等待狀態用於繪圖, 輸出, 系統錯誤
寬度值, 高度值 = 屏幕大小()
assert (寬度值, 高度值) == (WIDTH, HEIGHT)
try:
    繪製矩形(寬度值, 高度值-1, 1, 1, 0)
    raise AssertionError("boundary")
except 系統錯誤 as 錯誤:
    assert 錯誤.編號 == 22
繪製矩形(寬度值-1, 高度值-1, 1, 1, 0x665544)
輸出("PYTHON RESOLUTION PASS")
等待狀態用於繪圖()
'''.replace('WIDTH', str(寬度值)).replace('HEIGHT', str(高度值))
        上傳檔案集('測試屏幕.py', 原始碼.encode())
        等待(b'PYTHON RESOLUTION PASS', 發送文本('python /測試屏幕.py\n'))
        檢查像素((寬度值-1, 高度值-1), (68, 85, 102))
        等待(b'jkoros-native> ', 發送文本('q'))
        原始碼 = '''import 中文.內建.*;
public class 分辨率測試 {
    public static void main(String[] 實參) {
        int 寬度值=屏幕.寬度值(), 高度值=屏幕.高度值();
        if (寬度值!=WIDTH || 高度值!=HEIGHT) throw new 狀態異常("大小");
        try { 屏幕.矩形(寬度值,高度值-1,1,1,0); throw new 狀態異常("裁剪"); }
        catch (無效實際參數異常 錯誤) { }
        屏幕.擦除條目(0x302018);
        屏幕.矩形(寬度值-1,高度值-1,1,1,0x998877);
        System.out.println("JAVA RESOLUTION PASS");
        屏幕.等待();
    }
}
'''.replace('WIDTH', str(寬度值)).replace('HEIGHT', str(高度值))
        # 異常 처리는 宿主 javac 결과를 內建 JVM에 올려 검사한다.
        邊界位置原始碼 = 結果路徑/'해상도경계시험.java'
        邊界位置原始碼.write_text(原始碼.replace('class 分辨率測試', 'class 해상도경계시험'))
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(項目根/'dist/jkoros-native-korean.jar'), '-d', str(結果路徑), str(邊界位置原始碼)])
        上傳檔案集('해상도경계시험.class', (結果路徑/'해상도경계시험.class').read_bytes())
        等待(b'JAVA RESOLUTION PASS', 發送文本('java 해상도경계시험\n'))
        檢查像素((寬度值-1, 高度值-1), (119, 136, 153))
        等待(b'jkoros-native> ', 發送文本('q'))
        # 게스트 javac의 支持值 문법으로 大小 查詢值·擦除條目·다섯 實參 그리기를 컴파일한다.
        原始碼 = '''public class 分辨率測試 {
    public static void main(String[] 實參) {
        int 寬度值=中文.內建.屏幕.寬度值();
        int 高度值=中文.內建.屏幕.高度值();
        if (寬度值!=WIDTH || 高度值!=HEIGHT) return;
        中文.內建.屏幕.擦除條目(3153944);
        中文.內建.屏幕.矩形(寬度值-1,高度值-1,1,1,10061943);
        中文.內建.輸出.寫入行("JAVA RESOLUTION PASS");
        中文.內建.屏幕.等待();
    }
}
'''.replace('WIDTH', str(寬度值)).replace('HEIGHT', str(高度值))
        上傳檔案集('分辨率測試.java', 原始碼.encode())
        結果 = 命令殼('javac 分辨率測試.java'); assert 'exit 0' in 結果, 結果
        等待(b'JAVA RESOLUTION PASS', 發送文本('java 分辨率測試\n'))
        檢查像素((寬度值-1, 高度值-1), (119, 136, 153))
        等待(b'jkoros-native> ', 發送文本('q'))
        上傳檔案集('Swing測試.class', (結果路徑/'Swing測試.class').read_bytes())
        等待(b'SWING READY', 發送文本('java Swing測試\n'))
        水平位置, 垂直位置 = (寬度值-400)//2, (高度值-280)//2
        繪圖 = 檢查像素((水平位置, 垂直位置), (32, 80, 144))
        繪圖.save(str(結果路徑/(大小文本+'.png')))
        運行 = len(日誌記錄); 單擊值(水平位置+80, 垂直位置+155)
        等待('SWING CLICK 名稱'.encode(), 運行)
        運行 = len(日誌記錄); 單擊值(水平位置+385, 垂直位置+15); 等待(b'jkoros-native> ', 運行)
        assert 'AFTER_RESOLUTION' in 命令殼('echo AFTER_RESOLUTION')
        print('PASS:', 大小文本, 'RGB32, VNC, terminal drag/close, C/Python/Java bounds, centered Swing callbacks', flush=True)
    finally:
        if 傳送值: 傳送值.close()
        if 遠程值: 遠程值.close()
        if 程序值.poll() is None:
            程序值.terminate()
            try: 程序值.wait(timeout=8)
            except subprocess.TimeoutExpired: 程序值.kill(); 程序值.wait()
        選擇器.close(); 程序值.stdout.close()
        (結果路徑/(大小文本+'.log')).write_bytes(日誌記錄)


def 運行():
    結果路徑 = 項目根/'build/verification/resolution'; 結果路徑.mkdir(parents=True, exist_ok=True)
    日誌記錄 = {'passed': False, 'kernel_sha256': hashlib.sha256((項目根/'build/kernel8.img').read_bytes()).hexdigest(), 'resolutions': []}
    try:
        for 無效值 in ('0x0', '639x480', '1920x1081', '1921x1080', '1920*1080'):
            結果 = subprocess.run(['python3', str(項目根/'工具集/執行命令.py'), '--resolution', 無效值], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            assert 結果.returncode == 2 and b'--resolution' in 結果.stderr
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(結果路徑), str(項目根/'測試/Java/Swing測試.java')])
        for 寬度值, 高度值 in ((1920,1080), (1280,720), (640,480)):
            分辨率測試(寬度值, 高度值, 結果路徑); 日誌記錄['resolutions'].append([寬度值, 高度值])
        日誌記錄.update(passed=True, linux_loaded=False, physical_board_tested=False,
            checks=['RFB actual geometry and full-frame RGB32 pixels', 'terminal drag and close at bottom right',
                    'guest cc/javac and Python: Korean size API, last pixel, rejected out-of-bounds drawing',
                    'Swing centered placement, button callback and X', 'desktop and FTP networking together', 'invalid CLI sizes rejected'])
    finally:
        (結果路徑/'report.json').write_text(json.dumps(日誌記錄, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__': 運行()

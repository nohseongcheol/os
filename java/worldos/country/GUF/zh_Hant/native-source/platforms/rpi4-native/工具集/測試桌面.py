#!/usr/bin/env python3
"""實際資料 RFB 클라이언트로 QEMU 창의 한글/鍵值/클립보드/마우스와 屏幕 전송을 검사한다."""
import hashlib
import json
import re
import selectors
import socket
import struct
import subprocess
import time
from pathlib import Path
from 桌面視圖 import 精確值
from 執行命令 import 項目根


def 運行():
    輸出結果=項目根/'build/verification/desktop'; 輸出結果.mkdir(parents=True,exist_ok=True)
    程序=subprocess.Popen(['python3',str(項目根/'工具集/桌面視圖.py'),'--port','0'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    就緒情況監視器=selectors.DefaultSelector(); 就緒情況監視器.register(程序.stdout,selectors.EVENT_READ)
    執行記錄=bytearray(); 有效性驗證報告={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((項目根/'build/kernel8.img').read_bytes()).hexdigest()}
    def 直到(標記,運行=0):
        截止時間時間=time.monotonic()+45
        while 標記 not in 執行記錄[運行:]:
            if time.monotonic()>截止時間時間 or 程序.poll() is not None: raise AssertionError(執行記錄[運行:].decode('utf-8','replace'))
            for 已按下值,_ in 就緒情況監視器.select(.1):
                資料=已按下值.fileobj.read(4096)
                if 資料: 執行記錄.extend(資料)
        return bytes(執行記錄[運行:])
    try:
        直到(b'TERMINAL READY')
        埠編號=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',執行記錄).group(1))
        with socket.create_connection(('127.0.0.1',埠編號),timeout=10) as 客戶端:
            assert 精確值(客戶端,12)==b'RFB 003.008\n'; 客戶端.sendall(b'RFB 003.008\n')
            assert 1 in 精確值(客戶端,精確值(客戶端,1)[0]); 客戶端.sendall(b'\x01'); assert 精確值(客戶端,4)==b'\0'*4
            客戶端.sendall(b'\x01'); 初始值=精確值(客戶端,24); assert struct.unpack('>HH',初始值[:4])==(640,480); 精確值(客戶端,struct.unpack('>I',初始值[20:])[0])
            客戶端.sendall(b'\x00\x00\x00\x00'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
            客戶端.sendall(struct.pack('>BBHi',2,0,1,0))
            def 已按下值(符號值,是否按下中=True): 客戶端.sendall(struct.pack('>BBHI',4,int(是否按下中),0,符號值))
            def 已輸入字元(文本):
                for 字元資料 in 文本:
                    符號=0xff0d if 字元資料=='\n' else ord(字元資料) if ord(字元資料)<256 else 0x01000000|ord(字元資料)
                    已按下值(符號); 已按下值(符號,False)
            def 按下鍵(符號值): 已按下值(符號值); 已按下值(符號值,False)
            # Start with English keys only, as delivered without a host IME.
            偏移值=len(執行記錄); 已輸入字元('echo '); 按下鍵(0xffc6)
            已輸入字元('dkssudgktpdy gksrmf'); 按下鍵(0xffc6); 已輸入字元('\n')
            直到('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),偏移值)
            偏移值=len(執行記錄); 已輸入字元('echo ')
            已按下值(0xffe1); 按下鍵(32); 已按下值(0xffe1,False)
            已輸入字元('dlfr'); 按下鍵(0xff08); 按下鍵(0xff08); 已輸入字元('fr')
            按下鍵(0xff31); 已輸入字元(' EN\n')
            直到('\r\n읽 EN\r\njkoros-native> '.encode(),偏移值)
            偏移值=len(執行記錄); 已輸入字元('echo '); 按下鍵(0xff31)
            已輸入字元('rhk rkqtk RkRnd'); 按下鍵(0xff31); 已輸入字元('\n')
            直到('\r\n과 갑사 까꿍\r\njkoros-native> '.encode(),偏移值)
            # The same composition edits UTF-8 text in the native vi editor.
            偏移值=len(執行記錄); 已輸入字元('vi 韓文字母輸入.txt\n'); 直到(b'NORMAL',偏移值)
            已輸入字元('i'); 按下鍵(0xffc6); 已輸入字元('gksrmf dlfr'); 按下鍵(0xffc6)
            按下鍵(0xff1b); 已輸入字元(':wq\n'); 直到(b'jkoros-native> ',偏移值)
            偏移值=len(執行記錄); 已輸入字元('cat 韓文字母輸入.txt\n')
            直到('한글 읽'.encode(),偏移值); 直到(b'jkoros-native> ',偏移值)
            偏移值=len(執行記錄); 已輸入字元('help ko\n')
            直到('한/零操作數 鍵值, Shift+Space 또는 F9'.encode(),偏移值); 直到(b'jkoros-native> ',偏移值)
            偏移值=len(執行記錄); 已輸入字元('clear\necho "VNC 한글 輸入值 😀"\n'); 直到('VNC 한글 輸入值 😀\r\n'.encode(),偏移值)
            偏移值=len(執行記錄); 已按下值(0xffe3); 已按下值(ord('u')); 已按下值(ord('u'),False); 已按下值(0xffe3,False); 已輸入字元('echo CONTROL_OK\n'); 直到(b'\r\nCONTROL_OK\r\n',偏移值)
            # A shared clipboard is not a paste command. Require explicit Ctrl+Shift+V.
            剪貼板值='echo "粘貼值 是否完成"\n'.encode(); 偏移值=len(執行記錄)
            客戶端.sendall(struct.pack('>B3xI',6,len(剪貼板值))+剪貼板值)
            for 事件,_ in 就緒情況監視器.select(.15):
                資料塊=事件.fileobj.read(4096)
                if 資料塊: 執行記錄.extend(資料塊)
            assert '粘貼值 是否完成'.encode() not in 執行記錄[偏移值:]
            已按下值(0xffe3); 已按下值(0xffe1); 已按下值(ord('v')); 已按下值(ord('v'),False); 已按下值(0xffe1,False); 已按下值(0xffe3,False)
            # The prompt follows the guest's terminal redraw after command completion.
            直到('\r\n붙여넣기 是否完成\r\njkoros-native> '.encode(),偏移值)
            客戶端.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
            紅_綠_藍顏色=bytearray(640*480*3); 已看見條目列=False
            while not 已看見條目列:
                通知文本=精確值(客戶端,1)[0]
                if 通知文本==2: continue
                if 通知文本==3:
                    大小=struct.unpack('>I',精確值(客戶端,7)[3:])[0]; 精確值(客戶端,大小); continue
                assert 通知文本==0,通知文本
                矩形列列表=struct.unpack('>H',精確值(客戶端,3)[1:])[0]
                for _ in range(矩形列列表):
                    橫座標座標,Y_按鈕座標,已請求寬度值,已請求高度值,字元設定=struct.unpack('>HHHHi',精確值(客戶端,12)); assert 字元設定==0,字元設定
                    像素列列表=精確值(客戶端,已請求寬度值*已請求高度值*4)
                    for 內部側序數 in range(已請求高度值):
                        for 序數索引 in range(已請求寬度值):
                            原始地址=(內部側序數*已請求寬度值+序數索引)*4; 目的地址地址=((Y_按鈕座標+內部側序數)*640+橫座標座標+序數索引)*3
                            紅_綠_藍顏色[目的地址地址:目的地址地址+3]=bytes((像素列列表[原始地址+2],像素列列表[原始地址+1],像素列列表[原始地址]))
                    已看見條目列=True
            assert 紅_綠_藍顏色[(48*640+12)*3:(48*640+12)*3+3]==bytes((32,80,144))
            (輸出結果/'vnc-terminal.ppm').write_bytes(b'P6\n640 480\n255\n'+紅_綠_藍顏色)
            from PIL import Image
            Image.frombytes('RGB',(640,480),bytes(紅_綠_藍顏色)).save(str(輸出結果/'vnc-terminal.png'))
            偏移值=len(執行記錄)
            已按下值(0xffe3); 已按下值(0xffe1); 已按下值(ord('t')); 已按下值(ord('t'),False); 已按下值(0xffe1,False); 已按下值(0xffe3,False)
            直到(b'TERMINAL FOCUS 2',偏移值)
            偏移值=len(執行記錄); 已輸入字元('echo SECOND_VNC_WINDOW\n'); 直到(b'\r\nSECOND_VNC_WINDOW\r\n',偏移值)
            偏移值=len(執行記錄); 客戶端.sendall(struct.pack('>BBHH',5,1,576,81)); 客戶端.sendall(struct.pack('>BBHH',5,0,576,81)); 直到(b'TERMINAL FOCUS 1',偏移值)
            偏移值=len(執行記錄); 已輸入字元('python -c \'print("x"*9000)\'\n'); 直到(b'\r\njkoros-native> ',偏移值)
            assert len(執行記錄)-偏移值>8192,'exercise output longer than bridge status buffer'
            偏移值=len(執行記錄); 客戶端.sendall(struct.pack('>BBHH',5,1,560,63)); 客戶端.sendall(struct.pack('>BBHH',5,0,560,63)); 直到(b'TERMINAL FOCUS 1',偏移值)
            偏移值=len(執行記錄); 客戶端.sendall(struct.pack('>BBHH',5,1,80,16)); 客戶端.sendall(struct.pack('>BBHH',5,0,80,16)); 直到(b'TERMINAL FOCUS 1',偏移值)
            偏移值=len(執行記錄); 已輸入字元('echo REOPENED_VNC_WINDOW\n'); 直到(b'\r\nREOPENED_VNC_WINDOW\r\n',偏移值)
            偏移值=len(執行記錄); 已輸入字元('gui\n'); 直到(b'GUI READY:',偏移值)
            偏移值=len(執行記錄); 客戶端.sendall(struct.pack('>BBHH',5,1,80,332)); 客戶端.sendall(struct.pack('>BBHH',5,0,80,332)); 直到(b'TERMINAL READY',偏移值)
            有效性驗證報告.update(passed=True,checks=['RFB 3.8 handshake and actual 640x480 raw framebuffer','F9, Shift+Space and Hangul toggle: ASCII two-set keys compose Korean in shell and vi','compound vowels/finals, resyllabification and composition Backspace','help ko lists implemented shortcuts','Unicode Hangul/emoji keysyms -> guest shell','Ctrl modifiers and explicit clipboard paste; no clipboard auto-execution','Ctrl+Shift+T creates second native terminal, mouse X closes it','mouse close after 9 KiB output, desktop new-terminal button and legacy launcher button'])
        print('PASS: actual VNC keyboard/Unicode/paste/mouse/framebuffer -> native terminal')
    finally:
        if 程序.poll() is None:
            程序.terminate()
            try: 程序.wait(timeout=8)
            except subprocess.TimeoutExpired: 程序.kill(); 程序.wait()
        就緒情況監視器.close(); 程序.stdout.close()
        (輸出結果/'serial.log').write_bytes(執行記錄)
        (輸出結果/'report.json').write_text(json.dumps(有效性驗證報告,indent=2)+'\n')


if __name__=='__main__': 運行()

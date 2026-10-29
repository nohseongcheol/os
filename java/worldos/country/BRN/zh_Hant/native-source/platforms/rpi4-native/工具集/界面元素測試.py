#!/usr/bin/env python3
"""Native Swing rendering, Java callbacks, Korean wrappers and session switching."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from 執行命令 import 項目根,命令

def 運行():
    目的地址值位置=項目根/'build/verification/swing';目的地址值位置.mkdir(parents=True,exist_ok=True)
    類別路徑=項目根/'build/verification/new-java';類別路徑.mkdir(parents=True,exist_ok=True)
    subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(項目根/'dist/jkoros-native-korean.jar'),'-d',str(類別路徑),str(項目根/'測試/Java/Swing測試.java'),str(項目根/'測試/Java/測試韓文字母窗口.java')])
    有效性驗證報告={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((項目根/'build/kernel8.img').read_bytes()).hexdigest()};日誌記錄=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 工作中路徑:
        測試替身控制連接狀態=Path(工作中路徑)/'qmp.sock'
        資料位置=subprocess.Popen(命令()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(測試替身控制連接狀態)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        選擇器=selectors.DefaultSelector();選擇器.register(資料位置.stdout,selectors.EVENT_READ)
        def 句柄事件(秒數單位=.1):
            for 已按下值,_ in 選擇器.select(秒數單位):
                第二值=已按下值.fileobj.read(65536)
                if 第二值:日誌記錄.extend(第二值)
            assert b'PANIC:' not in 日誌記錄 and b'HALTED' not in 日誌記錄,日誌記錄[-2048:]
        def 等待(標記,當前位置,秒數單位=50):
            結束偏移=time.monotonic()+秒數單位
            while 標記 not in 日誌記錄[當前位置:]:
                if time.monotonic()>結束偏移 or 資料位置.poll() is not None:raise AssertionError(日誌記錄[當前位置:].decode('utf-8','replace'))
                句柄事件()
            return bytes(日誌記錄[當前位置:])
        def 發送(第二值,標記=b'jkoros-native> '):
            當前位置=len(日誌記錄);資料位置.stdin.write(第二值);資料位置.stdin.flush();return 等待(標記,當前位置)
        def 命令殼(字符串資料):return 發送((字符串資料+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def 快捷操作值(第三索引):return bytes([30,2,第三索引,0,0,0,0])
        def 單擊按鈕(橫座標座標,Y_按鈕座標):return bytes([30,1,1,橫座標座標&255,橫座標座標>>8,Y_按鈕座標&255,Y_按鈕座標>>8,30,1,0,橫座標座標&255,橫座標座標>>8,Y_按鈕座標&255,Y_按鈕座標>>8])
        def 命令模式():
            資料位置.stdin.write(b'\x1b');資料位置.stdin.flush();結束偏移=time.monotonic()+.2
            while time.monotonic()<結束偏移:句柄事件(.03)
        try:
            等待(b'jkoros-native> ',0)
            命令殼('terminal');句柄事件(.3)
            資料=(項目根/'build/verification/new-java/Swing測試.class').read_bytes()
            發送('load Swing測試.class\n'.encode(),b'hex> ')
            for 序數索引 in range(0,len(資料),64):發送(資料[序數索引:序數索引+64].hex().encode()+b'\n',b'hex> ')
            發送(b'.\n')
            發送('java Swing測試\n'.encode(),b'SWING READY')
            結束偏移=time.monotonic()+3
            while time.monotonic()<結束偏移:句柄事件(.1)
            # JFrame centered at (120,100), content at y=130.
            發送(單擊按鈕(200,210),b'',)  # focus JTextField
            資料位置.stdin.write('누리'.encode());資料位置.stdin.flush()
            結束偏移=time.monotonic()+.3
            while time.monotonic()<結束偏移:句柄事件(.05)
            結果=發送(單擊按鈕(200,255),'SWING CLICK 이름누리'.encode())
            等待(b'true',len(日誌記錄)-len(結果))
            發送(快捷操作值(1),b'TERMINAL FOCUS 2')
            結果=命令殼('echo GUI_SUSPENDED_OK');assert b'GUI_SUSPENDED_OK' in 結果
            發送(單擊按鈕(180,12),b'TERMINAL FOCUS 1')
            結束偏移=time.monotonic()+.3
            while time.monotonic()<結束偏移:句柄事件(.05)
            with socket.socket(socket.AF_UNIX) as 字元程式碼:
                字元程式碼.settimeout(10);字元程式碼.connect(str(測試替身控制連接狀態))
                with 字元程式碼.makefile('rwb') as 檔案條目:
                    json.loads(檔案條目.readline())
                    for 申請值 in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(目的地址值位置/'native-swing.png'),'format':'png'}}):
                        檔案條目.write((json.dumps(申請值)+'\n').encode());檔案條目.flush()
                        while True:
                            已返回值=json.loads(檔案條目.readline())
                            if 'error' in 已返回值:raise AssertionError(已返回值)
                            if 'return' in 已返回值:break
            發送(單擊按鈕(505,115))
            命令殼('echo SWING_CLOSED_OK')
            資料=(類別路徑/'測試韓文字母窗口.class').read_bytes()
            發送('load 測試韓文字母窗口.class\n'.encode(),b'hex> ')
            for 序數索引 in range(0,len(資料),64):發送(資料[序數索引:序數索引+64].hex().encode()+b'\n',b'hex> ')
            發送(b'.\n')
            發送('java 測試韓文字母窗口\n'.encode(),b'KOREAN SWING READY')
            發送(單擊按鈕(200,255),'KOREAN SWING CLICK 名稱'.encode())
            發送(單擊按鈕(505,115))
            命令殼('echo KOREAN_SWING_CLOSED_OK')
            有效性驗證報告.update(passed=True,direct_korean_gui=True,checks=['standard javax.swing JFrame/JLabel/JTextField/JButton in own EL0 JVM','SwingUtilities.invokeLater and ActionListener callbacks','Korean GUI text and UTF-8 keyboard input','3-second GUI lifetime and suspend/resume across terminals','JFrame title-bar X disposes window and returns to shell','中文 窗口/按鈕/動作通知/事件排隊 directly allocate objects and dispatch Korean callbacks; distinct from standard GUI types'])
            print('PASS: native Swing subset, Unicode input, action callback, lifecycle and suspension')
        finally:
            if 資料位置.poll() is None:資料位置.terminate()
            try:資料位置.wait(timeout=5)
            except subprocess.TimeoutExpired:資料位置.kill();資料位置.wait()
            選擇器.close();資料位置.stdin.close();資料位置.stdout.close();(目的地址值位置/'serial.log').write_bytes(日誌記錄);(目的地址值位置/'report.json').write_text(json.dumps(有效性驗證報告,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':運行()

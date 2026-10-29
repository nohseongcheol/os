#!/usr/bin/env python3
"""Actual EL0 vi, independently preserved terminal sessions and process snapshots."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from 執行命令 import 項目根,命令

def 運行():
    目的地址值位置=項目根/'build/verification/windows';目的地址值位置.mkdir(parents=True,exist_ok=True)
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
            命令殼('mkdir first; cd first; export NAME=one')
            發送('vi 首位序數.py\n'.encode(),b'NORMAL')
            發送('i값 = 21\nprint(值 * 2)\n'.encode(),b'INSERT')
            # A live editor survives the old two-second deadline and can be suspended.
            結束偏移=time.monotonic()+3
            while time.monotonic()<結束偏移:句柄事件(.1)
            發送(快捷操作值(1),b'TERMINAL FOCUS 2');句柄事件(.2)
            assert b'/\r\n' in 命令殼('pwd')
            命令殼('export NAME=two')
            發送('vi 第二序數.txt\n'.encode(),b'NORMAL')
            發送('i두 번째 窗口\n'.encode(),b'INSERT')
            發送(單擊按鈕(180,12),b'TERMINAL FOCUS 1');句柄事件(.2)
            命令模式();發送(b':wq\r')
            assert b'one:/first' in 命令殼('echo "$NAME:$PWD"')
            assert '值 = 21\r\nprint(值 * 2)'.encode() in 命令殼('cat 首位序數.py')
            結果=命令殼('python 首位序數.py');assert b'42\r\n' in 結果,結果
            # Close the first shell with its actual title-bar X; second editor resumes.
            發送(單擊按鈕(560,63),b'TERMINAL FOCUS 2');句柄事件(.2)
            命令模式();發送(b':wq\r')
            assert b'two:/' in 命令殼('echo "$NAME:$PWD"')
            assert '두 번째 窗口'.encode() in 命令殼('cat 第二序數.txt')
            # Edit persisted text, undo, refuse an unsaved quit, then explicitly discard.
            發送('vi 第二序數.txt\n'.encode(),b'NORMAL');發送(b'xu',b'NORMAL')
            發送(b'iX',b'INSERT');命令模式();發送(b':q\r',b'Unsaved')
            發送(b':q!\r');assert '두 번째 窗口'.encode() in 命令殼('cat 第二序數.txt')
            發送(快捷操作值(1),b'TERMINAL FOCUS 1');句柄事件(.2)
            發送(快捷操作值(1),b'TERMINAL FOCUS 3');句柄事件(.2)
            發送(快捷操作值(1),b'TERMINAL FOCUS 4');句柄事件(.2)
            # Drag the fourth terminal, then close a running editor with unsaved text.
            資料位置.stdin.write(bytes([30,1,1,200,0,116,0,30,1,1,170,0,96,0,30,1,0,170,0,96,0]));資料位置.stdin.flush()
            命令殼('echo DRAGGED_OK')
            發送('vi 버릴문서.txt\n'.encode(),b'NORMAL')
            發送('i저장하지 않은 資料'.encode(),b'INSERT')
            發送(單擊按鈕(578,97),b'TERMINAL FOCUS 3');句柄事件(.2)
            assert '버릴문서.txt'.encode() not in 命令殼('ls')
            發送(快捷操作值(1),b'TERMINAL FOCUS 4');句柄事件(.2)
            命令殼('echo REUSED_WINDOW_OK')
            已完成總量=日誌記錄.rfind(b'\r\n__DONE__\r\n')+len(b'\r\n__DONE__\r\n')
            等待(b'jkoros-native> ',已完成總量)
            # UART completion precedes the next QEMU display refresh.
            結束偏移=time.monotonic()+.3
            while time.monotonic()<結束偏移:句柄事件(.05)
            with socket.socket(socket.AF_UNIX) as 字元程式碼:
                字元程式碼.settimeout(10);字元程式碼.connect(str(測試替身控制連接狀態))
                with 字元程式碼.makefile('rwb') as 檔案條目:
                    json.loads(檔案條目.readline())
                    for 申請值 in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(目的地址值位置/'four-terminals.png'),'format':'png'}}):
                        檔案條目.write((json.dumps(申請值)+'\n').encode());檔案條目.flush()
                        while True:
                            已返回值=json.loads(檔案條目.readline())
                            if 'error' in 已返回值:raise AssertionError(已返回值)
                            if 'return' in 已返回值:break
            from PIL import Image
            像素列列表=Image.open(str(目的地址值位置/'four-terminals.png')).convert('RGB')
            for 座標一對,像素顏色 in [((12,48),(56,68,96)),((590,66),(56,68,96)),((44,84),(56,68,96)),((60,102),(32,80,144))]:
                assert 像素列列表.getpixel(座標一對)==像素顏色,(座標一對,像素列列表.getpixel(座標一對))
            命令殼('echo FOUR_WINDOWS_OK')
            有效性驗證報告.update(passed=True,checks=['EL0 UTF-8 vi create/save/edit/undo/unsaved quit/discard','interactive editor survives 3 seconds','two suspended vi instances preserve memory/registers and independent cwd/env','dragged title-bar X terminates unsaved vi, frees process, and permits window reuse','four native terminal windows','Korean Python identifiers compile and run after vi save'])
            print('PASS: native four-window desktop, independent shells, suspended EL0 vi, Korean coding')
        finally:
            if 資料位置.poll() is None:資料位置.terminate()
            try:資料位置.wait(timeout=5)
            except subprocess.TimeoutExpired:資料位置.kill();資料位置.wait()
            選擇器.close();資料位置.stdin.close();資料位置.stdout.close();(目的地址值位置/'serial.log').write_bytes(日誌記錄);(目的地址值位置/'report.json').write_text(json.dumps(有效性驗證報告,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':運行()

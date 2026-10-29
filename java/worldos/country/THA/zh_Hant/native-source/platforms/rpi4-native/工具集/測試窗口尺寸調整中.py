#!/usr/bin/env python3
"""實際資料 QEMU/VNC에서 終端 角值 拖動值·指針·동적 字元值 槽條目·編輯值 內容值 보존를 검사한다."""
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


def 測試窗口尺寸調整中(寬度值, 高度值, 結果路徑):
    with socket.socket() as 臨時值:
        臨時值.bind(('127.0.0.1', 0)); 埠編號 = 臨時值.getsockname()[1]
    大小文本 = '{}x{}'.format(寬度值, 高度值)
    程序值 = subprocess.Popen(['python3', str(項目根/'工具集/執行命令.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(埠編號), '--resolution', 大小文本], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    選擇器 = selectors.DefaultSelector(); 選擇器.register(程序值.stdout, selectors.EVENT_READ)
    日誌記錄 = bytearray(); 遠程值 = None; 傳送值 = None; 指針隱藏=[False]

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

    def 命令殼(文本): return 等待(b'\r\n__RESIZE_DONE__\r\n', 發送文本(文本+'; echo __RESIZE_DONE__\n'))

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
                if 編碼狀態值 == -239:
                    assert 寬度跨度==0 and 長度==0, 'remote cursor must be hidden'
                    指針隱藏[0]=True
                    continue
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
        遠程值.sendall(struct.pack('>BBHii', 2, 0, 2, 0, -239))
        檢查像素((寬度值-1, 高度值-1), (24, 32, 48))
        def 暫停短暫地(秒數值=.25):
            結尾=time.monotonic()+秒數值
            while time.monotonic()<結尾:
                for 事件,_ in 選擇器.select(.02):
                    資料=事件.fileobj.read(65536)
                    if 資料:日誌記錄.extend(資料)
        窗口=[12,48,568,360]
        def 驗證大小():
            欄值,列值=(窗口[2]-24)//8,(窗口[3]-56)//16
            文本=命令殼('terminal size')
            assert 'TERMINAL SIZE {}x{}\r\n'.format(欄值,列值) in 文本,文本
            # 實際資料 窗口 테두리: 단지 大小 查詢值 값만 바뀐 것이 아닌지 확인한다.
            分位置(寬度值-1,10,0);暫停短暫地()
            檢查像素((窗口[0],窗口[1]),(32,80,144))
            繪圖=檢查像素((窗口[0]+窗口[2]-1,窗口[1]+窗口[3]-1),(39,49,64))
            return 繪圖
        def 角值(方向):
            return (窗口[0]+(3 if 方向 in (1,3) else 窗口[2]-4),窗口[1]+(3 if 方向<=2 else 窗口[3]-4))
        def 調整尺寸拖動(方向,差異值,按鈕=1):
            首位操作數,三值=角值(方向);分位置(首位操作數,三值,0);暫停短暫地()
            # 대각선 양방향 화살표의 흰 선과 반대 방향의 빈 점을 확인한다.
            白像素=(首位操作數-7 if 方向 in (1,4) else 首位操作數+7,三值-7)
            檢查像素(白像素,(255,255,255))
            分位置(首位操作數,三值,按鈕)
            結束水平=max(0,min(寬度值-1,首位操作數+差異值[0]));結束垂直=max(0,min(高度值-1,三值+差異值[1]))
            分位置(結束水平,結束垂直,按鈕);分位置(結束水平,結束垂直,0);暫停短暫地()
            if 按鈕==1:
                左值,頂端值,寬度跨度,長度=窗口;右值,底端值=左值+寬度跨度,頂端值+長度
                if 方向 in (1,3):左值=max(0,min(右值-360,左值+結束水平-首位操作數))
                else:右值=max(左值+360,min(寬度值,右值+結束水平-首位操作數))
                if 方向<=2:頂端值=max(34,min(底端值-216,頂端值+結束垂直-三值))
                else:底端值=max(頂端值+216,min(高度值,底端值+結束垂直-三值))
                窗口[:]=[左值,頂端值,右值-左值,底端值-頂端值]
        驗證大小();assert 指針隱藏[0]
        調整尺寸拖動(4,(-100,-60),4);驗證大小() # 右 버튼은 크기를 바꾸지 않는다.
        for 方向,差異值 in ((4,(-120,-80)),(1,(24,16)),(2,(40,16)),(3,(24,32))):
            調整尺寸拖動(方向,差異值);驗證大小()
        # 輸入值 중인 긴 韓文文本 명령은 換行/水平位置 스크롤과 무관하게 그대로 실행된다.
        長整數文本='크기가 바뀌어도 입력한 한글 명령이 그대로 남습니다 '*3
        發送文本("echo '"+長整數文本+"'");暫停短暫地()
        調整尺寸拖動(4,(-1000,-1000));assert 窗口[2:]==[360,216]
        調整尺寸拖動(4,(寬度值,高度值))
        運行=發送文本('\n');等待(('\r\n'+長整數文本+'\r\n').encode(),運行);驗證大小()
        # vi가 編輯值 중에 屏幕 크기를 重試值 읽고, 저장하지 않은 한글도 유지한다.
        命令殼('ftpd start')
        傳送值=ftplib.FTP();傳送值.encoding='utf-8';傳送值.connect('127.0.0.1',埠編號,timeout=20);傳送值.login()
        等待(b'NORMAL',發送文本('vi /크기자료.txt\n'))
        等待(b'INSERT',發送文本('i미저장 한글 資料\n'));暫停短暫地()
        調整尺寸拖動(4,(-寬度值,-高度值))
        # ANSI 列值 이동에 새 列值 수가 나타나는지, 한 글자도 입력하지 않고 확인한다.
        assert ('\x1b[{};1H'.format((窗口[3]-56)//16)).encode() in 日誌記錄[-4096:]
        發送文本('작은 창에서도 繼續狀態值 寫入\n');暫停短暫地()
        調整尺寸拖動(4,(寬度值,高度值))
        發送文本('큰 창에서도 繼續狀態值 寫入\n');暫停短暫地()
        單擊按鈕(0xff1b);單擊按鈕(0xff1b,False);暫停短暫地()
        等待(b'jkoros-native> ',發送文本(':wq\n'))
        內容值=bytearray();傳送值.retrbinary('RETR 크기자료.txt',內容值.extend)
        assert 內容值=='미저장 한글 資料\n작은 창에서도 繼續狀態值 寫入\n큰 창에서도 繼續狀態值 寫入\n'.encode(),內容值
        驗證大小().save(str(結果路徑/(大小文本+'-large.png')))
        # 두 번째 창은 默認值 大小, 重試值 首位項目 창을 고르면 앞에서 바꾼 크기가 유지된다.
        運行=len(日誌記錄);單擊值(70,16);等待(b'TERMINAL FOCUS 2',運行)
        assert 'TERMINAL SIZE 68x19' in 命令殼('terminal size')
        運行=len(日誌記錄);單擊值(180,16);等待(b'TERMINAL FOCUS 1',運行);驗證大小()
        調整尺寸拖動(4,(-寬度值,-高度值));驗證大小().save(str(結果路徑/(大小文本+'-small.png')))
        # 大小 更改值 後端值 X 닫기도 새로운 右 가장자리를 사용한다.
        運行=len(日誌記錄);單擊值(窗口[0]+窗口[2]-20,窗口[1]+15);等待(b'TERMINAL FOCUS 2',運行)
        assert 'RESIZE CLOSED' in 命令殼('echo RESIZE CLOSED')
        print('PASS:',大小文本,'four corners, left drag, cursor, limits, live shell/vi, independent windows',flush=True)
    finally:
        if 傳送值:傳送值.close()
        if 遠程值:遠程值.close()
        if 程序值.poll() is None:
            程序值.terminate()
            try:程序值.wait(timeout=8)
            except subprocess.TimeoutExpired:程序值.kill();程序值.wait()
        選擇器.close();程序值.stdout.close();(結果路徑/(大小文本+'.log')).write_bytes(日誌記錄)


def 運行():
    結果路徑=項目根/'build/verification/resize';結果路徑.mkdir(parents=True,exist_ok=True)
    日誌記錄={'passed':False,'kernel_sha256':hashlib.sha256((項目根/'build/kernel8.img').read_bytes()).hexdigest(),'resolutions':[]}
    try:
        for 寬度值,高度值 in ((640,480),(1920,1080)):
            測試窗口尺寸調整中(寬度值,高度值,結果路徑);日誌記錄['resolutions'].append([寬度值,高度值])
        日誌記錄.update(passed=True,checks=['native diagonal cursor pixels and hidden RFB cursor','all four corners use left drag; right drag ignored',
            'minimum/maximum geometry and current text rows/columns','long Korean shell input and unsaved vi text preserved',
            'vi redraws during idle resize','per-window geometry and resized X close'])
    finally:(結果路徑/'report.json').write_text(json.dumps(日誌記錄,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':運行()

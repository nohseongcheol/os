#!/usr/bin/env python3
"""Run all examples in the real combined VNC + SLIP/FTP native VM."""
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
from pathlib import Path
from 桌面視圖 import 精確值
from 回顯示例服務器 import 回顯服務器列
from 執行命令 import 項目根


def 測試語言(語言,回顯服務器條目,結果資料):
    with socket.socket() as 臨時:
        臨時.bind(('127.0.0.1',0));檔案傳送埠編號=臨時.getsockname()[1]
    程序=subprocess.Popen(['python3',str(項目根/'工具集/執行命令.py'),'--desktop','--network','--port','0','--ftp-port',str(檔案傳送埠編號)],
        stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    就緒選擇器=selectors.DefaultSelector();就緒選擇器.register(程序.stdout,selectors.EVENT_READ)
    執行記錄=bytearray();客戶端=None;檔案傳送連接狀態=None
    def 接收消息(標記,運行=0):
        結束偏移=time.monotonic()+60
        while 標記 not in 執行記錄[運行:]:
            if time.monotonic()>結束偏移 or 程序.poll() is not None:raise AssertionError(執行記錄[運行:].decode('utf-8','replace'))
            for 已按下值,_ in 就緒選擇器.select(.1):
                資料=已按下值.fileobj.read(65536)
                if 資料:執行記錄.extend(資料)
        return 執行記錄[運行:].decode('utf-8','replace').replace('\r\n','\n')
    def 已按下值(符號值,是否按下中=True):客戶端.sendall(struct.pack('>BBHI',4,int(是否按下中),0,符號值))
    def 開始偏移(行):
        運行=len(執行記錄)
        for 字元程式碼 in 行+'\n':
            符號值=0xff0d if 字元程式碼=='\n' else ord(字元程式碼) if ord(字元程式碼)<256 else 0x1000000|ord(字元程式碼)
            已按下值(符號值);已按下值(符號值,False)
        return 運行
    def 命令殼(行):return 接收消息(b'jkoros-native> ',開始偏移(行))
    def 執行命令(行,預期):
        文本=命令殼(行);assert 預期 in 文本 and 'exit 0' in 文本,(行,文本)
        return 文本
    def 像素列列表():
        客戶端.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
        紅_綠_藍顏色=bytearray(640*480*3)
        while True:
            分類值=精確值(客戶端,1)[0]
            if 分類值==2:continue
            if 分類值==3:
                項目個數=struct.unpack('>I',精確值(客戶端,7)[3:])[0];精確值(客戶端,項目個數);continue
            assert 分類值==0,分類值
            條目個數=struct.unpack('>H',精確值(客戶端,3)[1:])[0]
            for _ in range(條目個數):
                橫座標座標,Y_按鈕座標,已請求寬度值,已請求高度值,字元設定=struct.unpack('>HHHHi',精確值(客戶端,12));assert 字元設定==0,字元設定
                資料=精確值(客戶端,已請求寬度值*已請求高度值*4)
                for 列位置 in range(已請求高度值):
                    for 欄位置 in range(已請求寬度值):
                        原始資料=(列位置*已請求寬度值+欄位置)*4;目標值=((Y_按鈕座標+列位置)*640+橫座標座標+欄位置)*3
                        紅_綠_藍顏色[目標值:目標值+3]=bytes((資料[原始資料+2],資料[原始資料+1],資料[原始資料]))
            if 條目個數:return 紅_綠_藍顏色
    try:
        接收消息(b'TERMINAL READY');接收消息(b'jkoros-native> ',執行記錄.rfind(b'TERMINAL READY'))
        埠編號=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',執行記錄).group(1))
        客戶端=socket.create_connection(('127.0.0.1',埠編號),timeout=10)
        assert 精確值(客戶端,12)==b'RFB 003.008\n';客戶端.sendall(b'RFB 003.008\n')
        assert 1 in 精確值(客戶端,精確值(客戶端,1)[0]);客戶端.sendall(b'\x01');assert 精確值(客戶端,4)==b'\0'*4
        客戶端.sendall(b'\x01');初始值=精確值(客戶端,24);精確值(客戶端,struct.unpack('>I',初始值[20:])[0])
        客戶端.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
        客戶端.sendall(struct.pack('>BBHi',2,0,1,0))
        assert 'FTP listening' in 命令殼('ftpd start')
        檔案傳送連接狀態=ftplib.FTP();檔案傳送連接狀態.encoding='utf-8';檔案傳送連接狀態.connect('127.0.0.1',檔案傳送埠編號,timeout=20);檔案傳送連接狀態.login()
        載荷數據資料=('GUI와 FTP 동시 使用值 '+語言+' 😀\n').encode()
        檔案傳送連接狀態.storbinary('STOR 함께.txt',io.BytesIO(載荷數據資料))
        assert 載荷數據資料.decode().strip() in 命令殼('cat /함께.txt')
        已接收個數=bytearray();檔案傳送連接狀態.retrbinary('RETR 함께.txt',已接收個數.extend);assert 已接收個數==載荷數據資料;檔案傳送連接狀態.delete('함께.txt')
        # No installation command: every language and the manual exist at boot.
        發送列表=命令殼('ls /example')
        assert all(名稱 in 發送列表 for 名稱 in ('java/','c/','python/','README.md')),發送列表
        if 語言=='java':
            捆綁構建清單=json.loads((項目根/'build/examples/manifest.json').read_text())
            for 路徑,條目分 in 捆綁構建清單.items():
                命令殼('cp '+路徑+' /example-check.bin')
                內容值=bytearray();檔案傳送連接狀態.retrbinary('RETR example-check.bin',內容值.extend)
                assert len(內容值)==條目分['bytes'] and hashlib.sha256(內容值).hexdigest()==條目分['sha256'],路徑
            檔案傳送連接狀態.delete('example-check.bin')
            # Exercise packed file bytes, the last byte of a full file, and root
            # FTP listing for file slots above the former 16-entry limit.
            二進制=bytes(range(256))*64
            檔案傳送連接狀態.storbinary('STOR boundary.bin',io.BytesIO(二進制))
            內容值=bytearray();檔案傳送連接狀態.retrbinary('RETR boundary.bin',內容值.extend)
            assert 內容值==二進制 and 'boundary.bin' in 檔案傳送連接狀態.nlst()
            命令殼('cp /boundary.bin /boundary-copy.bin')
            內容值=bytearray();檔案傳送連接狀態.retrbinary('RETR boundary-copy.bin',內容值.extend)
            assert 內容值==二進制
            檔案傳送連接狀態.delete('boundary.bin');檔案傳送連接狀態.delete('boundary-copy.bin')
        assert '輸出例' in 命令殼('ls /example/'+語言)
        命令殼('cd /example/'+語言)
        名稱表={'java':'JAVA','c':'C','python':'PYTHON'}[語言]
        預期檔案=名稱表+' 檔案: 한글 資料 😀\n'
        if 語言=='java':
            執行命令('javac 輸出例.java','Compiled:');執行命令('java 輸出例','JAVA 輸出: 안녕하세요 😀')
            執行命令('javac 檔案例.java','Compiled:');執行命令('java 檔案例',預期檔案)
            執行命令('java 網路例 {} {}'.format(回顯服務器條目.TCP埠,回顯服務器條目.UDP埠),'JAVA 네트워크 驗證: TCP UDP 한글')
            圖形命令='java 繪圖例'
        elif 語言=='c':
            for 名稱,已轉發值,預期 in [('輸出','', 'C 輸出: 안녕하세요 😀'),('檔案','',預期檔案),
                    ('네트워크',' '+str(回顯服務器條目.UDP埠),'C 네트워크 驗證: UDP 한글')]:
                執行命令('cc '+名稱+'範例.c -o 執行命令','Compiled native ARM64 ELF:')
                執行命令('./執行命令'+已轉發值,預期)
            執行命令('cc 繪圖例.c -o 執行命令','Compiled native ARM64 ELF:');圖形命令='./執行命令'
        else:
            for 名稱,已轉發值,預期 in [('輸出','','PYTHON 輸出: 안녕하세요 😀'),('檔案','',預期檔案),
                    ('네트워크',' '+str(回顯服務器條目.UDP埠),'PYTHON 네트워크 驗證: UDP 한글')]:
                執行命令('python '+名稱+'範例.py'+已轉發值,預期)
            圖形命令='python 繪圖例.py'
        開始繪圖=開始偏移(圖形命令)
        文本=接收消息('그림을 확인한 後端值 Enter를 누르세요.\r\n'.encode(),開始繪圖)
        assert 名稱表+' 그래픽: 빨강 초록 파랑' in 文本 and 'exit 0' not in 文本,文本
        # While EL0 waits for GUI input, kernel FTP must continue serving data.
        檔案傳送連接狀態.storbinary('STOR 도중.txt',io.BytesIO(b'FTP DURING GRAPHICS'))
        已接收個數=bytearray();檔案傳送連接狀態.retrbinary('RETR 도중.txt',已接收個數.extend);assert 已接收個數==b'FTP DURING GRAPHICS';檔案傳送連接狀態.delete('도중.txt')
        紅_綠_藍顏色=像素列列表()
        for Y_按鈕座標,像素顏色 in [(410,(255,0,0)),(435,(0,255,0)),(460,(0,0,255))]:
            偏移值=(Y_按鈕座標*640+610)*3;assert tuple(紅_綠_藍顏色[偏移值:偏移值+3])==像素顏色,(語言,Y_按鈕座標,tuple(紅_綠_藍顏色[偏移值:偏移值+3]))
        from PIL import Image
        Image.frombytes('RGB',(640,480),bytes(紅_綠_藍顏色)).save(str(結果資料/(語言+'-graphics.png')))
        已按下值(0xff0d);已按下值(0xff0d,False)
        assert 'exit 0' in 接收消息(b'jkoros-native> ',開始繪圖)
        if 語言=='java':
            開始窗口=開始偏移('java 窗口例')
            接收消息('GUI 範例 準備: 窗口例'.encode(),開始窗口)
            def 單擊值(水平位置,垂直位置):
                for 按鈕 in (1,0):客戶端.sendall(struct.pack('>BBHH',5,按鈕,水平位置,垂直位置))
            time.sleep(.3)
            上一個映像=Image.frombytes('RGB',(640,480),bytes(像素列列表()))
            單擊值(160,196)
            for _ in range(2):已按下值(0xff08);已按下值(0xff08,False)
            for 字元值 in '한글':已按下值(0x1000000|ord(字元值));已按下值(0x1000000|ord(字元值),False)
            for 重複狀態個數 in (1,2):
                運行=len(執行記錄);單擊值(180,242)
                接收消息(('GUI 問候例: 안녕하세요, 한글님! ('+str(重複狀態個數)+')').encode(),運行)
            time.sleep(.3)
            窗口繪圖=Image.frombytes('RGB',(640,480),bytes(像素列列表()))
            assert 上一個映像.crop((110,272,530,300)).tobytes()!=窗口繪圖.crop((110,272,530,300)).tobytes()
            窗口繪圖.save(str(結果資料/'java-swing.png'))
            運行=len(執行記錄);單擊值(535,105)
            assert 'exit 0' in 接收消息(b'jkoros-native> ',運行)
        # Download the guest-created bytes through FTP in the same GUI VM.
        檔案條目名稱={'java':'java.txt','c':'c.txt','python':'python.txt'}[語言]
        命令殼('cp '+檔案條目名稱+' /有效性校驗.txt')
        已接收個數=bytearray();檔案傳送連接狀態.retrbinary('RETR 有效性校驗.txt',已接收個數.extend);assert 已接收個數==預期檔案.encode()
        命令殼('echo preserved > 輸出例.'+('py' if 語言=='python' else 語言))
        assert 'EXAMPLES READY' in 命令殼('example '+語言)
        assert '\npreserved\n' in 命令殼('cat 輸出例.'+('py' if 語言=='python' else 語言))
        assert '한/零操作數 鍵值, Shift+Space 또는 F9' in 命令殼('help ko')
        # VNC input remains usable while the FTP control/data connections are active.
        assert 'GUI NETWORK TOGETHER' in 命令殼('echo GUI NETWORK TOGETHER')
        檔案傳送連接狀態.quit();檔案傳送連接狀態=None;assert 'FTP stopped' in 命令殼('ftpd stop')
        print('PASS '+語言+': Korean output, file bytes, external network and framebuffer in desktop+network VM',flush=True)
    finally:
        if 檔案傳送連接狀態:
            try:檔案傳送連接狀態.close()
            except OSError:pass
        if 客戶端:客戶端.close()
        程序.terminate()
        try:程序.wait(timeout=8)
        except subprocess.TimeoutExpired:程序.kill();程序.wait()
        就緒選擇器.close();程序.stdout.close();(結果資料/(語言+'-serial.log')).write_bytes(執行記錄)


def 運行():
    結果資料=項目根/'build/verification/examples';結果資料.mkdir(parents=True,exist_ok=True)
    有效性驗證報告={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((項目根/'build/kernel8.img').read_bytes()).hexdigest(),'languages':[]}
    try:
        with 回顯服務器列() as 回顯服務器條目:
            for 語言 in ('java','c','python'):
                測試語言(語言,回顯服務器條目,結果資料);有效性驗證報告['languages'].append(語言)
            預期=[('tcp','JAVA TCP 한글\n'),('udp','JAVA UDP 한글'),('udp','C UDP 한글'),('udp','PYTHON UDP 한글')]
            assert 回顯服務器條目.擁有已接收==[(分類值,資料.encode()) for 分類值,資料 in 預期],回顯服務器條目.擁有已接收
            有效性驗證報告['host_network_payloads']=[{'protocol':分類值,'text':資料.decode()} for 分類值,資料 in 回顯服務器條目.擁有已接收]
        有效性驗證報告.update(passed=True,examples_executed=13,graphics_pixel_checks=9,
                      swing_example_korean_input_button_label_and_close=True,
                      same_vm_vnc_and_ftp=True,ftp_while_graphics_waits=True,guest_examples_preserve_existing_files=True,
                      examples_present_at_boot=True,all_embedded_file_hashes_match=True,
                      full_16k_binary_copy_and_ftp_listing_above_slot_16=True)
    finally:(結果資料/'report.json').write_text(json.dumps(有效性驗證報告,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':運行()

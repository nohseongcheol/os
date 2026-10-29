#!/usr/bin/env python3
"""Exercise the installed Remmina in an isolated X display and D-Bus session.

Needs Remmina's VNC plugin, xdotool, Xvfb (or the existing ARM64 Xvfb rootfs
and qemu-aarch64), dbus-run-session, and ImageMagick import. Never uses :0.
"""
import hashlib
import json
import os
from pathlib import Path
import re
import selectors
import shutil
import subprocess
import tempfile
import time
from 執行命令 import 項目根


def 運行():
    結果資料=項目根/'build/verification/remmina';結果資料.mkdir(parents=True,exist_ok=True)
    有效性驗證報告={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((項目根/'build/kernel8.img').read_bytes()).hexdigest()}
    with tempfile.TemporaryDirectory(prefix='jkoros-remmina-') as 工作中路徑:
        工作中路徑=Path(工作中路徑);運行中程序列=[];就緒選擇器=selectors.DefaultSelector();串行輸入輸出=bytearray()
        日誌記錄列=[]
        try:
            虛擬顯示操作=shutil.which('Xvfb')
            if 虛擬顯示操作: 服務器值=[虛擬顯示操作]
            else:
                根文件系統=項目根.parent/'rpi4/build/rootfs'
                服務器值=['qemu-aarch64','-L',str(根文件系統),str(根文件系統/'usr/bin/Xvfb')]
            def 運行(實際參數陣列,環境=None,**已命名實際參數):
                日誌記錄=(結果資料/('process-%d.log'%len(日誌記錄列))).open('wb');日誌記錄列.append(日誌記錄)
                資料位置=subprocess.Popen(實際參數陣列,env=環境,stdout=日誌記錄,stderr=subprocess.STDOUT,**已命名實際參數)
                運行中程序列.append(資料位置);return 資料位置
            環境=dict(os.environ)
            for 名稱 in ('DISPLAY','WAYLAND_DISPLAY','DBUS_SESSION_BUS_ADDRESS','XAUTHORITY'):環境.pop(名稱,None)
            環境.update(GTK_IM_MODULE='gtk-im-context-simple',NO_AT_BRIDGE='1',
                XDG_CONFIG_HOME=str(工作中路徑/'config'),XDG_DATA_HOME=str(工作中路徑/'data'),XDG_CACHE_HOME=str(工作中路徑/'cache'))
            數值值=next(項目個數 for 項目個數 in range(80,200) if not Path('/tmp/.X11-unix/X'+str(項目個數)).exists() and not Path('/tmp/.X%d-lock'%項目個數).exists())
            環境['DISPLAY']=':'+str(數值值)
            顯示操作設備=運行(服務器值+[環境['DISPLAY'],'-screen','0','1024x768x24','-nolisten','tcp','-ac','-noreset','-extension','GLX'],環境=環境)
            截止時間時間=time.monotonic()+30
            while True:
                assert 顯示操作設備.poll() is None and time.monotonic()<截止時間時間,'Xvfb failed; see process-0.log'
                準備狀態完成=subprocess.run(['xdotool','getdisplaygeometry'],env=環境,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
                if 準備狀態完成.returncode==0:break
                time.sleep(.1)
            客戶機=subprocess.Popen(['python3',str(項目根/'工具集/執行命令.py'),'--desktop','--port','0'],
                stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            運行中程序列.append(客戶機);就緒選擇器.register(客戶機.stdout,selectors.EVENT_READ)
            def 等待(標記,偏移值=0):
                截止時間時間=time.monotonic()+45
                while 標記 not in 串行輸入輸出[偏移值:]:
                    assert 客戶機.poll() is None and time.monotonic()<截止時間時間,串行輸入輸出[偏移值:].decode('utf-8','replace')
                    for 已按下值,_ in 就緒選擇器.select(.1):
                        資料=已按下值.fileobj.read(65536)
                        if 資料:串行輸入輸出.extend(資料)
            等待(b'TERMINAL READY');等待(b'jkoros-native> ',串行輸入輸出.rfind(b'TERMINAL READY'))
            埠編號=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',串行輸入輸出).group(1))
            配置檔=工作中路徑/'test.remmina'
            配置檔.write_text('[remmina]\nname=JKOROS_KOREAN_TEST\nprotocol=VNC\nserver=127.0.0.1:%d\nviewmode=1\nquality=9\ncolordepth=32\nscale=0\nviewonly=0\n'%埠編號)
            運行(['dbus-run-session','--','remmina','-c',str(配置檔)],環境=環境,start_new_session=True)
            def 虛擬輸入工具(*實際參數陣列):return subprocess.check_output(['xdotool']+list(實際參數陣列),env=環境,stderr=subprocess.STDOUT)
            截止時間時間=time.monotonic()+60;窗口=None
            while time.monotonic()<截止時間時間:
                搜索結果=subprocess.run(['xdotool','search','--onlyvisible','--name','JKOROS_KOREAN_TEST'],env=環境,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
                if 搜索結果.returncode==0:
                    候選=搜索結果.stdout.splitlines()[-1].decode()
                    time.sleep(.5)
                    已聚焦=subprocess.run(['xdotool','windowfocus','--sync',候選],env=環境,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
                    if 已聚焦.returncode==0:窗口=候選;break
                time.sleep(.1)
            assert 窗口,'Remmina window not found'
            # Click the VNC surface, away from its toolbar and title bar.
            虛擬輸入工具('mousemove','--window',窗口,'280','240','click','1')
            time.sleep(1)
            def 已輸入字元(文本):虛擬輸入工具('type','--clearmodifiers','--delay','50',文本)
            def 已按下值(*已按下鍵列):虛擬輸入工具('key','--clearmodifiers',*已按下鍵列)
            偏移值=len(串行輸入輸出);已輸入字元('echo ');已按下值('F9');已輸入字元('dkssudgktpdy gksrmf');已按下值('F9','Return')
            等待('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),偏移值)
            偏移值=len(串行輸入輸出);已輸入字元('echo ');已按下值('shift+space');已輸入字元('rhk rkqtk');已按下值('shift+space','Return')
            等待('\r\n과 갑사\r\njkoros-native> '.encode(),偏移值)
            偏移值=len(串行輸入輸出);已輸入字元('help ko');已按下值('Return')
            等待('한/零操作數 鍵值, Shift+Space 또는 F9'.encode(),偏移值);等待(b'jkoros-native> ',偏移值)
            偏移值=len(串行輸入輸出);已輸入字元('echo ');已按下值('F9');已輸入字元('gksrmf dlfr')
            等待('읽'.encode(),偏移值)
            subprocess.check_call(['import','-display',環境['DISPLAY'],'-window',窗口,str(結果資料/'remmina-korean.png')])
            已按下值('F9','Return')
            等待(b'jkoros-native> ',偏移值)
            # 實際資料 Remmina의 屏幕 여백을 찾아 게스트 모서리를 왼쪽으로 끈다.
            from PIL import Image
            繪圖=Image.open(str(結果資料/'remmina-korean.png')).convert('RGB')
            標題欄=None
            for 垂直位置 in range(繪圖.height):
                水平位置列=[水平位置 for 水平位置 in range(繪圖.width) if 繪圖.getpixel((水平位置,垂直位置))==(32,80,144)]
                if len(水平位置列)>=500:標題欄=(min(水平位置列),垂直位置);break
            assert 標題欄,'native terminal title bar not found'
            水平位置,垂直位置=標題欄[0]+564,標題欄[1]+356
            虛擬輸入工具('mousemove','--window',窗口,str(水平位置),str(垂直位置))
            def 等待狀態用於位圖(名稱,點列列表):
                截止時間值=time.monotonic()+15
                while True:
                    subprocess.check_call(['import','-display',環境['DISPLAY'],'-window',窗口,str(結果資料/名稱)])
                    位圖映像=Image.open(str(結果資料/名稱)).convert('RGB')
                    if all(位圖映像.getpixel(位置)==顏色 for 位置,顏色 in 點列列表):return
                    assert time.monotonic()<截止時間值,'Remmina framebuffer did not settle: '+名稱
                    time.sleep(.1)
            等待狀態用於位圖('remmina-resize-cursor.png',[
                ((水平位置-7,垂直位置-7),(255,255,255)),((水平位置+7,垂直位置+7),(255,255,255))])
            虛擬輸入工具('mousedown','1','mousemove','--window',窗口,str(水平位置-120),str(垂直位置-80),'mouseup','1')
            time.sleep(.4)
            偏移值=len(串行輸入輸出);已輸入字元('terminal size');已按下值('Return')
            等待(b'TERMINAL SIZE 53x14\r\n',偏移值)
            虛擬輸入工具('mousemove','--window',窗口,'500','45')
            等待狀態用於位圖('remmina-resized.png',[
                ((標題欄[0]+447,標題欄[1]+279),(39,49,64)),((水平位置,垂直位置),(24,32,48))])
            if shutil.which('dpkg-query'):
                版本編號=subprocess.check_output(['dpkg-query','-W','-f','${Version}','remmina']).decode().strip()
            else:
                版本編號=subprocess.check_output(['remmina','--version'],env=環境,stderr=subprocess.STDOUT).decode('utf-8','replace')
            有效性驗證報告.update(passed=True,display=環境['DISPLAY'],remmina_version=版本編號,
                checks=['actual Remmina VNC client, isolated X display and D-Bus',
                        'English ASCII keys -> F9 -> Korean composition -> English',
                        'Shift+Space toggles with compound vowels/final splitting',
                        'guest help ko advertises implemented shortcuts','KO title and Korean guest text screenshot',
                        'actual Remmina left-button corner resize changes grid to 53x14'])
            print('PASS: actual Remmina F9/Shift+Space Korean input and help',flush=True)
        finally:
            if not 有效性驗證報告['passed'] and '環境' in locals() and 環境.get('DISPLAY','').startswith(':'):
                try:
                    subprocess.run(['import','-display',環境['DISPLAY'],'-window','root',str(結果資料/'failure.png')],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=10)
                except (OSError,subprocess.TimeoutExpired):pass
            for 資料位置 in reversed(運行中程序列):
                if 資料位置.poll() is None:
                    if 資料位置.args[0]=='dbus-run-session':
                        import signal
                        os.killpg(資料位置.pid,signal.SIGTERM)
                    else:資料位置.terminate()
                    try:資料位置.wait(timeout=5)
                    except subprocess.TimeoutExpired:資料位置.kill();資料位置.wait()
            就緒選擇器.close()
            for 檔案條目 in 日誌記錄列:檔案條目.close()
            (結果資料/'serial.log').write_bytes(串行輸入輸出)
            (結果資料/'report.json').write_text(json.dumps(有效性驗證報告,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':運行()

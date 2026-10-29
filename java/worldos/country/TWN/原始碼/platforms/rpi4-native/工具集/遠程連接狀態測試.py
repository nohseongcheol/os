#!/usr/bin/env python3
"""實際資料 OpenSSH 클라이언트와 RFB 클라이언트로 게스트 서비스를 검증한다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import socket
import struct
import subprocess
import tempfile
import threading
import time
import selectors
from Crypto.Cipher import DES
from 執行命令 import 項目根, 命令
from 網路橋接 import 網路橋接


def 運行():
    解析器 = argparse.ArgumentParser(description=__doc__)
    解析器.add_argument('--kernel', type=Path, default=項目根 / 'build/kernel8.img')
    解析器.add_argument('--access', type=Path, default=項目根 / 'build/remote/access.json')
    解析器.add_argument('--output', type=Path, default=項目根 / 'build/verification/native-remote')
    實參 = 解析器.parse_args()
    輸出 = 實參.output
    輸出.mkdir(parents=True, exist_ok=True)
    設置 = json.loads(實參.access.read_text())
    報告值 = {'passed': False, 'physical_board_tested': False, 'linux_loaded': False,
          'kernel_sha256': hashlib.sha256(實參.kernel.read_bytes()).hexdigest(), 'checks': []}
    def 空埠():
        with socket.socket() as 連接:
            連接.bind(('127.0.0.5', 0))
            return 連接.getsockname()[1]
    命令殼埠, 屏幕埠, 檔案埠 = 空埠(), 空埠(), 空埠()
    日誌記錄 = bytearray()
    程序值 = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-remote-') as 臨時值, 網路橋接(檔案埠,
                ['tcp:{}:22'.format(命令殼埠), 'tcp:{}:5900'.format(屏幕埠)], 宿主地址='127.0.0.5') as 橋接值:
            運行參數 = 命令()
            運行參數[運行參數.index('-kernel') + 1] = str(實參.kernel.resolve())
            程序值 = subprocess.Popen(運行參數 + ['-display','none','-monitor','none','-serial','stdio'] + 橋接值.已轉發實際參數(),
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            def 彙集值列():
                while True:
                    資料 = 程序值.stdout.read(4096)
                    if not 資料: break
                    日誌記錄.extend(資料)
            執行緒值 = threading.Thread(target=彙集值列, daemon=True)
            執行緒值.start()
            def 等待狀態狀態(機器字文本, 初始項目=0, 限制值=60):
                結尾 = time.monotonic() + 限制值
                while 機器字文本 not in 日誌記錄[初始項目:]:
                    if time.monotonic()>結尾 or 程序值.poll() is not None:
                        raise AssertionError('Missing '+repr(機器字文本)+'\n'+日誌記錄[初始項目:].decode('utf-8','replace'))
                    time.sleep(.02)
            等待狀態狀態(b'jkoros-native> ')
            輔助器值 = Path(臨時值)/'askpass'
            輔助器值.write_text('#!/usr/bin/python3\nimport os\nprint(os.environ["JKOROS_TEST_PASSWORD"])\n')
            輔助器值.chmod(0o700)
            環境 = dict(os.environ, DISPLAY=':999', SSH_ASKPASS=str(輔助器值), SSH_ASKPASS_REQUIRE='force')
            def 安全命令殼(密碼值, 指令值, 追加條目=()):
                環境['JKOROS_TEST_PASSWORD']=密碼值
                實參=['ssh','-v']+list(追加條目)+['-p',str(命令殼埠),'-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile='+str(Path(臨時值)/'known_hosts'),
                    '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1',
                    '-o','ConnectTimeout=20','user@127.0.0.5',指令值]
                結果=subprocess.run(實參,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                                    env=環境,start_new_session=True,timeout=50)
                return 結果
            結果=安全命令殼('!' + 設置['ssh_password'], 'echo SHOULD_NOT_RUN')
            (輸出/'ssh-rejected.log').write_bytes(結果.stderr)
            assert 結果.returncode!=0 and b'Permission denied' in 結果.stderr and b'SHOULD_NOT_RUN' not in 日誌記錄, 結果.stderr
            報告值['checks'].append('SSH incorrect password rejected')
            time.sleep(.5)
            結果=安全命令殼(設置['ssh_password'], 'echo SSH_NATIVE_PASS')
            (輸出/'ssh.log').write_bytes(結果.stderr)
            (輸出/'ssh-output.txt').write_bytes(結果.stdout)
            assert 結果.returncode==0 and b'SSH_NATIVE_PASS' in 結果.stdout, (結果.returncode,結果.stdout,結果.stderr)
            報告值['checks'].append('OpenSSH password authentication and native shell exec')
            assert b'cipher: aes128-ctr MAC: hmac-sha2-256' in 結果.stderr, 結果.stderr
            報告值['checks'].append('Negotiated allowlisted AES-CTR / HMAC-SHA256')
            print('SSH authentication / exec PASS',flush=True)
            time.sleep(.3)
            結果=安全命令殼(設置['ssh_password'], 'cd /example/java; java 輸出例; cd /')
            assert 結果.returncode==0 and 'JAVA 輸出: 안녕하세요 😀'.encode() in 結果.stdout,結果.stdout
            報告值['checks'].append('SSH executes EL0 Java example with UTF-8 output')
            time.sleep(.3)
            結果=安全命令殼(設置['ssh_password'], 'missing_remote_command')
            assert 結果.returncode==127,結果.returncode
            報告值['checks'].append('SSH nonzero command exit status')
            time.sleep(.3)
            結果=安全命令殼(設置['ssh_password'], 'cat /example/java/窗口例.java', ('-o', 'RekeyLimit=1K'))
            (輸出/'ssh-rekey.log').write_bytes(結果.stderr)
            assert 結果.returncode==0 and 'class 窗口例'.encode() in 結果.stdout, (結果.returncode,結果.stdout,結果.stderr)
            assert 結果.stderr.count(b'SSH2_MSG_NEWKEYS received')>=2, 結果.stderr
            報告值['checks'].append('OpenSSH rekey during native command output')
            time.sleep(.3)
            交互式參數列=['ssh','-tt','-p',str(命令殼埠),'-o','StrictHostKeyChecking=yes','-o','UserKnownHostsFile='+str(Path(臨時值)/'known_hosts'),
                '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1','user@127.0.0.5']
            交互式會話=subprocess.Popen(交互式參數列,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=環境,start_new_session=True,bufsize=0)
            執行記錄=bytearray();選中狀態值=selectors.DefaultSelector();選中狀態值.register(交互式會話.stdout,selectors.EVENT_READ)
            def 讀取交互式(顯示值):
                截止時間值=time.monotonic()+30
                while 顯示值 not in 執行記錄:
                    if time.monotonic()>截止時間值 or 交互式會話.poll() is not None:raise AssertionError('SSH interactive missing '+repr(顯示值)+' '+repr(bytes(執行記錄)))
                    for 條目值,_ in 選中狀態值.select(.1):
                        片段值=條目值.fileobj.read(4096)
                        if 片段值:執行記錄.extend(片段值)
            try:
                讀取交互式(b'shared native console')
                交互式會話.stdin.write(b'echo SSH_INTERACTIVE_PASS\r');交互式會話.stdin.flush();讀取交互式(b'\r\nSSH_INTERACTIVE_PASS\r\n')
                交互式會話.stdin.write(b'\x04');交互式會話.stdin.flush();餘數值,錯誤=交互式會話.communicate(timeout=15)
                assert 交互式會話.returncode==0 and b'PTY allocation request failed' not in 錯誤,(交互式會話.returncode,錯誤)
                (輸出/'ssh-interactive.txt').write_bytes(執行記錄+餘數值)
            finally:
                選中狀態值.close()
                if 交互式會話.poll() is None:交互式會話.kill();交互式會話.wait()
            報告值['checks'].append('SSH interactive terminal request, command, Ctrl-D disconnect')
            def 精確地值(連接, 數):
                資料=bytearray()
                while len(資料)<數:
                    塊片值=連接.recv(數-len(資料))
                    if not 塊片值: raise AssertionError('RFB EOF')
                    資料.extend(塊片值)
                return bytes(資料)
            def 屏幕身份驗證(密碼值):
                連接=socket.create_connection(('127.0.0.5',屏幕埠),10);連接.settimeout(30)
                assert 精確地值(連接,12)==b'RFB 003.008\n'
                連接.sendall(b'RFB 003.008\n');assert 精確地值(連接,2)==b'\x01\x02'
                連接.sendall(b'\x02');挑戰值=精確地值(連接,16)
                輸入密碼=密碼值.encode('ascii')[:8].ljust(8, b'\0')
                鍵材料=bytes(int('{:08b}'.format(數)[::-1],2) for 數 in 輸入密碼)
                連接.sendall(DES.new(鍵材料,DES.MODE_ECB).encrypt(挑戰值))
                狀態值=struct.unpack('!I',精確地值(連接,4))[0]
                return 連接,狀態值
            無效密碼='!' if not 設置['vnc_password'].startswith('!') else '?'
            連接,狀態值=屏幕身份驗證(無效密碼);assert 狀態值==1;連接.close();time.sleep(.6)
            報告值['checks'].append('VNC incorrect password rejected')
            連接,狀態值=屏幕身份驗證(設置['vnc_password']);assert 狀態值==0
            with 連接:
                連接.sendall(b'\x01');初始狀態=精確地值(連接,24);寬度值,高度值=struct.unpack('!HH',初始狀態[:4]);名稱=精確地值(連接,struct.unpack('!I',初始狀態[20:24])[0])
                assert (寬度值,高度值)==(640,480) and b'jkoros native'==名稱
                def 屏幕(遞增步驟=0):
                    連接.sendall(struct.pack('!BBHHHH',3,遞增步驟,0,0,寬度值,高度值));頭值=精確地值(連接,4);數=struct.unpack('!H',頭值[2:])[0];總計值=0
                    繪圖=bytearray(寬度值*高度值*4)
                    for _ in range(數):
                        橫座標座標,Y_按鈕座標,區域寬度,區域高度,方法模式=struct.unpack('!HHHHi',精確地值(連接,12));assert 方法模式==0 and 橫座標座標+區域寬度<=寬度值 and Y_按鈕座標+區域高度<=高度值
                        像素=精確地值(連接,區域寬度*區域高度*4);總計值+=len(像素)
                        for 行 in range(區域高度):繪圖[((Y_按鈕座標+行)*寬度值+橫座標座標)*4:((Y_按鈕座標+行)*寬度值+橫座標座標+區域寬度)*4]=像素[行*區域寬度*4:(行+1)*區域寬度*4]
                    if not 遞增步驟:
                        from PIL import Image
                        Image.frombytes('RGB',(寬度值,高度值),bytes(繪圖),'raw','BGRX').save(str(輸出/'native-vnc.png'))
                    return 數,總計值
                數,總計值=屏幕();assert 數>0 and 總計值==寬度值*高度值*4
                報告值['checks'].append('Native framebuffer RFB full update {} bytes'.format(總計值))
                數,總計值=屏幕(1);assert 總計值<寬度值*高度值*4
                報告值['checks'].append('RFB incremental update')
                初始項目=len(日誌記錄)
                for 字元值 in 'echo VNC_NATIVE_PASS\r':
                    符號=0xff0d if 字元值=='\r' else ord(字元值)
                    連接.sendall(struct.pack('!BBHI',4,1,0,符號));連接.sendall(struct.pack('!BBHI',4,0,0,符號))
                等待狀態狀態(b'VNC_NATIVE_PASS',初始項目)
                報告值['checks'].append('Authenticated VNC keyboard executes guest shell command')
                def 鍵筆畫(符號,按下值=1):連接.sendall(struct.pack('!BBHI',4,按下值,0,符號))
                初始項目=len(日誌記錄)
                for 字元值 in 'echo ':鍵筆畫(ord(字元值))
                鍵筆畫(0xffc6)
                for 字元值 in 'gksrmf':鍵筆畫(ord(字元值))
                鍵筆畫(0xffc6);鍵筆畫(0xff0d)
                等待狀態狀態('\r\n한글\r\n'.encode(),初始項目)
                報告值['checks'].append('Native VNC F9 two-set Hangul composition')
                連接.sendall(struct.pack('!BBHH',5,0,120,100))
                報告值['checks'].append('VNC pointer input accepted')
            程序值.stdin.write(b'poweroff\n');程序值.stdin.flush();程序值.wait(timeout=15);assert 程序值.returncode==0
            報告值['passed']=True
    finally:
        if 程序值 and 程序值.poll() is None:
            程序值.terminate()
            try: 程序值.wait(timeout=5)
            except subprocess.TimeoutExpired: 程序值.kill();程序值.wait()
        (輸出/'serial.log').write_bytes(日誌記錄)
        (輸出/'report.json').write_text(json.dumps(報告值,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(報告值,ensure_ascii=False,indent=2))


if __name__=='__main__': 運行()

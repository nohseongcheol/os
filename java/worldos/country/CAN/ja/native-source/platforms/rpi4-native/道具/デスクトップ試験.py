#!/usr/bin/env python3
"""実際データ RFB 클라이언트로 QEMU 창의 한글/キー値/클립보드/마우스와 画面 전송을 검사한다."""
import hashlib
import json
import re
import selectors
import socket
import struct
import subprocess
import time
from pathlib import Path
from デスクトップ表示像 import 厳密値
from 命令実行 import 計画根


def 起動処理():
    出力結果=計画根/'build/verification/desktop'; 出力結果.mkdir(parents=True,exist_ok=True)
    プロセス=subprocess.Popen(['python3',str(計画根/'道具/デスクトップ表示像.py'),'--port','0'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    準備状態監視器=selectors.DefaultSelector(); 準備状態監視器.register(プロセス.stdout,selectors.EVENT_READ)
    実行記録=bytearray(); 妥当性報告={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((計画根/'build/kernel8.img').read_bytes()).hexdigest()}
    def 到達待ち(標識,起動処理=0):
        期限時間=time.monotonic()+45
        while 標識 not in 実行記録[起動処理:]:
            if time.monotonic()>期限時間 or プロセス.poll() is not None: raise AssertionError(実行記録[起動処理:].decode('utf-8','replace'))
            for 押下済み値,_ in 準備状態監視器.select(.1):
                データ=押下済み値.fileobj.read(4096)
                if データ: 実行記録.extend(データ)
        return bytes(実行記録[起動処理:])
    try:
        到達待ち(b'TERMINAL READY')
        ポート番号=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',実行記録).group(1))
        with socket.create_connection(('127.0.0.1',ポート番号),timeout=10) as 接続元:
            assert 厳密値(接続元,12)==b'RFB 003.008\n'; 接続元.sendall(b'RFB 003.008\n')
            assert 1 in 厳密値(接続元,厳密値(接続元,1)[0]); 接続元.sendall(b'\x01'); assert 厳密値(接続元,4)==b'\0'*4
            接続元.sendall(b'\x01'); 初期値=厳密値(接続元,24); assert struct.unpack('>HH',初期値[:4])==(640,480); 厳密値(接続元,struct.unpack('>I',初期値[20:])[0])
            接続元.sendall(b'\x00\x00\x00\x00'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
            接続元.sendall(struct.pack('>BBHi',2,0,1,0))
            def 押下済み値(記号値,判定押下中=True): 接続元.sendall(struct.pack('>BBHI',4,int(判定押下中),0,記号値))
            def 型付き文字(文):
                for 文字データ in 文:
                    記号=0xff0d if 文字データ=='\n' else ord(文字データ) if ord(文字データ)<256 else 0x01000000|ord(文字データ)
                    押下済み値(記号); 押下済み値(記号,False)
            def 押下キー(記号値): 押下済み値(記号値); 押下済み値(記号値,False)
            # Start with English keys only, as delivered without a host IME.
            変位量値=len(実行記録); 型付き文字('echo '); 押下キー(0xffc6)
            型付き文字('dkssudgktpdy gksrmf'); 押下キー(0xffc6); 型付き文字('\n')
            到達待ち('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),変位量値)
            変位量値=len(実行記録); 型付き文字('echo ')
            押下済み値(0xffe1); 押下キー(32); 押下済み値(0xffe1,False)
            型付き文字('dlfr'); 押下キー(0xff08); 押下キー(0xff08); 型付き文字('fr')
            押下キー(0xff31); 型付き文字(' EN\n')
            到達待ち('\r\n읽 EN\r\njkoros-native> '.encode(),変位量値)
            変位量値=len(実行記録); 型付き文字('echo '); 押下キー(0xff31)
            型付き文字('rhk rkqtk RkRnd'); 押下キー(0xff31); 型付き文字('\n')
            到達待ち('\r\n과 갑사 까꿍\r\njkoros-native> '.encode(),変位量値)
            # The same composition edits UTF-8 text in the native vi editor.
            変位量値=len(実行記録); 型付き文字('vi ハングル入力.txt\n'); 到達待ち(b'NORMAL',変位量値)
            型付き文字('i'); 押下キー(0xffc6); 型付き文字('gksrmf dlfr'); 押下キー(0xffc6)
            押下キー(0xff1b); 型付き文字(':wq\n'); 到達待ち(b'jkoros-native> ',変位量値)
            変位量値=len(実行記録); 型付き文字('cat ハングル入力.txt\n')
            到達待ち('한글 읽'.encode(),変位量値); 到達待ち(b'jkoros-native> ',変位量値)
            変位量値=len(実行記録); 型付き文字('help ko\n')
            到達待ち('한/零被演算子 キー値, Shift+Space 또는 F9'.encode(),変位量値); 到達待ち(b'jkoros-native> ',変位量値)
            変位量値=len(実行記録); 型付き文字('clear\necho "VNC 한글 入力値 😀"\n'); 到達待ち('VNC 한글 入力値 😀\r\n'.encode(),変位量値)
            変位量値=len(実行記録); 押下済み値(0xffe3); 押下済み値(ord('u')); 押下済み値(ord('u'),False); 押下済み値(0xffe3,False); 型付き文字('echo CONTROL_OK\n'); 到達待ち(b'\r\nCONTROL_OK\r\n',変位量値)
            # A shared clipboard is not a paste command. Require explicit Ctrl+Shift+V.
            貼付け板値='echo "貼付け値 判定完了"\n'.encode(); 変位量値=len(実行記録)
            接続元.sendall(struct.pack('>B3xI',6,len(貼付け板値))+貼付け板値)
            for イベント,_ in 準備状態監視器.select(.15):
                データブロック=イベント.fileobj.read(4096)
                if データブロック: 実行記録.extend(データブロック)
            assert '貼付け値 判定完了'.encode() not in 実行記録[変位量値:]
            押下済み値(0xffe3); 押下済み値(0xffe1); 押下済み値(ord('v')); 押下済み値(ord('v'),False); 押下済み値(0xffe1,False); 押下済み値(0xffe3,False)
            # The prompt follows the guest's terminal redraw after command completion.
            到達待ち('\r\n붙여넣기 判定完了\r\njkoros-native> '.encode(),変位量値)
            接続元.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
            RGB色=bytearray(640*480*3); 確認済み登録項目一覧=False
            while not 確認済み登録項目一覧:
                通知本文=厳密値(接続元,1)[0]
                if 通知本文==2: continue
                if 通知本文==3:
                    容量=struct.unpack('>I',厳密値(接続元,7)[3:])[0]; 厳密値(接続元,容量); continue
                assert 通知本文==0,通知本文
                矩形一覧一覧=struct.unpack('>H',厳密値(接続元,3)[1:])[0]
                for _ in range(矩形一覧一覧):
                    横座標,縦座標,要求済み幅値,要求済み高さ値,文字設定=struct.unpack('>HHHHi',厳密値(接続元,12)); assert 文字設定==0,文字設定
                    画素列一覧=厳密値(接続元,要求済み幅値*要求済み高さ値*4)
                    for 内側序数 in range(要求済み高さ値):
                        for 序数添字 in range(要求済み幅値):
                            原本番地=(内側序数*要求済み幅値+序数添字)*4; 宛先番地=((縦座標+内側序数)*640+横座標+序数添字)*3
                            RGB色[宛先番地:宛先番地+3]=bytes((画素列一覧[原本番地+2],画素列一覧[原本番地+1],画素列一覧[原本番地]))
                    確認済み登録項目一覧=True
            assert RGB色[(48*640+12)*3:(48*640+12)*3+3]==bytes((32,80,144))
            (出力結果/'vnc-terminal.ppm').write_bytes(b'P6\n640 480\n255\n'+RGB色)
            from PIL import Image
            Image.frombytes('RGB',(640,480),bytes(RGB色)).save(str(出力結果/'vnc-terminal.png'))
            変位量値=len(実行記録)
            押下済み値(0xffe3); 押下済み値(0xffe1); 押下済み値(ord('t')); 押下済み値(ord('t'),False); 押下済み値(0xffe1,False); 押下済み値(0xffe3,False)
            到達待ち(b'TERMINAL FOCUS 2',変位量値)
            変位量値=len(実行記録); 型付き文字('echo SECOND_VNC_WINDOW\n'); 到達待ち(b'\r\nSECOND_VNC_WINDOW\r\n',変位量値)
            変位量値=len(実行記録); 接続元.sendall(struct.pack('>BBHH',5,1,576,81)); 接続元.sendall(struct.pack('>BBHH',5,0,576,81)); 到達待ち(b'TERMINAL FOCUS 1',変位量値)
            変位量値=len(実行記録); 型付き文字('python -c \'print("x"*9000)\'\n'); 到達待ち(b'\r\njkoros-native> ',変位量値)
            assert len(実行記録)-変位量値>8192,'exercise output longer than bridge status buffer'
            変位量値=len(実行記録); 接続元.sendall(struct.pack('>BBHH',5,1,560,63)); 接続元.sendall(struct.pack('>BBHH',5,0,560,63)); 到達待ち(b'TERMINAL FOCUS 1',変位量値)
            変位量値=len(実行記録); 接続元.sendall(struct.pack('>BBHH',5,1,80,16)); 接続元.sendall(struct.pack('>BBHH',5,0,80,16)); 到達待ち(b'TERMINAL FOCUS 1',変位量値)
            変位量値=len(実行記録); 型付き文字('echo REOPENED_VNC_WINDOW\n'); 到達待ち(b'\r\nREOPENED_VNC_WINDOW\r\n',変位量値)
            変位量値=len(実行記録); 型付き文字('gui\n'); 到達待ち(b'GUI READY:',変位量値)
            変位量値=len(実行記録); 接続元.sendall(struct.pack('>BBHH',5,1,80,332)); 接続元.sendall(struct.pack('>BBHH',5,0,80,332)); 到達待ち(b'TERMINAL READY',変位量値)
            妥当性報告.update(passed=True,checks=['RFB 3.8 handshake and actual 640x480 raw framebuffer','F9, Shift+Space and Hangul toggle: ASCII two-set keys compose Korean in shell and vi','compound vowels/finals, resyllabification and composition Backspace','help ko lists implemented shortcuts','Unicode Hangul/emoji keysyms -> guest shell','Ctrl modifiers and explicit clipboard paste; no clipboard auto-execution','Ctrl+Shift+T creates second native terminal, mouse X closes it','mouse close after 9 KiB output, desktop new-terminal button and legacy launcher button'])
        print('PASS: actual VNC keyboard/Unicode/paste/mouse/framebuffer -> native terminal')
    finally:
        if プロセス.poll() is None:
            プロセス.terminate()
            try: プロセス.wait(timeout=8)
            except subprocess.TimeoutExpired: プロセス.kill(); プロセス.wait()
        準備状態監視器.close(); プロセス.stdout.close()
        (出力結果/'serial.log').write_bytes(実行記録)
        (出力結果/'report.json').write_text(json.dumps(妥当性報告,indent=2)+'\n')


if __name__=='__main__': 起動処理()

#!/usr/bin/env python3
"""RFB 화면은 QEMU에서, 鍵值 입력은 內建 內核值 UART로 전달한다. localhost 전용, 단일 控制值 클라이언트.
RFB 3.8: https://www.rfc-editor.org/rfc/rfc6143.html
"""
import argparse
from contextlib import ExitStack
from pathlib import Path
import signal
import socket
import struct
import subprocess
import sys
import tempfile
import threading
import time
from 執行命令 import 命令
from local_input import create


def 精確值(通訊端值, 大小):
    資料 = bytearray()
    while len(資料) < 大小:
        片段值 = 通訊端值.recv(大小 - len(資料))
        if not 片段值: raise EOFError()
        資料.extend(片段值)
    return bytes(資料)


class 鍵盤:
    def __init__(自身值, 發送, 模式已更改=None):
        自身值.傳送位元組列 = 發送; 自身值.修飾符鍵 = set(); 自身值.剪貼板值 = b''
        自身值.韓文字母組合器 = create(發送, Path(__file__).resolve().parents[1]); 自身值.韓語 = False; 自身值.切換鍵 = set()
        自身值.Unicode輸入 = None
        自身值.模式已更改 = 模式已更改
        if 模式已更改: 模式已更改(False)

    def 發送(自身值, 資料):
        自身值.韓文字母組合器.提交合成狀態()
        自身值.傳送位元組列(資料)

    def 切換模式(自身值):
        自身值.韓文字母組合器.提交合成狀態(); 自身值.韓語 = not 自身值.韓語
        if 自身值.模式已更改: 自身值.模式已更改(自身值.韓語)

    def 已按下值(自身值, 是否按下中, 鍵符號):
        if 鍵符號 in (0xffe1, 0xffe2, 0xffe3, 0xffe4, 0xffe9, 0xffea, 0xfe03, 0xff7e):
            if 是否按下中: 自身值.修飾符鍵.add(鍵符號)
            else: 自身值.修飾符鍵.discard(鍵符號)
            return
        if not 是否按下中:
            自身值.切換鍵.discard(鍵符號)
            return
        控制鍵 = bool(自身值.修飾符鍵 & {0xffe3, 0xffe4})
        移位鍵 = bool(自身值.修飾符鍵 & {0xffe1, 0xffe2})
        if 控制鍵 and 移位鍵 and 鍵符號 in (ord('u'),ord('U')):
            自身值.韓文字母組合器.提交合成狀態(); 自身值.Unicode輸入 = ''; return
        if 自身值.Unicode輸入 is not None:
            if 鍵符號 in (32,0xff0d):
                try:
                    值=int(自身值.Unicode輸入,16)
                    if 32<=值<=0x10ffff and not 0xd800<=值<=0xdfff: 自身值.發送(chr(值).encode('utf-8'))
                except ValueError: pass
                自身值.Unicode輸入=None
            elif 鍵符號==0xff1b: 自身值.Unicode輸入=None
            elif 鍵符號==0xff08: 自身值.Unicode輸入=自身值.Unicode輸入[:-1]
            elif 鍵符號<128 and chr(鍵符號) in '0123456789abcdefABCDEF' and len(自身值.Unicode輸入)<6: 自身值.Unicode輸入+=chr(鍵符號)
            return
        if 鍵符號 in (0xff31,0xffc6) or 鍵符號==32 and 移位鍵 and not 控制鍵:
            if 鍵符號 not in 自身值.切換鍵: 自身值.切換模式()
            自身值.切換鍵.add(鍵符號)
            return
        if 鍵符號==0xff08 and 自身值.韓語 and not 控制鍵 and 自身值.韓文字母組合器.退格(): return
        if 控制鍵 and 移位鍵 and 鍵符號 in (ord('t'),ord('T')):
            自身值.發送(bytes([30,2,1,0,0,0,0])); return
        if 鍵符號==0xffc3: 自身值.發送(bytes([30,2,2,0,0,0,0])); return
        if 鍵符號==0xffc9: 自身值.發送(bytes([30,2,3,0,0,0,0])); return
        if 控制鍵 and 移位鍵 and 鍵符號 in (ord('v'), ord('V')):
            # Clipboard updates alone never execute text. An explicit paste key is required.
            自身值.發送(自身值.剪貼板值); return
        特殊鍵 = {0xff08:b'\x7f',0xff09:b'\t',0xff0d:b'\r',0xff1b:b'\x1b',0xffff:b'\x1b[3~',
                   0xff50:b'\x1b[H',0xff57:b'\x1b[F',0xff51:b'\x1b[D',0xff52:b'\x1b[A',
                   0xff53:b'\x1b[C',0xff54:b'\x1b[B',0xff55:b'\x1b[5~',0xff56:b'\x1b[6~',0xffc9:b'\x1b[24~'}
        if 鍵符號 in 特殊鍵: 自身值.發送(特殊鍵[鍵符號]); return
        字元編碼狀態 = 鍵符號 & 0xffffff if 鍵符號 & 0xff000000 == 0x01000000 else 鍵符號
        if 字元編碼狀態 > 0x10ffff or 0xd800 <= 字元編碼狀態 <= 0xdfff or 鍵符號 >= 0xff00 and 鍵符號 < 0x1000000: return
        if 控制鍵 and 0x40 <= 字元編碼狀態 <= 0x7f: 自身值.發送(bytes([字元編碼狀態 & 31])); return
        if 字元編碼狀態 < 32: return
        if 自身值.韓語 and 自身值.修飾符鍵 & {0xffea,0xfe03,0xff7e} and not 控制鍵 and hasattr(自身值.韓文字母組合器, 'profile'):
            if 自身值.韓文字母組合器.供給鍵(chr(字元編碼狀態), altgr=True): return
        前導部分 = b'\x1b' if 自身值.修飾符鍵 & {0xffe9, 0xffea} else b''
        if 自身值.韓語 and not 控制鍵 and not 前導部分 and 32<=字元編碼狀態<127:
            字元資料=chr(字元編碼狀態).upper() if 移位鍵 else chr(字元編碼狀態)
            if 自身值.韓文字母組合器.供給鍵(字元資料): return
        自身值.發送(前導部分 + chr(字元編碼狀態).encode('utf-8'))


class 連接桌面:
    def __init__(自身值, 程序):
        自身值.程序=程序; 自身值.鎖值=threading.Lock(); 自身值.準備狀態完成=False; 自身值.終端=False; 自身值.初始屏幕=False; 自身值.是否已關閉=False

    def 發送(自身值, 資料):
        if not 資料 or 自身值.是否已關閉: return
        with 自身值.鎖值:
            try: 自身值.程序.stdin.write(資料); 自身值.程序.stdin.flush()
            except (BrokenPipeError, ValueError): pass

    def 串行輸入輸出(自身值):
        結尾部分=b''
        try:
            while True:
                資料=自身值.程序.stdout.read(4096)
                if not 資料: break
                sys.stdout.buffer.write(資料); sys.stdout.buffer.flush()
                結尾部分=(結尾部分+資料)[-8192:]
                已打開=結尾部分.rfind(b'TERMINAL READY'); 是否已關閉=結尾部分.rfind(b'TERMINAL CLOSED'); 繪圖屏幕=結尾部分.rfind(b'GUI READY:'); 擁有已退出=結尾部分.rfind(b'GUI EXIT')
                # Preserve the mode after its marker has left the rolling UART buffer.
                if max(已打開,是否已關閉,繪圖屏幕,擁有已退出)>=0:
                    自身值.終端=已打開>max(是否已關閉,繪圖屏幕,擁有已退出)
                    自身值.初始屏幕=繪圖屏幕>max(已打開,是否已關閉,擁有已退出)
                if not 自身值.準備狀態完成 and b'jkoros-native> ' in 結尾部分:
                    自身值.準備狀態完成=True; 自身值.發送(b'terminal\n')
        finally: 自身值.是否已關閉=True

    def 客戶端(自身值, 客戶端, 路徑):
        服務器值=socket.socket(socket.AF_UNIX); 服務器值.settimeout(10); 客戶端.settimeout(10)
        鍵盤條目=鍵盤(自身值.發送,lambda 韓語:自身值.發送(bytes([30,3,int(韓語),0,0,0,0])))
        上一個按鈕列=0
        try:
            服務器值.connect(str(路徑))
            # 初始狀態 협상은 순서대로 끝낸다. 之後值 輸出 가닥만 클라이언트에 쓴다.
            客戶端.sendall(精確值(服務器值,12))
            版本編號=精確值(客戶端,12)
            if 版本編號 not in (b'RFB 003.008\n',b'RFB 003.007\n'): raise ValueError('RFB 3.7/3.8 required')
            服務器值.sendall(版本編號)
            項目個數=精確值(服務器值,1);客戶端.sendall(項目個數+精確值(服務器值,項目個數[0]))
            安全性=精確值(客戶端,1)
            if 安全性!=b'\x01': raise ValueError('unexpected security type')
            服務器值.sendall(安全性)
            if 版本編號==b'RFB 003.008\n':客戶端.sendall(精確值(服務器值,4))
            服務器值.sendall(精確值(客戶端,1))
            初始值=精確值(服務器值,24)
            客戶端.sendall(初始值+精確值(服務器值,struct.unpack('>I',初始值[20:])[0]))
            像素位元組列=初始值[4]//8;指針支持=False
            客戶端.settimeout(None);服務器值.settimeout(None)
            def 輸出結果():
                try:
                    while True:
                        分類值=精確值(服務器值,1)[0]
                        if 分類值==0:
                            頭值=精確值(服務器值,3);條目個數=struct.unpack('>H',頭值[1:])[0]
                            # RFC 6143 §7.8.1: 커널이 그린 포인터와 遠程值 포인터의 중복을 피한다.
                            隱藏值=指針支持
                            if 隱藏值:客戶端.sendall(struct.pack('>BBHHHHHi',0,0,1,0,0,0,0,-239))
                            客戶端.sendall(bytes([分類值])+頭值)
                            for _ in range(條目個數):
                                矩形=精確值(服務器值,12);水平位置,垂直位置,寬度跨度,高度值,編碼狀態值=struct.unpack('>HHHHi',矩形)
                                if 編碼狀態值!=0:raise ValueError('unexpected framebuffer encoding: '+str(編碼狀態值))
                                客戶端.sendall(矩形)
                                餘數資料=寬度跨度*高度值*像素位元組列
                                while 餘數資料:
                                    資料=精確值(服務器值,min(餘數資料,65536));客戶端.sendall(資料);餘數資料-=len(資料)
                        elif 分類值==1:
                            頭值=精確值(服務器值,5);項目個數=struct.unpack('>H',頭值[3:])[0]
                            客戶端.sendall(bytes([分類值])+頭值+精確值(服務器值,項目個數*6))
                        elif 分類值==2:客戶端.sendall(bytes([分類值]))
                        elif 分類值==3:
                            頭值=精確值(服務器值,7);項目個數=struct.unpack('>I',頭值[3:])[0]
                            if 項目個數>1048576:raise ValueError('server clipboard too large')
                            客戶端.sendall(bytes([分類值])+頭值+精確值(服務器值,項目個數))
                        else:raise ValueError('unexpected RFB server message: '+str(分類值))
                except (OSError,EOFError,ValueError):pass
                finally:
                    try:客戶端.shutdown(socket.SHUT_RDWR)
                    except OSError:pass
            後臺任務=threading.Thread(target=輸出結果,daemon=True);後臺任務.start()
            while not 自身值.是否已關閉:
                分類值=精確值(客戶端,1)[0]
                if 分類值==4:
                    主體文本=精確值(客戶端,7); 鍵盤條目.已按下值(主體文本[0]!=0,struct.unpack('>I',主體文本[3:])[0]); continue
                if 分類值==255:
                    主體文本=精確值(客戶端,11)
                    if 主體文本[0]!=0: raise ValueError('unsupported QEMU input extension')
                    鍵盤條目.已按下值(struct.unpack('>H',主體文本[1:3])[0]!=0,struct.unpack('>I',主體文本[3:7])[0]); continue
                if 分類值==5:
                    主體文本=精確值(客戶端,5); 按鈕列,橫座標座標,Y_按鈕座標=struct.unpack('>BHH',主體文本)
                    是否已按下=按鈕列&~上一個按鈕列; 上一個按鈕列=按鈕列
                    if 是否已按下: 鍵盤條目.韓文字母組合器.提交合成狀態()
                    if 是否已按下&1 and 自身值.初始屏幕 and 64<=橫座標座標<576 and 112<=Y_按鈕座標<372:
                        查找索引=(Y_按鈕座標-112)//52
                        if (Y_按鈕座標-112)%52<40 and 查找索引<5: 自身值.發送(bytes([ord('1')+查找索引]))
                    else: 自身值.發送(bytes([30,1,按鈕列,橫座標座標&255,橫座標座標>>8,Y_按鈕座標&255,Y_按鈕座標>>8]))
                    continue
                if 分類值==6:
                    主體文本=精確值(客戶端,7); 長度=struct.unpack('>i',主體文本[3:])[0]
                    if abs(長度)>65536: raise ValueError('clipboard too large')
                    文本=精確值(客戶端,abs(長度))
                    if 長度>=0:
                        try: 鍵盤條目.剪貼板值=文本.decode('utf-8').encode('utf-8')
                        except UnicodeDecodeError: 鍵盤條目.剪貼板值=文本.decode('latin-1').encode('utf-8')
                        鍵盤條目.剪貼板值=鍵盤條目.剪貼板值[:65536].decode('utf-8','ignore').encode('utf-8')
                    服務器值.sendall(bytes([分類值])+主體文本+文本); continue
                if 分類值==0:
                    主體文本=精確值(客戶端,19)
                    if 主體文本[3] not in (8,16,32):raise ValueError('unsupported pixel size')
                    像素位元組列=主體文本[3]//8
                elif 分類值==2:
                    主體文本=精確值(客戶端,3); 條目個數=struct.unpack('>H',主體文本[1:])[0]
                    if 條目個數>512: raise ValueError('too many encodings')
                    已編碼值列=struct.unpack('>'+str(條目個數)+'i',精確值(客戶端,條目個數*4))
                    指針支持=-239 in 已編碼值列
                    # 로컬 屏幕 중계는 默認值 Raw만 요청하여 프레임 경계에서 포인터를 숨긴다.
                    主體文本=struct.pack('>BHi',0,1,0)
                elif 分類值 in (3,150): 主體文本=精確值(客戶端,9)
                elif 分類值==248:
                    主體文本=精確值(客戶端,8)
                    if 主體文本[7]>64: raise ValueError('fence too large')
                    主體文本+=精確值(客戶端,主體文本[7])
                elif 分類值==250: 主體文本=精確值(客戶端,3)
                elif 分類值==251:
                    主體文本=精確值(客戶端,7)
                    if 主體文本[5]>16: raise ValueError('too many screens')
                    主體文本+=精確值(客戶端,主體文本[5]*16)
                else: raise ValueError('unsupported RFB message {}'.format(分類值))
                服務器值.sendall(bytes([分類值])+主體文本)
        except (OSError,EOFError,ValueError) as 錯誤:
            if str(錯誤): print('VNC client:',錯誤,file=sys.stderr,flush=True)
        finally:
            for 通訊端值 in (客戶端,服務器值):
                try: 通訊端值.shutdown(socket.SHUT_RDWR)
                except OSError: pass
                通訊端值.close()


def 運行桌面(埠編號=5902, 使用網路=False, 檔案傳送埠編號=2121, 轉發中規則列=(), 分辨率值=(640, 480), 客戶機地址=None, 宿主地址='127.0.0.1'):
    with ExitStack() as 資源集, tempfile.TemporaryDirectory(prefix='jkoros-desktop-') as 工作中路徑:
        網路橋接條目 = None
        if 使用網路:
            from 網路橋接 import 網路橋接
            網路橋接條目 = 資源集.enter_context(網路橋接(檔案傳送埠編號, 轉發中規則列, 客戶機地址=客戶機地址, 宿主地址=宿主地址))
        路徑=Path(工作中路徑)/'display.sock'
        with socket.socket() as 接收埠:
            接收埠.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            接收埠.bind(('127.0.0.1',埠編號)); 接收埠.listen(1); 接收埠.settimeout(.2)
            VNC埠=接收埠.getsockname()[1]
            if 網路橋接條目 and (VNC埠==檔案傳送埠編號 or 50000<=VNC埠<=50007 or any(網路ABI=='tcp' and 宿主==VNC埠 for 網路ABI,宿主,_ in 網路橋接條目.轉發中規則列)):
                raise ValueError('VNC port conflicts with an FTP/TCP forwarding port')
            程序=subprocess.Popen(命令(分辨率值)+['-display','none','-monitor','none','-serial','stdio','-vnc','unix:'+str(路徑)]+(網路橋接條目.已轉發實際參數() if 網路橋接條目 else []),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            橋接=連接桌面(程序); 讀取器=threading.Thread(target=橋接.串行輸入輸出,daemon=True); 讀取器.start()
            print('DESKTOP VNC 127.0.0.1:{} — Remmina VNC; keyboard/Unicode/paste bridge; Ctrl+C stops VM'.format(接收埠.getsockname()[1]),flush=True)
            if 網路橋接條目: print('NETWORK FTP {}:{} — guest command: ftpd start'.format(宿主地址,檔案傳送埠編號),flush=True)
            def 終止(信號編號,執行狀態幀): raise KeyboardInterrupt()
            上一個=signal.signal(signal.SIGTERM,終止)
            處理任務=None; 已中斷=False
            try:
                while 程序.poll() is None:
                    try: 客戶端,_=接收埠.accept()
                    except socket.timeout: continue
                    if 處理任務 is not None and 處理任務.is_alive(): 客戶端.close(); continue
                    if not 路徑.exists(): 客戶端.close(); continue
                    處理任務=threading.Thread(target=橋接.客戶端,args=(客戶端,路徑),daemon=True); 處理任務.start()
            except KeyboardInterrupt: 已中斷=True
            finally:
                橋接.是否已關閉=True
                if 網路橋接條目: 網路橋接條目.暫停事件.set()
                if 程序.poll() is None:
                    程序.terminate()
                    try: 程序.wait(timeout=5)
                    except subprocess.TimeoutExpired: 程序.kill(); 程序.wait()
                讀取器.join(timeout=2); 程序.stdin.close(); 程序.stdout.close(); signal.signal(signal.SIGTERM,上一個)
            if 網路橋接條目 and 網路橋接條目.錯誤: raise RuntimeError('network bridge: '+網路橋接條目.錯誤)
            return 0 if 已中斷 else 程序.returncode


if __name__=='__main__':
    from 執行命令 import 讀取分辨率
    參數解析器=argparse.ArgumentParser(description=__doc__); 參數解析器.add_argument('--port',type=int,default=5902)
    參數解析器.add_argument('--resolution',type=讀取分辨率,default=(640,480))
    參數解析器.add_argument('--network',action='store_true'); 參數解析器.add_argument('--ftp-port',type=int,default=2121)
    參數解析器.add_argument('--forward',action='append',default=[])
    實際參數陣列=參數解析器.parse_args()
    if 實際參數陣列.forward and not 實際參數陣列.network: 參數解析器.error('--forward requires --network')
    raise SystemExit(運行桌面(實際參數陣列.port,使用網路=實際參數陣列.network,檔案傳送埠編號=實際參數陣列.ftp_port,轉發中規則列=實際參數陣列.forward,分辨率值=實際參數陣列.resolution))

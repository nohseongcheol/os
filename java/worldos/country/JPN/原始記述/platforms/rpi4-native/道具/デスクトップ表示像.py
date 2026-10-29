#!/usr/bin/env python3
"""RFB 화면은 QEMU에서, キー値 입력은 内蔵 中核値 UART로 전달한다. localhost 전용, 단일 制御値 클라이언트.
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
from 命令実行 import 命令
from local_input import create


def 厳密値(ソケット値, 容量):
    データ = bytearray()
    while len(データ) < 容量:
        断片値 = ソケット値.recv(容量 - len(データ))
        if not 断片値: raise EOFError()
        データ.extend(断片値)
    return bytes(データ)


class キーボード:
    def __init__(自身値, 送信, 方式変更済み=None):
        自身値.転送バイト列 = 送信; 自身値.修飾子キー = set(); 自身値.貼付け板値 = b''
        自身値.ハングル組立器 = create(送信, Path(__file__).resolve().parents[1]); 自身値.韓国語 = False; 自身値.切替キー = set()
        自身値.Unicode入力 = None
        自身値.方式変更済み = 方式変更済み
        if 方式変更済み: 方式変更済み(False)

    def 送信(自身値, データ):
        自身値.ハングル組立器.確定合成状態()
        自身値.転送バイト列(データ)

    def 切替方式(自身値):
        自身値.ハングル組立器.確定合成状態(); 自身値.韓国語 = not 自身値.韓国語
        if 自身値.方式変更済み: 自身値.方式変更済み(自身値.韓国語)

    def 押下済み値(自身値, 判定押下中, キー記号):
        if キー記号 in (0xffe1, 0xffe2, 0xffe3, 0xffe4, 0xffe9, 0xffea, 0xfe03, 0xff7e):
            if 判定押下中: 自身値.修飾子キー.add(キー記号)
            else: 自身値.修飾子キー.discard(キー記号)
            return
        if not 判定押下中:
            自身値.切替キー.discard(キー記号)
            return
        制御キー = bool(自身値.修飾子キー & {0xffe3, 0xffe4})
        シフトキー = bool(自身値.修飾子キー & {0xffe1, 0xffe2})
        if 制御キー and シフトキー and キー記号 in (ord('u'),ord('U')):
            自身値.ハングル組立器.確定合成状態(); 自身値.Unicode入力 = ''; return
        if 自身値.Unicode入力 is not None:
            if キー記号 in (32,0xff0d):
                try:
                    値=int(自身値.Unicode入力,16)
                    if 32<=値<=0x10ffff and not 0xd800<=値<=0xdfff: 自身値.送信(chr(値).encode('utf-8'))
                except ValueError: pass
                自身値.Unicode入力=None
            elif キー記号==0xff1b: 自身値.Unicode入力=None
            elif キー記号==0xff08: 自身値.Unicode入力=自身値.Unicode入力[:-1]
            elif キー記号<128 and chr(キー記号) in '0123456789abcdefABCDEF' and len(自身値.Unicode入力)<6: 自身値.Unicode入力+=chr(キー記号)
            return
        if キー記号 in (0xff31,0xffc6) or キー記号==32 and シフトキー and not 制御キー:
            if キー記号 not in 自身値.切替キー: 自身値.切替方式()
            自身値.切替キー.add(キー記号)
            return
        if キー記号==0xff08 and 自身値.韓国語 and not 制御キー and 自身値.ハングル組立器.後退消去(): return
        if 制御キー and シフトキー and キー記号 in (ord('t'),ord('T')):
            自身値.送信(bytes([30,2,1,0,0,0,0])); return
        if キー記号==0xffc3: 自身値.送信(bytes([30,2,2,0,0,0,0])); return
        if キー記号==0xffc9: 自身値.送信(bytes([30,2,3,0,0,0,0])); return
        if 制御キー and シフトキー and キー記号 in (ord('v'), ord('V')):
            # Clipboard updates alone never execute text. An explicit paste key is required.
            自身値.送信(自身値.貼付け板値); return
        特殊キー = {0xff08:b'\x7f',0xff09:b'\t',0xff0d:b'\r',0xff1b:b'\x1b',0xffff:b'\x1b[3~',
                   0xff50:b'\x1b[H',0xff57:b'\x1b[F',0xff51:b'\x1b[D',0xff52:b'\x1b[A',
                   0xff53:b'\x1b[C',0xff54:b'\x1b[B',0xff55:b'\x1b[5~',0xff56:b'\x1b[6~',0xffc9:b'\x1b[24~'}
        if キー記号 in 特殊キー: 自身値.送信(特殊キー[キー記号]); return
        文字符号化状態 = キー記号 & 0xffffff if キー記号 & 0xff000000 == 0x01000000 else キー記号
        if 文字符号化状態 > 0x10ffff or 0xd800 <= 文字符号化状態 <= 0xdfff or キー記号 >= 0xff00 and キー記号 < 0x1000000: return
        if 制御キー and 0x40 <= 文字符号化状態 <= 0x7f: 自身値.送信(bytes([文字符号化状態 & 31])); return
        if 文字符号化状態 < 32: return
        if 自身値.韓国語 and 自身値.修飾子キー & {0xffea,0xfe03,0xff7e} and not 制御キー and hasattr(自身値.ハングル組立器, 'profile'):
            if 自身値.ハングル組立器.供給キー(chr(文字符号化状態), altgr=True): return
        先行部分 = b'\x1b' if 自身値.修飾子キー & {0xffe9, 0xffea} else b''
        if 自身値.韓国語 and not 制御キー and not 先行部分 and 32<=文字符号化状態<127:
            文字データ=chr(文字符号化状態).upper() if シフトキー else chr(文字符号化状態)
            if 自身値.ハングル組立器.供給キー(文字データ): return
        自身値.送信(先行部分 + chr(文字符号化状態).encode('utf-8'))


class デスクトップ接続:
    def __init__(自身値, プロセス):
        自身値.プロセス=プロセス; 自身値.錠値=threading.Lock(); 自身値.用意状態完了=False; 自身値.端末=False; 自身値.初期画面=False; 自身値.判定閉鎖済み=False

    def 送信(自身値, データ):
        if not データ or 自身値.判定閉鎖済み: return
        with 自身値.錠値:
            try: 自身値.プロセス.stdin.write(データ); 自身値.プロセス.stdin.flush()
            except (BrokenPipeError, ValueError): pass

    def 直列入出力(自身値):
        終端部分=b''
        try:
            while True:
                データ=自身値.プロセス.stdout.read(4096)
                if not データ: break
                sys.stdout.buffer.write(データ); sys.stdout.buffer.flush()
                終端部分=(終端部分+データ)[-8192:]
                開放済み=終端部分.rfind(b'TERMINAL READY'); 判定閉鎖済み=終端部分.rfind(b'TERMINAL CLOSED'); 描画中画面=終端部分.rfind(b'GUI READY:'); 保有終了済み=終端部分.rfind(b'GUI EXIT')
                # Preserve the mode after its marker has left the rolling UART buffer.
                if max(開放済み,判定閉鎖済み,描画中画面,保有終了済み)>=0:
                    自身値.端末=開放済み>max(判定閉鎖済み,描画中画面,保有終了済み)
                    自身値.初期画面=描画中画面>max(開放済み,判定閉鎖済み,保有終了済み)
                if not 自身値.用意状態完了 and b'jkoros-native> ' in 終端部分:
                    自身値.用意状態完了=True; 自身値.送信(b'terminal\n')
        finally: 自身値.判定閉鎖済み=True

    def 接続元(自身値, 接続元, 経路):
        サーバー値=socket.socket(socket.AF_UNIX); サーバー値.settimeout(10); 接続元.settimeout(10)
        キーボード入口=キーボード(自身値.送信,lambda 韓国語:自身値.送信(bytes([30,3,int(韓国語),0,0,0,0])))
        前回ボタン一覧=0
        try:
            サーバー値.connect(str(経路))
            # 初期状況 협상은 순서대로 끝낸다. 後続側値 出力 가닥만 클라이언트에 쓴다.
            接続元.sendall(厳密値(サーバー値,12))
            版番号=厳密値(接続元,12)
            if 版番号 not in (b'RFB 003.008\n',b'RFB 003.007\n'): raise ValueError('RFB 3.7/3.8 required')
            サーバー値.sendall(版番号)
            項目個数=厳密値(サーバー値,1);接続元.sendall(項目個数+厳密値(サーバー値,項目個数[0]))
            安全性=厳密値(接続元,1)
            if 安全性!=b'\x01': raise ValueError('unexpected security type')
            サーバー値.sendall(安全性)
            if 版番号==b'RFB 003.008\n':接続元.sendall(厳密値(サーバー値,4))
            サーバー値.sendall(厳密値(接続元,1))
            初期値=厳密値(サーバー値,24)
            接続元.sendall(初期値+厳密値(サーバー値,struct.unpack('>I',初期値[20:])[0]))
            画素バイト列=初期値[4]//8;ポインタ対応済み=False
            接続元.settimeout(None);サーバー値.settimeout(None)
            def 出力結果():
                try:
                    while True:
                        分類値=厳密値(サーバー値,1)[0]
                        if 分類値==0:
                            先頭部値=厳密値(サーバー値,3);入口個数=struct.unpack('>H',先頭部値[1:])[0]
                            # RFC 6143 §7.8.1: 커널이 그린 포인터와 遠隔値 포인터의 중복을 피한다.
                            隠蔽値=ポインタ対応済み
                            if 隠蔽値:接続元.sendall(struct.pack('>BBHHHHHi',0,0,1,0,0,0,0,-239))
                            接続元.sendall(bytes([分類値])+先頭部値)
                            for _ in range(入口個数):
                                矩形=厳密値(サーバー値,12);水平位置,垂直位置,幅跨域,高さ値,符号化状態値=struct.unpack('>HHHHi',矩形)
                                if 符号化状態値!=0:raise ValueError('unexpected framebuffer encoding: '+str(符号化状態値))
                                接続元.sendall(矩形)
                                剰余データ=幅跨域*高さ値*画素バイト列
                                while 剰余データ:
                                    データ=厳密値(サーバー値,min(剰余データ,65536));接続元.sendall(データ);剰余データ-=len(データ)
                        elif 分類値==1:
                            先頭部値=厳密値(サーバー値,5);項目個数=struct.unpack('>H',先頭部値[3:])[0]
                            接続元.sendall(bytes([分類値])+先頭部値+厳密値(サーバー値,項目個数*6))
                        elif 分類値==2:接続元.sendall(bytes([分類値]))
                        elif 分類値==3:
                            先頭部値=厳密値(サーバー値,7);項目個数=struct.unpack('>I',先頭部値[3:])[0]
                            if 項目個数>1048576:raise ValueError('server clipboard too large')
                            接続元.sendall(bytes([分類値])+先頭部値+厳密値(サーバー値,項目個数))
                        else:raise ValueError('unexpected RFB server message: '+str(分類値))
                except (OSError,EOFError,ValueError):pass
                finally:
                    try:接続元.shutdown(socket.SHUT_RDWR)
                    except OSError:pass
            作業担当=threading.Thread(target=出力結果,daemon=True);作業担当.start()
            while not 自身値.判定閉鎖済み:
                分類値=厳密値(接続元,1)[0]
                if 分類値==4:
                    本体本文=厳密値(接続元,7); キーボード入口.押下済み値(本体本文[0]!=0,struct.unpack('>I',本体本文[3:])[0]); continue
                if 分類値==255:
                    本体本文=厳密値(接続元,11)
                    if 本体本文[0]!=0: raise ValueError('unsupported QEMU input extension')
                    キーボード入口.押下済み値(struct.unpack('>H',本体本文[1:3])[0]!=0,struct.unpack('>I',本体本文[3:7])[0]); continue
                if 分類値==5:
                    本体本文=厳密値(接続元,5); ボタン一覧,横座標,縦座標=struct.unpack('>BHH',本体本文)
                    判定押下済み=ボタン一覧&~前回ボタン一覧; 前回ボタン一覧=ボタン一覧
                    if 判定押下済み: キーボード入口.ハングル組立器.確定合成状態()
                    if 判定押下済み&1 and 自身値.初期画面 and 64<=横座標<576 and 112<=縦座標<372:
                        検索添字=(縦座標-112)//52
                        if (縦座標-112)%52<40 and 検索添字<5: 自身値.送信(bytes([ord('1')+検索添字]))
                    else: 自身値.送信(bytes([30,1,ボタン一覧,横座標&255,横座標>>8,縦座標&255,縦座標>>8]))
                    continue
                if 分類値==6:
                    本体本文=厳密値(接続元,7); 長さ=struct.unpack('>i',本体本文[3:])[0]
                    if abs(長さ)>65536: raise ValueError('clipboard too large')
                    文=厳密値(接続元,abs(長さ))
                    if 長さ>=0:
                        try: キーボード入口.貼付け板値=文.decode('utf-8').encode('utf-8')
                        except UnicodeDecodeError: キーボード入口.貼付け板値=文.decode('latin-1').encode('utf-8')
                        キーボード入口.貼付け板値=キーボード入口.貼付け板値[:65536].decode('utf-8','ignore').encode('utf-8')
                    サーバー値.sendall(bytes([分類値])+本体本文+文); continue
                if 分類値==0:
                    本体本文=厳密値(接続元,19)
                    if 本体本文[3] not in (8,16,32):raise ValueError('unsupported pixel size')
                    画素バイト列=本体本文[3]//8
                elif 分類値==2:
                    本体本文=厳密値(接続元,3); 入口個数=struct.unpack('>H',本体本文[1:])[0]
                    if 入口個数>512: raise ValueError('too many encodings')
                    符号化済み値一覧=struct.unpack('>'+str(入口個数)+'i',厳密値(接続元,入口個数*4))
                    ポインタ対応済み=-239 in 符号化済み値一覧
                    # 로컬 画面 중계는 既定値 Raw만 요청하여 프레임 경계에서 포인터를 숨긴다.
                    本体本文=struct.pack('>BHi',0,1,0)
                elif 分類値 in (3,150): 本体本文=厳密値(接続元,9)
                elif 分類値==248:
                    本体本文=厳密値(接続元,8)
                    if 本体本文[7]>64: raise ValueError('fence too large')
                    本体本文+=厳密値(接続元,本体本文[7])
                elif 分類値==250: 本体本文=厳密値(接続元,3)
                elif 分類値==251:
                    本体本文=厳密値(接続元,7)
                    if 本体本文[5]>16: raise ValueError('too many screens')
                    本体本文+=厳密値(接続元,本体本文[5]*16)
                else: raise ValueError('unsupported RFB message {}'.format(分類値))
                サーバー値.sendall(bytes([分類値])+本体本文)
        except (OSError,EOFError,ValueError) as エラー:
            if str(エラー): print('VNC client:',エラー,file=sys.stderr,flush=True)
        finally:
            for ソケット値 in (接続元,サーバー値):
                try: ソケット値.shutdown(socket.SHUT_RDWR)
                except OSError: pass
                ソケット値.close()


def デスクトップ起動処理(ポート番号=5902, 通信使用=False, ファイル転送ポート番号=2121, 転送中規則一覧=(), 解像度値=(640, 480), ゲスト番地=None, ホスト番地='127.0.0.1'):
    with ExitStack() as 資源一覧, tempfile.TemporaryDirectory(prefix='jkoros-desktop-') as 作業中経路:
        通信網橋渡し入口 = None
        if 通信使用:
            from 通信網橋渡し import 通信網橋渡し
            通信網橋渡し入口 = 資源一覧.enter_context(通信網橋渡し(ファイル転送ポート番号, 転送中規則一覧, ゲスト番地=ゲスト番地, ホスト番地=ホスト番地))
        経路=Path(作業中経路)/'display.sock'
        with socket.socket() as ポート受取:
            ポート受取.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            ポート受取.bind(('127.0.0.1',ポート番号)); ポート受取.listen(1); ポート受取.settimeout(.2)
            VNCポート=ポート受取.getsockname()[1]
            if 通信網橋渡し入口 and (VNCポート==ファイル転送ポート番号 or 50000<=VNCポート<=50007 or any(通信網ABI=='tcp' and ホスト==VNCポート for 通信網ABI,ホスト,_ in 通信網橋渡し入口.転送中規則一覧)):
                raise ValueError('VNC port conflicts with an FTP/TCP forwarding port')
            プロセス=subprocess.Popen(命令(解像度値)+['-display','none','-monitor','none','-serial','stdio','-vnc','unix:'+str(経路)]+(通信網橋渡し入口.転送済み引数() if 通信網橋渡し入口 else []),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            橋渡し=デスクトップ接続(プロセス); 読取器=threading.Thread(target=橋渡し.直列入出力,daemon=True); 読取器.start()
            print('DESKTOP VNC 127.0.0.1:{} — Remmina VNC; keyboard/Unicode/paste bridge; Ctrl+C stops VM'.format(ポート受取.getsockname()[1]),flush=True)
            if 通信網橋渡し入口: print('NETWORK FTP {}:{} — guest command: ftpd start'.format(ホスト番地,ファイル転送ポート番号),flush=True)
            def 終了(信号番号,実行状態枠組): raise KeyboardInterrupt()
            前回=signal.signal(signal.SIGTERM,終了)
            処理工程作業=None; 中断済み=False
            try:
                while プロセス.poll() is None:
                    try: 接続元,_=ポート受取.accept()
                    except socket.timeout: continue
                    if 処理工程作業 is not None and 処理工程作業.is_alive(): 接続元.close(); continue
                    if not 経路.exists(): 接続元.close(); continue
                    処理工程作業=threading.Thread(target=橋渡し.接続元,args=(接続元,経路),daemon=True); 処理工程作業.start()
            except KeyboardInterrupt: 中断済み=True
            finally:
                橋渡し.判定閉鎖済み=True
                if 通信網橋渡し入口: 通信網橋渡し入口.一時停止イベント.set()
                if プロセス.poll() is None:
                    プロセス.terminate()
                    try: プロセス.wait(timeout=5)
                    except subprocess.TimeoutExpired: プロセス.kill(); プロセス.wait()
                読取器.join(timeout=2); プロセス.stdin.close(); プロセス.stdout.close(); signal.signal(signal.SIGTERM,前回)
            if 通信網橋渡し入口 and 通信網橋渡し入口.エラー: raise RuntimeError('network bridge: '+通信網橋渡し入口.エラー)
            return 0 if 中断済み else プロセス.returncode


if __name__=='__main__':
    from 命令実行 import 解像度読取
    引数解析器=argparse.ArgumentParser(description=__doc__); 引数解析器.add_argument('--port',type=int,default=5902)
    引数解析器.add_argument('--resolution',type=解像度読取,default=(640,480))
    引数解析器.add_argument('--network',action='store_true'); 引数解析器.add_argument('--ftp-port',type=int,default=2121)
    引数解析器.add_argument('--forward',action='append',default=[])
    引数配列=引数解析器.parse_args()
    if 引数配列.forward and not 引数配列.network: 引数解析器.error('--forward requires --network')
    raise SystemExit(デスクトップ起動処理(引数配列.port,通信使用=引数配列.network,ファイル転送ポート番号=引数配列.ftp_port,転送中規則一覧=引数配列.forward,解像度値=引数配列.resolution))

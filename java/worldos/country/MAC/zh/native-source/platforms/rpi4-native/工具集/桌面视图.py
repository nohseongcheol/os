#!/usr/bin/env python3
"""RFB 화면은 QEMU에서, 键值 입력은 内置 内核值 UART로 전달한다. localhost 전용, 단일 控制值 클라이언트.
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
from 执行命令 import 命令
from local_input import create


def 精确值(套接字值, 大小):
    数据 = bytearray()
    while len(数据) < 大小:
        片段值 = 套接字值.recv(大小 - len(数据))
        if not 片段值: raise EOFError()
        数据.extend(片段值)
    return bytes(数据)


class 键盘:
    def __init__(自身值, 发送, 模式已更改=None):
        自身值.传送字节列 = 发送; 自身值.修饰符键 = set(); 自身值.剪贴板值 = b''
        自身值.韩文字母组合器 = create(发送, Path(__file__).resolve().parents[1]); 自身值.韩语 = False; 自身值.切换键 = set()
        自身值.Unicode输入 = None
        自身值.模式已更改 = 模式已更改
        if 模式已更改: 模式已更改(False)

    def 发送(自身值, 数据):
        自身值.韩文字母组合器.提交合成状态()
        自身值.传送字节列(数据)

    def 切换模式(自身值):
        自身值.韩文字母组合器.提交合成状态(); 自身值.韩语 = not 自身值.韩语
        if 自身值.模式已更改: 自身值.模式已更改(自身值.韩语)

    def 已按下值(自身值, 是否按下中, 键符号):
        if 键符号 in (0xffe1, 0xffe2, 0xffe3, 0xffe4, 0xffe9, 0xffea, 0xfe03, 0xff7e):
            if 是否按下中: 自身值.修饰符键.add(键符号)
            else: 自身值.修饰符键.discard(键符号)
            return
        if not 是否按下中:
            自身值.切换键.discard(键符号)
            return
        控制键 = bool(自身值.修饰符键 & {0xffe3, 0xffe4})
        移位键 = bool(自身值.修饰符键 & {0xffe1, 0xffe2})
        if 控制键 and 移位键 and 键符号 in (ord('u'),ord('U')):
            自身值.韩文字母组合器.提交合成状态(); 自身值.Unicode输入 = ''; return
        if 自身值.Unicode输入 is not None:
            if 键符号 in (32,0xff0d):
                try:
                    值=int(自身值.Unicode输入,16)
                    if 32<=值<=0x10ffff and not 0xd800<=值<=0xdfff: 自身值.发送(chr(值).encode('utf-8'))
                except ValueError: pass
                自身值.Unicode输入=None
            elif 键符号==0xff1b: 自身值.Unicode输入=None
            elif 键符号==0xff08: 自身值.Unicode输入=自身值.Unicode输入[:-1]
            elif 键符号<128 and chr(键符号) in '0123456789abcdefABCDEF' and len(自身值.Unicode输入)<6: 自身值.Unicode输入+=chr(键符号)
            return
        if 键符号 in (0xff31,0xffc6) or 键符号==32 and 移位键 and not 控制键:
            if 键符号 not in 自身值.切换键: 自身值.切换模式()
            自身值.切换键.add(键符号)
            return
        if 键符号==0xff08 and 自身值.韩语 and not 控制键 and 自身值.韩文字母组合器.退格(): return
        if 控制键 and 移位键 and 键符号 in (ord('t'),ord('T')):
            自身值.发送(bytes([30,2,1,0,0,0,0])); return
        if 键符号==0xffc3: 自身值.发送(bytes([30,2,2,0,0,0,0])); return
        if 键符号==0xffc9: 自身值.发送(bytes([30,2,3,0,0,0,0])); return
        if 控制键 and 移位键 and 键符号 in (ord('v'), ord('V')):
            # Clipboard updates alone never execute text. An explicit paste key is required.
            自身值.发送(自身值.剪贴板值); return
        特殊键 = {0xff08:b'\x7f',0xff09:b'\t',0xff0d:b'\r',0xff1b:b'\x1b',0xffff:b'\x1b[3~',
                   0xff50:b'\x1b[H',0xff57:b'\x1b[F',0xff51:b'\x1b[D',0xff52:b'\x1b[A',
                   0xff53:b'\x1b[C',0xff54:b'\x1b[B',0xff55:b'\x1b[5~',0xff56:b'\x1b[6~',0xffc9:b'\x1b[24~'}
        if 键符号 in 特殊键: 自身值.发送(特殊键[键符号]); return
        字符编码状态 = 键符号 & 0xffffff if 键符号 & 0xff000000 == 0x01000000 else 键符号
        if 字符编码状态 > 0x10ffff or 0xd800 <= 字符编码状态 <= 0xdfff or 键符号 >= 0xff00 and 键符号 < 0x1000000: return
        if 控制键 and 0x40 <= 字符编码状态 <= 0x7f: 自身值.发送(bytes([字符编码状态 & 31])); return
        if 字符编码状态 < 32: return
        if 自身值.韩语 and 自身值.修饰符键 & {0xffea,0xfe03,0xff7e} and not 控制键 and hasattr(自身值.韩文字母组合器, 'profile'):
            if 自身值.韩文字母组合器.供给键(chr(字符编码状态), altgr=True): return
        前导部分 = b'\x1b' if 自身值.修饰符键 & {0xffe9, 0xffea} else b''
        if 自身值.韩语 and not 控制键 and not 前导部分 and 32<=字符编码状态<127:
            字符数据=chr(字符编码状态).upper() if 移位键 else chr(字符编码状态)
            if 自身值.韩文字母组合器.供给键(字符数据): return
        自身值.发送(前导部分 + chr(字符编码状态).encode('utf-8'))


class 连接桌面:
    def __init__(自身值, 进程):
        自身值.进程=进程; 自身值.锁值=threading.Lock(); 自身值.准备状态完成=False; 自身值.终端=False; 自身值.初始屏幕=False; 自身值.是否已关闭=False

    def 发送(自身值, 数据):
        if not 数据 or 自身值.是否已关闭: return
        with 自身值.锁值:
            try: 自身值.进程.stdin.write(数据); 自身值.进程.stdin.flush()
            except (BrokenPipeError, ValueError): pass

    def 串行输入输出(自身值):
        结尾部分=b''
        try:
            while True:
                数据=自身值.进程.stdout.read(4096)
                if not 数据: break
                sys.stdout.buffer.write(数据); sys.stdout.buffer.flush()
                结尾部分=(结尾部分+数据)[-8192:]
                已打开=结尾部分.rfind(b'TERMINAL READY'); 是否已关闭=结尾部分.rfind(b'TERMINAL CLOSED'); 绘图屏幕=结尾部分.rfind(b'GUI READY:'); 拥有已退出=结尾部分.rfind(b'GUI EXIT')
                # Preserve the mode after its marker has left the rolling UART buffer.
                if max(已打开,是否已关闭,绘图屏幕,拥有已退出)>=0:
                    自身值.终端=已打开>max(是否已关闭,绘图屏幕,拥有已退出)
                    自身值.初始屏幕=绘图屏幕>max(已打开,是否已关闭,拥有已退出)
                if not 自身值.准备状态完成 and b'jkoros-native> ' in 结尾部分:
                    自身值.准备状态完成=True; 自身值.发送(b'terminal\n')
        finally: 自身值.是否已关闭=True

    def 客户端(自身值, 客户端, 路径):
        服务器值=socket.socket(socket.AF_UNIX); 服务器值.settimeout(10); 客户端.settimeout(10)
        键盘条目=键盘(自身值.发送,lambda 韩语:自身值.发送(bytes([30,3,int(韩语),0,0,0,0])))
        上一个按钮列=0
        try:
            服务器值.connect(str(路径))
            # 初始状态 협상은 순서대로 끝낸다. 之后值 输出 가닥만 클라이언트에 쓴다.
            客户端.sendall(精确值(服务器值,12))
            版本编号=精确值(客户端,12)
            if 版本编号 not in (b'RFB 003.008\n',b'RFB 003.007\n'): raise ValueError('RFB 3.7/3.8 required')
            服务器值.sendall(版本编号)
            项目个数=精确值(服务器值,1);客户端.sendall(项目个数+精确值(服务器值,项目个数[0]))
            安全性=精确值(客户端,1)
            if 安全性!=b'\x01': raise ValueError('unexpected security type')
            服务器值.sendall(安全性)
            if 版本编号==b'RFB 003.008\n':客户端.sendall(精确值(服务器值,4))
            服务器值.sendall(精确值(客户端,1))
            初始值=精确值(服务器值,24)
            客户端.sendall(初始值+精确值(服务器值,struct.unpack('>I',初始值[20:])[0]))
            像素字节列=初始值[4]//8;指针支持=False
            客户端.settimeout(None);服务器值.settimeout(None)
            def 输出结果():
                try:
                    while True:
                        分类值=精确值(服务器值,1)[0]
                        if 分类值==0:
                            头值=精确值(服务器值,3);条目个数=struct.unpack('>H',头值[1:])[0]
                            # RFC 6143 §7.8.1: 커널이 그린 포인터와 远程值 포인터의 중복을 피한다.
                            隐藏值=指针支持
                            if 隐藏值:客户端.sendall(struct.pack('>BBHHHHHi',0,0,1,0,0,0,0,-239))
                            客户端.sendall(bytes([分类值])+头值)
                            for _ in range(条目个数):
                                矩形=精确值(服务器值,12);水平位置,垂直位置,宽度跨度,高度值,编码状态值=struct.unpack('>HHHHi',矩形)
                                if 编码状态值!=0:raise ValueError('unexpected framebuffer encoding: '+str(编码状态值))
                                客户端.sendall(矩形)
                                余数数据=宽度跨度*高度值*像素字节列
                                while 余数数据:
                                    数据=精确值(服务器值,min(余数数据,65536));客户端.sendall(数据);余数数据-=len(数据)
                        elif 分类值==1:
                            头值=精确值(服务器值,5);项目个数=struct.unpack('>H',头值[3:])[0]
                            客户端.sendall(bytes([分类值])+头值+精确值(服务器值,项目个数*6))
                        elif 分类值==2:客户端.sendall(bytes([分类值]))
                        elif 分类值==3:
                            头值=精确值(服务器值,7);项目个数=struct.unpack('>I',头值[3:])[0]
                            if 项目个数>1048576:raise ValueError('server clipboard too large')
                            客户端.sendall(bytes([分类值])+头值+精确值(服务器值,项目个数))
                        else:raise ValueError('unexpected RFB server message: '+str(分类值))
                except (OSError,EOFError,ValueError):pass
                finally:
                    try:客户端.shutdown(socket.SHUT_RDWR)
                    except OSError:pass
            后台任务=threading.Thread(target=输出结果,daemon=True);后台任务.start()
            while not 自身值.是否已关闭:
                分类值=精确值(客户端,1)[0]
                if 分类值==4:
                    主体文本=精确值(客户端,7); 键盘条目.已按下值(主体文本[0]!=0,struct.unpack('>I',主体文本[3:])[0]); continue
                if 分类值==255:
                    主体文本=精确值(客户端,11)
                    if 主体文本[0]!=0: raise ValueError('unsupported QEMU input extension')
                    键盘条目.已按下值(struct.unpack('>H',主体文本[1:3])[0]!=0,struct.unpack('>I',主体文本[3:7])[0]); continue
                if 分类值==5:
                    主体文本=精确值(客户端,5); 按钮列,横坐标坐标,Y_按钮坐标=struct.unpack('>BHH',主体文本)
                    是否已按下=按钮列&~上一个按钮列; 上一个按钮列=按钮列
                    if 是否已按下: 键盘条目.韩文字母组合器.提交合成状态()
                    if 是否已按下&1 and 自身值.初始屏幕 and 64<=横坐标坐标<576 and 112<=Y_按钮坐标<372:
                        查找索引=(Y_按钮坐标-112)//52
                        if (Y_按钮坐标-112)%52<40 and 查找索引<5: 自身值.发送(bytes([ord('1')+查找索引]))
                    else: 自身值.发送(bytes([30,1,按钮列,横坐标坐标&255,横坐标坐标>>8,Y_按钮坐标&255,Y_按钮坐标>>8]))
                    continue
                if 分类值==6:
                    主体文本=精确值(客户端,7); 长度=struct.unpack('>i',主体文本[3:])[0]
                    if abs(长度)>65536: raise ValueError('clipboard too large')
                    文本=精确值(客户端,abs(长度))
                    if 长度>=0:
                        try: 键盘条目.剪贴板值=文本.decode('utf-8').encode('utf-8')
                        except UnicodeDecodeError: 键盘条目.剪贴板值=文本.decode('latin-1').encode('utf-8')
                        键盘条目.剪贴板值=键盘条目.剪贴板值[:65536].decode('utf-8','ignore').encode('utf-8')
                    服务器值.sendall(bytes([分类值])+主体文本+文本); continue
                if 分类值==0:
                    主体文本=精确值(客户端,19)
                    if 主体文本[3] not in (8,16,32):raise ValueError('unsupported pixel size')
                    像素字节列=主体文本[3]//8
                elif 分类值==2:
                    主体文本=精确值(客户端,3); 条目个数=struct.unpack('>H',主体文本[1:])[0]
                    if 条目个数>512: raise ValueError('too many encodings')
                    已编码值列=struct.unpack('>'+str(条目个数)+'i',精确值(客户端,条目个数*4))
                    指针支持=-239 in 已编码值列
                    # 로컬 屏幕 중계는 默认值 Raw만 요청하여 프레임 경계에서 포인터를 숨긴다.
                    主体文本=struct.pack('>BHi',0,1,0)
                elif 分类值 in (3,150): 主体文本=精确值(客户端,9)
                elif 分类值==248:
                    主体文本=精确值(客户端,8)
                    if 主体文本[7]>64: raise ValueError('fence too large')
                    主体文本+=精确值(客户端,主体文本[7])
                elif 分类值==250: 主体文本=精确值(客户端,3)
                elif 分类值==251:
                    主体文本=精确值(客户端,7)
                    if 主体文本[5]>16: raise ValueError('too many screens')
                    主体文本+=精确值(客户端,主体文本[5]*16)
                else: raise ValueError('unsupported RFB message {}'.format(分类值))
                服务器值.sendall(bytes([分类值])+主体文本)
        except (OSError,EOFError,ValueError) as 错误:
            if str(错误): print('VNC client:',错误,file=sys.stderr,flush=True)
        finally:
            for 套接字值 in (客户端,服务器值):
                try: 套接字值.shutdown(socket.SHUT_RDWR)
                except OSError: pass
                套接字值.close()


def 运行桌面(端口编号=5902, 使用网络=False, 文件传送端口编号=2121, 转发中规则列=(), 分辨率值=(640, 480), 客户机地址=None, 宿主地址='127.0.0.1'):
    with ExitStack() as 资源集, tempfile.TemporaryDirectory(prefix='jkoros-desktop-') as 工作中路径:
        网络桥接条目 = None
        if 使用网络:
            from 网络桥接 import 网络桥接
            网络桥接条目 = 资源集.enter_context(网络桥接(文件传送端口编号, 转发中规则列, 客户机地址=客户机地址, 宿主地址=宿主地址))
        路径=Path(工作中路径)/'display.sock'
        with socket.socket() as 接收端口:
            接收端口.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            接收端口.bind(('127.0.0.1',端口编号)); 接收端口.listen(1); 接收端口.settimeout(.2)
            VNC端口=接收端口.getsockname()[1]
            if 网络桥接条目 and (VNC端口==文件传送端口编号 or 50000<=VNC端口<=50007 or any(网络ABI=='tcp' and 宿主==VNC端口 for 网络ABI,宿主,_ in 网络桥接条目.转发中规则列)):
                raise ValueError('VNC port conflicts with an FTP/TCP forwarding port')
            进程=subprocess.Popen(命令(分辨率值)+['-display','none','-monitor','none','-serial','stdio','-vnc','unix:'+str(路径)]+(网络桥接条目.已转发参数() if 网络桥接条目 else []),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            桥接=连接桌面(进程); 读取器=threading.Thread(target=桥接.串行输入输出,daemon=True); 读取器.start()
            print('DESKTOP VNC 127.0.0.1:{} — Remmina VNC; keyboard/Unicode/paste bridge; Ctrl+C stops VM'.format(接收端口.getsockname()[1]),flush=True)
            if 网络桥接条目: print('NETWORK FTP {}:{} — guest command: ftpd start'.format(宿主地址,文件传送端口编号),flush=True)
            def 终止(信号编号,执行状态帧): raise KeyboardInterrupt()
            上一个=signal.signal(signal.SIGTERM,终止)
            处理任务=None; 已中断=False
            try:
                while 进程.poll() is None:
                    try: 客户端,_=接收端口.accept()
                    except socket.timeout: continue
                    if 处理任务 is not None and 处理任务.is_alive(): 客户端.close(); continue
                    if not 路径.exists(): 客户端.close(); continue
                    处理任务=threading.Thread(target=桥接.客户端,args=(客户端,路径),daemon=True); 处理任务.start()
            except KeyboardInterrupt: 已中断=True
            finally:
                桥接.是否已关闭=True
                if 网络桥接条目: 网络桥接条目.暂停事件.set()
                if 进程.poll() is None:
                    进程.terminate()
                    try: 进程.wait(timeout=5)
                    except subprocess.TimeoutExpired: 进程.kill(); 进程.wait()
                读取器.join(timeout=2); 进程.stdin.close(); 进程.stdout.close(); signal.signal(signal.SIGTERM,上一个)
            if 网络桥接条目 and 网络桥接条目.错误: raise RuntimeError('network bridge: '+网络桥接条目.错误)
            return 0 if 已中断 else 进程.returncode


if __name__=='__main__':
    from 执行命令 import 读取分辨率
    参数解析器=argparse.ArgumentParser(description=__doc__); 参数解析器.add_argument('--port',type=int,default=5902)
    参数解析器.add_argument('--resolution',type=读取分辨率,default=(640,480))
    参数解析器.add_argument('--network',action='store_true'); 参数解析器.add_argument('--ftp-port',type=int,default=2121)
    参数解析器.add_argument('--forward',action='append',default=[])
    参数数组=参数解析器.parse_args()
    if 参数数组.forward and not 参数数组.network: 参数解析器.error('--forward requires --network')
    raise SystemExit(运行桌面(参数数组.port,使用网络=参数数组.network,文件传送端口编号=参数数组.ftp_port,转发中规则列=参数数组.forward,分辨率值=参数数组.resolution))

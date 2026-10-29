#!/usr/bin/env python3
"""实际数据 RFB 클라이언트로 QEMU 창의 한글/键值/클립보드/마우스와 屏幕 전송을 검사한다."""
import hashlib
import json
import re
import selectors
import socket
import struct
import subprocess
import time
from pathlib import Path
from 桌面视图 import 精确值
from 执行命令 import 项目根


def 运行():
    输出结果=项目根/'build/verification/desktop'; 输出结果.mkdir(parents=True,exist_ok=True)
    进程=subprocess.Popen(['python3',str(项目根/'工具集/桌面视图.py'),'--port','0'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    就绪情况监视器=selectors.DefaultSelector(); 就绪情况监视器.register(进程.stdout,selectors.EVENT_READ)
    执行记录=bytearray(); 有效性验证报告={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((项目根/'build/kernel8.img').read_bytes()).hexdigest()}
    def 直到(标记,运行=0):
        截止时间时间=time.monotonic()+45
        while 标记 not in 执行记录[运行:]:
            if time.monotonic()>截止时间时间 or 进程.poll() is not None: raise AssertionError(执行记录[运行:].decode('utf-8','replace'))
            for 已按下值,_ in 就绪情况监视器.select(.1):
                数据=已按下值.fileobj.read(4096)
                if 数据: 执行记录.extend(数据)
        return bytes(执行记录[运行:])
    try:
        直到(b'TERMINAL READY')
        端口编号=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',执行记录).group(1))
        with socket.create_connection(('127.0.0.1',端口编号),timeout=10) as 客户端:
            assert 精确值(客户端,12)==b'RFB 003.008\n'; 客户端.sendall(b'RFB 003.008\n')
            assert 1 in 精确值(客户端,精确值(客户端,1)[0]); 客户端.sendall(b'\x01'); assert 精确值(客户端,4)==b'\0'*4
            客户端.sendall(b'\x01'); 初始值=精确值(客户端,24); assert struct.unpack('>HH',初始值[:4])==(640,480); 精确值(客户端,struct.unpack('>I',初始值[20:])[0])
            客户端.sendall(b'\x00\x00\x00\x00'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
            客户端.sendall(struct.pack('>BBHi',2,0,1,0))
            def 已按下值(符号值,是否按下中=True): 客户端.sendall(struct.pack('>BBHI',4,int(是否按下中),0,符号值))
            def 已输入字符(文本):
                for 字符数据 in 文本:
                    符号=0xff0d if 字符数据=='\n' else ord(字符数据) if ord(字符数据)<256 else 0x01000000|ord(字符数据)
                    已按下值(符号); 已按下值(符号,False)
            def 按下键(符号值): 已按下值(符号值); 已按下值(符号值,False)
            # Start with English keys only, as delivered without a host IME.
            偏移值=len(执行记录); 已输入字符('echo '); 按下键(0xffc6)
            已输入字符('dkssudgktpdy gksrmf'); 按下键(0xffc6); 已输入字符('\n')
            直到('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),偏移值)
            偏移值=len(执行记录); 已输入字符('echo ')
            已按下值(0xffe1); 按下键(32); 已按下值(0xffe1,False)
            已输入字符('dlfr'); 按下键(0xff08); 按下键(0xff08); 已输入字符('fr')
            按下键(0xff31); 已输入字符(' EN\n')
            直到('\r\n읽 EN\r\njkoros-native> '.encode(),偏移值)
            偏移值=len(执行记录); 已输入字符('echo '); 按下键(0xff31)
            已输入字符('rhk rkqtk RkRnd'); 按下键(0xff31); 已输入字符('\n')
            直到('\r\n과 갑사 까꿍\r\njkoros-native> '.encode(),偏移值)
            # The same composition edits UTF-8 text in the native vi editor.
            偏移值=len(执行记录); 已输入字符('vi 韩文字母输入.txt\n'); 直到(b'NORMAL',偏移值)
            已输入字符('i'); 按下键(0xffc6); 已输入字符('gksrmf dlfr'); 按下键(0xffc6)
            按下键(0xff1b); 已输入字符(':wq\n'); 直到(b'jkoros-native> ',偏移值)
            偏移值=len(执行记录); 已输入字符('cat 韩文字母输入.txt\n')
            直到('한글 읽'.encode(),偏移值); 直到(b'jkoros-native> ',偏移值)
            偏移值=len(执行记录); 已输入字符('help ko\n')
            直到('한/零操作数 键值, Shift+Space 또는 F9'.encode(),偏移值); 直到(b'jkoros-native> ',偏移值)
            偏移值=len(执行记录); 已输入字符('clear\necho "VNC 한글 输入值 😀"\n'); 直到('VNC 한글 输入值 😀\r\n'.encode(),偏移值)
            偏移值=len(执行记录); 已按下值(0xffe3); 已按下值(ord('u')); 已按下值(ord('u'),False); 已按下值(0xffe3,False); 已输入字符('echo CONTROL_OK\n'); 直到(b'\r\nCONTROL_OK\r\n',偏移值)
            # A shared clipboard is not a paste command. Require explicit Ctrl+Shift+V.
            剪贴板值='echo "粘贴值 是否完成"\n'.encode(); 偏移值=len(执行记录)
            客户端.sendall(struct.pack('>B3xI',6,len(剪贴板值))+剪贴板值)
            for 事件,_ in 就绪情况监视器.select(.15):
                数据块=事件.fileobj.read(4096)
                if 数据块: 执行记录.extend(数据块)
            assert '粘贴值 是否完成'.encode() not in 执行记录[偏移值:]
            已按下值(0xffe3); 已按下值(0xffe1); 已按下值(ord('v')); 已按下值(ord('v'),False); 已按下值(0xffe1,False); 已按下值(0xffe3,False)
            # The prompt follows the guest's terminal redraw after command completion.
            直到('\r\n붙여넣기 是否完成\r\njkoros-native> '.encode(),偏移值)
            客户端.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
            红_绿_蓝颜色=bytearray(640*480*3); 已看见条目列=False
            while not 已看见条目列:
                通知文本=精确值(客户端,1)[0]
                if 通知文本==2: continue
                if 通知文本==3:
                    大小=struct.unpack('>I',精确值(客户端,7)[3:])[0]; 精确值(客户端,大小); continue
                assert 通知文本==0,通知文本
                矩形列列表=struct.unpack('>H',精确值(客户端,3)[1:])[0]
                for _ in range(矩形列列表):
                    横坐标坐标,Y_按钮坐标,已请求宽度值,已请求高度值,字符设定=struct.unpack('>HHHHi',精确值(客户端,12)); assert 字符设定==0,字符设定
                    像素列列表=精确值(客户端,已请求宽度值*已请求高度值*4)
                    for 内部侧序数 in range(已请求高度值):
                        for 序数索引 in range(已请求宽度值):
                            原始地址=(内部侧序数*已请求宽度值+序数索引)*4; 目的地址地址=((Y_按钮坐标+内部侧序数)*640+横坐标坐标+序数索引)*3
                            红_绿_蓝颜色[目的地址地址:目的地址地址+3]=bytes((像素列列表[原始地址+2],像素列列表[原始地址+1],像素列列表[原始地址]))
                    已看见条目列=True
            assert 红_绿_蓝颜色[(48*640+12)*3:(48*640+12)*3+3]==bytes((32,80,144))
            (输出结果/'vnc-terminal.ppm').write_bytes(b'P6\n640 480\n255\n'+红_绿_蓝颜色)
            from PIL import Image
            Image.frombytes('RGB',(640,480),bytes(红_绿_蓝颜色)).save(str(输出结果/'vnc-terminal.png'))
            偏移值=len(执行记录)
            已按下值(0xffe3); 已按下值(0xffe1); 已按下值(ord('t')); 已按下值(ord('t'),False); 已按下值(0xffe1,False); 已按下值(0xffe3,False)
            直到(b'TERMINAL FOCUS 2',偏移值)
            偏移值=len(执行记录); 已输入字符('echo SECOND_VNC_WINDOW\n'); 直到(b'\r\nSECOND_VNC_WINDOW\r\n',偏移值)
            偏移值=len(执行记录); 客户端.sendall(struct.pack('>BBHH',5,1,576,81)); 客户端.sendall(struct.pack('>BBHH',5,0,576,81)); 直到(b'TERMINAL FOCUS 1',偏移值)
            偏移值=len(执行记录); 已输入字符('python -c \'print("x"*9000)\'\n'); 直到(b'\r\njkoros-native> ',偏移值)
            assert len(执行记录)-偏移值>8192,'exercise output longer than bridge status buffer'
            偏移值=len(执行记录); 客户端.sendall(struct.pack('>BBHH',5,1,560,63)); 客户端.sendall(struct.pack('>BBHH',5,0,560,63)); 直到(b'TERMINAL FOCUS 1',偏移值)
            偏移值=len(执行记录); 客户端.sendall(struct.pack('>BBHH',5,1,80,16)); 客户端.sendall(struct.pack('>BBHH',5,0,80,16)); 直到(b'TERMINAL FOCUS 1',偏移值)
            偏移值=len(执行记录); 已输入字符('echo REOPENED_VNC_WINDOW\n'); 直到(b'\r\nREOPENED_VNC_WINDOW\r\n',偏移值)
            偏移值=len(执行记录); 已输入字符('gui\n'); 直到(b'GUI READY:',偏移值)
            偏移值=len(执行记录); 客户端.sendall(struct.pack('>BBHH',5,1,80,332)); 客户端.sendall(struct.pack('>BBHH',5,0,80,332)); 直到(b'TERMINAL READY',偏移值)
            有效性验证报告.update(passed=True,checks=['RFB 3.8 handshake and actual 640x480 raw framebuffer','F9, Shift+Space and Hangul toggle: ASCII two-set keys compose Korean in shell and vi','compound vowels/finals, resyllabification and composition Backspace','help ko lists implemented shortcuts','Unicode Hangul/emoji keysyms -> guest shell','Ctrl modifiers and explicit clipboard paste; no clipboard auto-execution','Ctrl+Shift+T creates second native terminal, mouse X closes it','mouse close after 9 KiB output, desktop new-terminal button and legacy launcher button'])
        print('PASS: actual VNC keyboard/Unicode/paste/mouse/framebuffer -> native terminal')
    finally:
        if 进程.poll() is None:
            进程.terminate()
            try: 进程.wait(timeout=8)
            except subprocess.TimeoutExpired: 进程.kill(); 进程.wait()
        就绪情况监视器.close(); 进程.stdout.close()
        (输出结果/'serial.log').write_bytes(执行记录)
        (输出结果/'report.json').write_text(json.dumps(有效性验证报告,indent=2)+'\n')


if __name__=='__main__': 运行()

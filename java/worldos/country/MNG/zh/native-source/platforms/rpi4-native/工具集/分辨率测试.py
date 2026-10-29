#!/usr/bin/env python3
"""实际数据 QEMU/VNC에서 屏幕 大小·边界位置值·窗口 移动值·Swing·언어별 그리기를 검사한다."""
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
from 桌面视图 import 精确值
from 执行命令 import 项目根


def 分辨率测试(宽度值, 高度值, 结果路径):
    with socket.socket() as 临时值:
        临时值.bind(('127.0.0.1', 0)); 端口编号 = 临时值.getsockname()[1]
    大小文本 = '{}x{}'.format(宽度值, 高度值)
    进程值 = subprocess.Popen(['python3', str(项目根/'工具集/执行命令.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(端口编号), '--resolution', 大小文本], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    选择器 = selectors.DefaultSelector(); 选择器.register(进程值.stdout, selectors.EVENT_READ)
    日志记录 = bytearray(); 远程值 = None; 传送值 = None

    def 等待(显示值, 运行=0):
        截止时间值 = time.monotonic() + 60
        while 显示值 not in 日志记录[运行:]:
            if time.monotonic() > 截止时间值 or 进程值.poll() is not None or b'HALTED' in 日志记录 or b'PANIC:' in 日志记录:
                raise AssertionError(日志记录[运行:].decode('utf-8', 'replace'))
            for 事件, _ in 选择器.select(.1):
                数据 = 事件.fileobj.read(65536)
                if 数据: 日志记录.extend(数据)
        return 日志记录[运行:].decode('utf-8', 'replace')

    def 单击按钮(符号, 是否已按下=True): 远程值.sendall(struct.pack('>BBHI', 4, int(是否已按下), 0, 符号))

    def 发送文本(文本):
        运行 = len(日志记录)
        for 字符值 in 文本:
            符号 = 0xff0d if 字符值 == '\n' else ord(字符值) if ord(字符值) < 256 else 0x1000000 | ord(字符值)
            单击按钮(符号); 单击按钮(符号, False)
        return 运行

    def 命令壳(文本): return 等待(b'\r\n__RESOLUTION_DONE__\r\n', 发送文本(文本+'; echo __RESOLUTION_DONE__\n'))

    def 分位置(水平位置, 垂直位置, 是否已按下): 远程值.sendall(struct.pack('>BBHH', 5, 是否已按下, 水平位置, 垂直位置))

    def 单击值(水平位置, 垂直位置): 分位置(水平位置, 垂直位置, 1); 分位置(水平位置, 垂直位置, 0)

    def 位图映像():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 实际数据 너비를 쓴다.
        远程值.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 宽度值, 高度值))
        绘图 = Image.new('RGB', (宽度值, 高度值)); 区域面积值 = 0
        while True:
            种类值 = 精确值(远程值, 1)[0]
            if 种类值 == 2: continue
            if 种类值 == 3:
                长度 = struct.unpack('>I', 精确值(远程值, 7)[3:])[0]; 精确值(远程值, 长度); continue
            assert 种类值 == 0, 种类值
            项目个数 = struct.unpack('>H', 精确值(远程值, 3)[1:])[0]
            for _ in range(项目个数):
                水平位置, 垂直位置, 宽度跨度, 长度, 编码状态值 = struct.unpack('>HHHHi', 精确值(远程值, 12))
                assert 编码状态值 == 0 and 水平位置+宽度跨度 <= 宽度值 and 垂直位置+长度 <= 高度值
                绘图.paste(Image.frombytes('RGB', (宽度跨度, 长度), 精确值(远程值, 宽度跨度*长度*4), 'raw', 'BGRX'), (水平位置, 垂直位置))
                区域面积值 += 宽度跨度*长度
            if 区域面积值:
                assert 区域面积值 == 宽度值*高度值, 区域面积值
                return 绘图

    def 检查像素(坐标值, 颜色值):
        截止时间值 = time.monotonic()+10
        while True:
            绘图 = 位图映像()
            if 绘图.getpixel(坐标值) == 颜色值: return 绘图
            if time.monotonic() > 截止时间值: raise AssertionError((坐标值, 绘图.getpixel(坐标值), 颜色值))

    def 上传文件集(名称, 数据): 传送值.storbinary('STOR '+名称, io.BytesIO(数据))

    try:
        等待(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+大小文本+' RGB32').encode() in 日志记录
        print('BOOT:', 大小文本, flush=True)
        远程编号 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', 日志记录).group(1))
        远程值 = socket.create_connection(('127.0.0.1', 远程编号), timeout=20)
        assert 精确值(远程值, 12) == b'RFB 003.008\n'; 远程值.sendall(b'RFB 003.008\n')
        assert 1 in 精确值(远程值, 精确值(远程值, 1)[0]); 远程值.sendall(b'\x01')
        assert 精确值(远程值, 4) == b'\0'*4; 远程值.sendall(b'\x01')
        初始状态 = 精确值(远程值, 24); assert struct.unpack('>HH', 初始状态[:4]) == (宽度值, 高度值)
        精确值(远程值, struct.unpack('>I', 初始状态[20:])[0])
        远程值.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        远程值.sendall(struct.pack('>BBHi', 2, 0, 1, 0))
        检查像素((宽度值-1, 高度值-1), (24, 32, 48))
        # 屏幕 右 아래까지 이동한다. 上一个项目 640×480 边界位置值 밖에서 X를 누른다.
        分位置(40, 60, 1); 分位置(宽度值-568+28, 高度值-360+12, 1); 分位置(宽度值-568+28, 高度值-360+12, 0)
        检查像素((宽度值-568, 高度值-360), (32, 80, 144))
        运行 = len(日志记录); 单击值(宽度值-20, 高度值-345); 等待(b'TERMINAL FOCUS 1', 运行)
        检查像素((宽度值-568, 高度值-360), (24, 32, 48))
        运行 = len(日志记录); 单击值(80, 16); 等待(b'TERMINAL FOCUS 1', 运行)
        命令壳('ftpd start')
        传送值 = ftplib.FTP(); 传送值.encoding = 'utf-8'; 传送值.connect('127.0.0.1', 端口编号, timeout=20); 传送值.login()
        # C 边界位置值 검사는 32비트 unsigned 负数值 转换值·裁剪 밖·빈 사각형을 포함한다.
        源代码 = '''#include <屏幕ABI.h>
#include <文件ABI.h>
int main(void) {
    unsigned 宽度值=屏幕宽度(), 高度值=屏幕高度();
    if(宽度值!=WIDTH || 高度值!=HEIGHT) return 1;
    if(绘制矩形(宽度值,高度值,0,0,0)) return 2;
    if(绘制矩形(宽度值,高度值-1,1,1,0)!=-22) return 3;
    if(绘制矩形(宽度值-1,高度值,1,1,0)!=-22) return 4;
    if(绘制矩形(-1,0,1,1,0)!=-22) return 5;
    if(绘制矩形(0,0,-1,1,0)!=-22) return 6;
    if(绘制矩形(宽度值-1,高度值-1,1,1,0x332211)) return 7;
    写入文件数据(1,"C RESOLUTION PASS\\n",18);
    等待状态用于绘图(); return 0;
}
'''.replace('WIDTH', str(宽度值)).replace('HEIGHT', str(高度值))
        上传文件集('测试屏幕.c', 源代码.encode())
        assert 'exit 0' in 命令壳('cc /测试屏幕.c -o /测试屏幕')
        等待(b'C RESOLUTION PASS', 发送文本('run /测试屏幕\n'))
        检查像素((宽度值-1, 高度值-1), (17, 34, 51))
        等待(b'jkoros-native> ', 发送文本('q'))
        源代码 = '''from 中文 import 屏幕大小, 绘制矩形, 等待状态用于绘图, 输出, 系统错误
宽度值, 高度值 = 屏幕大小()
assert (宽度值, 高度值) == (WIDTH, HEIGHT)
try:
    绘制矩形(宽度值, 高度值-1, 1, 1, 0)
    raise AssertionError("boundary")
except 系统错误 as 错误:
    assert 错误.编号 == 22
绘制矩形(宽度值-1, 高度值-1, 1, 1, 0x665544)
输出("PYTHON RESOLUTION PASS")
等待状态用于绘图()
'''.replace('WIDTH', str(宽度值)).replace('HEIGHT', str(高度值))
        上传文件集('测试屏幕.py', 源代码.encode())
        等待(b'PYTHON RESOLUTION PASS', 发送文本('python /测试屏幕.py\n'))
        检查像素((宽度值-1, 高度值-1), (68, 85, 102))
        等待(b'jkoros-native> ', 发送文本('q'))
        源代码 = '''import 中文.内置.*;
public class 分辨率测试 {
    public static void main(String[] 实参) {
        int 宽度值=屏幕.宽度值(), 高度值=屏幕.高度值();
        if (宽度值!=WIDTH || 高度值!=HEIGHT) throw new 状态异常("大小");
        try { 屏幕.矩形(宽度值,高度值-1,1,1,0); throw new 状态异常("裁剪"); }
        catch (无效参数异常 错误) { }
        屏幕.擦除条目(0x302018);
        屏幕.矩形(宽度值-1,高度值-1,1,1,0x998877);
        System.out.println("JAVA RESOLUTION PASS");
        屏幕.等待();
    }
}
'''.replace('WIDTH', str(宽度值)).replace('HEIGHT', str(高度值))
        # 异常 처리는 宿主 javac 결과를 内置 JVM에 올려 검사한다.
        边界位置源代码 = 结果路径/'해상도경계시험.java'
        边界位置源代码.write_text(源代码.replace('class 分辨率测试', 'class 해상도경계시험'))
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(项目根/'dist/jkoros-native-korean.jar'), '-d', str(结果路径), str(边界位置源代码)])
        上传文件集('해상도경계시험.class', (结果路径/'해상도경계시험.class').read_bytes())
        等待(b'JAVA RESOLUTION PASS', 发送文本('java 해상도경계시험\n'))
        检查像素((宽度值-1, 高度值-1), (119, 136, 153))
        等待(b'jkoros-native> ', 发送文本('q'))
        # 게스트 javac의 支持值 문법으로 大小 查询值·擦除条目·다섯 实参 그리기를 컴파일한다.
        源代码 = '''public class 分辨率测试 {
    public static void main(String[] 实参) {
        int 宽度值=中文.内置.屏幕.宽度值();
        int 高度值=中文.内置.屏幕.高度值();
        if (宽度值!=WIDTH || 高度值!=HEIGHT) return;
        中文.内置.屏幕.擦除条目(3153944);
        中文.内置.屏幕.矩形(宽度值-1,高度值-1,1,1,10061943);
        中文.内置.输出.写入行("JAVA RESOLUTION PASS");
        中文.内置.屏幕.等待();
    }
}
'''.replace('WIDTH', str(宽度值)).replace('HEIGHT', str(高度值))
        上传文件集('分辨率测试.java', 源代码.encode())
        结果 = 命令壳('javac 分辨率测试.java'); assert 'exit 0' in 结果, 结果
        等待(b'JAVA RESOLUTION PASS', 发送文本('java 分辨率测试\n'))
        检查像素((宽度值-1, 高度值-1), (119, 136, 153))
        等待(b'jkoros-native> ', 发送文本('q'))
        上传文件集('Swing测试.class', (结果路径/'Swing测试.class').read_bytes())
        等待(b'SWING READY', 发送文本('java Swing测试\n'))
        水平位置, 垂直位置 = (宽度值-400)//2, (高度值-280)//2
        绘图 = 检查像素((水平位置, 垂直位置), (32, 80, 144))
        绘图.save(str(结果路径/(大小文本+'.png')))
        运行 = len(日志记录); 单击值(水平位置+80, 垂直位置+155)
        等待('SWING CLICK 名称'.encode(), 运行)
        运行 = len(日志记录); 单击值(水平位置+385, 垂直位置+15); 等待(b'jkoros-native> ', 运行)
        assert 'AFTER_RESOLUTION' in 命令壳('echo AFTER_RESOLUTION')
        print('PASS:', 大小文本, 'RGB32, VNC, terminal drag/close, C/Python/Java bounds, centered Swing callbacks', flush=True)
    finally:
        if 传送值: 传送值.close()
        if 远程值: 远程值.close()
        if 进程值.poll() is None:
            进程值.terminate()
            try: 进程值.wait(timeout=8)
            except subprocess.TimeoutExpired: 进程值.kill(); 进程值.wait()
        选择器.close(); 进程值.stdout.close()
        (结果路径/(大小文本+'.log')).write_bytes(日志记录)


def 运行():
    结果路径 = 项目根/'build/verification/resolution'; 结果路径.mkdir(parents=True, exist_ok=True)
    日志记录 = {'passed': False, 'kernel_sha256': hashlib.sha256((项目根/'build/kernel8.img').read_bytes()).hexdigest(), 'resolutions': []}
    try:
        for 无效值 in ('0x0', '639x480', '1920x1081', '1921x1080', '1920*1080'):
            结果 = subprocess.run(['python3', str(项目根/'工具集/执行命令.py'), '--resolution', 无效值], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            assert 结果.returncode == 2 and b'--resolution' in 结果.stderr
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(结果路径), str(项目根/'测试/Java/Swing测试.java')])
        for 宽度值, 高度值 in ((1920,1080), (1280,720), (640,480)):
            分辨率测试(宽度值, 高度值, 结果路径); 日志记录['resolutions'].append([宽度值, 高度值])
        日志记录.update(passed=True, linux_loaded=False, physical_board_tested=False,
            checks=['RFB actual geometry and full-frame RGB32 pixels', 'terminal drag and close at bottom right',
                    'guest cc/javac and Python: Korean size API, last pixel, rejected out-of-bounds drawing',
                    'Swing centered placement, button callback and X', 'desktop and FTP networking together', 'invalid CLI sizes rejected'])
    finally:
        (结果路径/'report.json').write_text(json.dumps(日志记录, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__': 运行()

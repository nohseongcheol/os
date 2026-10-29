#!/usr/bin/env python3
"""实际数据 QEMU/VNC에서 终端 角值 拖动值·指针·동적 字符值 槽条目·编辑值 内容值 보존를 검사한다."""
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


def 测试窗口尺寸调整中(宽度值, 高度值, 结果路径):
    with socket.socket() as 临时值:
        临时值.bind(('127.0.0.1', 0)); 端口编号 = 临时值.getsockname()[1]
    大小文本 = '{}x{}'.format(宽度值, 高度值)
    进程值 = subprocess.Popen(['python3', str(项目根/'工具集/执行命令.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(端口编号), '--resolution', 大小文本], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    选择器 = selectors.DefaultSelector(); 选择器.register(进程值.stdout, selectors.EVENT_READ)
    日志记录 = bytearray(); 远程值 = None; 传送值 = None; 指针隐藏=[False]

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

    def 命令壳(文本): return 等待(b'\r\n__RESIZE_DONE__\r\n', 发送文本(文本+'; echo __RESIZE_DONE__\n'))

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
                if 编码状态值 == -239:
                    assert 宽度跨度==0 and 长度==0, 'remote cursor must be hidden'
                    指针隐藏[0]=True
                    continue
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
        远程值.sendall(struct.pack('>BBHii', 2, 0, 2, 0, -239))
        检查像素((宽度值-1, 高度值-1), (24, 32, 48))
        def 暂停短暂地(秒数值=.25):
            结尾=time.monotonic()+秒数值
            while time.monotonic()<结尾:
                for 事件,_ in 选择器.select(.02):
                    数据=事件.fileobj.read(65536)
                    if 数据:日志记录.extend(数据)
        窗口=[12,48,568,360]
        def 验证大小():
            列值,行值=(窗口[2]-24)//8,(窗口[3]-56)//16
            文本=命令壳('terminal size')
            assert 'TERMINAL SIZE {}x{}\r\n'.format(列值,行值) in 文本,文本
            # 实际数据 窗口 테두리: 단지 大小 查询值 값만 바뀐 것이 아닌지 확인한다.
            分位置(宽度值-1,10,0);暂停短暂地()
            检查像素((窗口[0],窗口[1]),(32,80,144))
            绘图=检查像素((窗口[0]+窗口[2]-1,窗口[1]+窗口[3]-1),(39,49,64))
            return 绘图
        def 角值(方向):
            return (窗口[0]+(3 if 方向 in (1,3) else 窗口[2]-4),窗口[1]+(3 if 方向<=2 else 窗口[3]-4))
        def 调整尺寸拖动(方向,差异值,按钮=1):
            首位操作数,三值=角值(方向);分位置(首位操作数,三值,0);暂停短暂地()
            # 대각선 양방향 화살표의 흰 선과 반대 방향의 빈 점을 확인한다.
            白像素=(首位操作数-7 if 方向 in (1,4) else 首位操作数+7,三值-7)
            检查像素(白像素,(255,255,255))
            分位置(首位操作数,三值,按钮)
            结束水平=max(0,min(宽度值-1,首位操作数+差异值[0]));结束垂直=max(0,min(高度值-1,三值+差异值[1]))
            分位置(结束水平,结束垂直,按钮);分位置(结束水平,结束垂直,0);暂停短暂地()
            if 按钮==1:
                左值,顶端值,宽度跨度,长度=窗口;右值,底端值=左值+宽度跨度,顶端值+长度
                if 方向 in (1,3):左值=max(0,min(右值-360,左值+结束水平-首位操作数))
                else:右值=max(左值+360,min(宽度值,右值+结束水平-首位操作数))
                if 方向<=2:顶端值=max(34,min(底端值-216,顶端值+结束垂直-三值))
                else:底端值=max(顶端值+216,min(高度值,底端值+结束垂直-三值))
                窗口[:]=[左值,顶端值,右值-左值,底端值-顶端值]
        验证大小();assert 指针隐藏[0]
        调整尺寸拖动(4,(-100,-60),4);验证大小() # 右 버튼은 크기를 바꾸지 않는다.
        for 方向,差异值 in ((4,(-120,-80)),(1,(24,16)),(2,(40,16)),(3,(24,32))):
            调整尺寸拖动(方向,差异值);验证大小()
        # 输入值 중인 긴 韩文文本 명령은 换行/水平位置 스크롤과 무관하게 그대로 실행된다.
        长整数文本='크기가 바뀌어도 입력한 한글 명령이 그대로 남습니다 '*3
        发送文本("echo '"+长整数文本+"'");暂停短暂地()
        调整尺寸拖动(4,(-1000,-1000));assert 窗口[2:]==[360,216]
        调整尺寸拖动(4,(宽度值,高度值))
        运行=发送文本('\n');等待(('\r\n'+长整数文本+'\r\n').encode(),运行);验证大小()
        # vi가 编辑值 중에 屏幕 크기를 重试值 읽고, 저장하지 않은 한글도 유지한다.
        命令壳('ftpd start')
        传送值=ftplib.FTP();传送值.encoding='utf-8';传送值.connect('127.0.0.1',端口编号,timeout=20);传送值.login()
        等待(b'NORMAL',发送文本('vi /크기자료.txt\n'))
        等待(b'INSERT',发送文本('i미저장 한글 数据\n'));暂停短暂地()
        调整尺寸拖动(4,(-宽度值,-高度值))
        # ANSI 行值 이동에 새 行值 수가 나타나는지, 한 글자도 입력하지 않고 확인한다.
        assert ('\x1b[{};1H'.format((窗口[3]-56)//16)).encode() in 日志记录[-4096:]
        发送文本('작은 창에서도 继续状态值 写入\n');暂停短暂地()
        调整尺寸拖动(4,(宽度值,高度值))
        发送文本('큰 창에서도 继续状态值 写入\n');暂停短暂地()
        单击按钮(0xff1b);单击按钮(0xff1b,False);暂停短暂地()
        等待(b'jkoros-native> ',发送文本(':wq\n'))
        内容值=bytearray();传送值.retrbinary('RETR 크기자료.txt',内容值.extend)
        assert 内容值=='미저장 한글 数据\n작은 창에서도 继续状态值 写入\n큰 창에서도 继续状态值 写入\n'.encode(),内容值
        验证大小().save(str(结果路径/(大小文本+'-large.png')))
        # 두 번째 창은 默认值 大小, 重试值 首位项目 창을 고르면 앞에서 바꾼 크기가 유지된다.
        运行=len(日志记录);单击值(70,16);等待(b'TERMINAL FOCUS 2',运行)
        assert 'TERMINAL SIZE 68x19' in 命令壳('terminal size')
        运行=len(日志记录);单击值(180,16);等待(b'TERMINAL FOCUS 1',运行);验证大小()
        调整尺寸拖动(4,(-宽度值,-高度值));验证大小().save(str(结果路径/(大小文本+'-small.png')))
        # 大小 更改值 后端值 X 닫기도 새로운 右 가장자리를 사용한다.
        运行=len(日志记录);单击值(窗口[0]+窗口[2]-20,窗口[1]+15);等待(b'TERMINAL FOCUS 2',运行)
        assert 'RESIZE CLOSED' in 命令壳('echo RESIZE CLOSED')
        print('PASS:',大小文本,'four corners, left drag, cursor, limits, live shell/vi, independent windows',flush=True)
    finally:
        if 传送值:传送值.close()
        if 远程值:远程值.close()
        if 进程值.poll() is None:
            进程值.terminate()
            try:进程值.wait(timeout=8)
            except subprocess.TimeoutExpired:进程值.kill();进程值.wait()
        选择器.close();进程值.stdout.close();(结果路径/(大小文本+'.log')).write_bytes(日志记录)


def 运行():
    结果路径=项目根/'build/verification/resize';结果路径.mkdir(parents=True,exist_ok=True)
    日志记录={'passed':False,'kernel_sha256':hashlib.sha256((项目根/'build/kernel8.img').read_bytes()).hexdigest(),'resolutions':[]}
    try:
        for 宽度值,高度值 in ((640,480),(1920,1080)):
            测试窗口尺寸调整中(宽度值,高度值,结果路径);日志记录['resolutions'].append([宽度值,高度值])
        日志记录.update(passed=True,checks=['native diagonal cursor pixels and hidden RFB cursor','all four corners use left drag; right drag ignored',
            'minimum/maximum geometry and current text rows/columns','long Korean shell input and unsaved vi text preserved',
            'vi redraws during idle resize','per-window geometry and resized X close'])
    finally:(结果路径/'report.json').write_text(json.dumps(日志记录,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':运行()
